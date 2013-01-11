import time
import types
import urllib

from datetime import datetime, timedelta


#--- Message senders ----------------------------------------------
class SenderTropo:

    def __init__(self, api_token, numbers):
        self.api_token = api_token

        if type(numbers) != types.ListType:
            numbers = [numbers]

        self.numbers = numbers

    def send_notification(self, name, crash_message):
        statuses = []

        for number in self.numbers:
            data = urllib.urlencode({
                'action': 'create',
                'token': self.api_token,
                'numberToDial': number.replace(' ', ''),
                'msg': '%s: %s' % (name, crash_message)
            })

            fp = urllib.urlopen('https://api.tropo.com/1.0/sessions',
                                data)

            statuses.append( fp.read() )

        return '  '.join(statuses)


class SenderMail:
    """Send mail notifications using a specified SMTP server."""
    
    def __init__(self, mail_to, mail_from, smtp_host, smtp_user, smtp_password, smtp_port=587, tls=True):
        """Construct mail notification sender class.

        `mail_to` the email address (or list of email addresses) to send the notification to.
        `mail_from` the email address that the notification should be sent from.
        `smtp_host` the IP address or hostname of the SMTP server.
        `smtp_user` the user to authenticate the SMTP connection with.
        `smtp_password` the password to authenticate the SMTP connection with.
        `smtp_port` the port number of the SMTP server (defaults to 587).
        `tls` specifies if TLS must be used to encrypt the connection (defaults to True).
        """
        if (isinstance(mail_to, str)):
            self.mail_to = (mail_to,)
        else:
            self.mail_to = mail_to
        self.mail_from = mail_from
        self.smtp_host = smtp_host
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_port = smtp_port
        self.use_tls = tls

    def send_notification(self, name, crash_message):
        """Send an mail notification about a crash event.

        `name` the name of the crash checker that initiated the notificaton.
        `crash_message` the message from the crash error.
        """
        from smtplib import SMTP
        from email.MIMEText import MIMEText

        # build message
        message = MIMEText(crash_message, 'plain')
        message['Subject'] = name
        message['To'] = ','.join(self.mail_to)
        message['From'] = self.mail_from

        # connect to SMTP server and send message
        connection = SMTP(self.smtp_host, self.smtp_port)
        connection.ehlo()
        if self.use_tls:
            # put SMTP connection into TLS mode so that further commands are encrypted
            connection.starttls()
            connection.ehlo()
        connection.login(self.smtp_user, self.smtp_password)
        try:
            connection.sendmail(self.mail_from, self.mail_to, message.as_string())
            return True # success
        except:
            return False # failure
        finally:
            connection.quit()


#--- Exceptions ----------------------------------------------
class ReportCrash(Exception):
    pass



#--- Impl ----------------------------------------------
class CrashHound:

    def __init__(self, sender):
        self.check_functions = {}
        self.sender = sender

    #--- Registers ----------------------------------------------
    def register_check(self, name, check_fn, notify_every=240):
        """Register a check.

        `check_fn` should throw ReportCrash to indicate that a check has failed.
        `notify_every` indicates how often a notification should be sent.
        The default is 240 (it will send a notifcation every 4 minutes if the check keeps failing).

        Example of a custom check looks like this::

            def check_fn():
                if 42:
                    raise ReportCrash('42 is true!')

            crash_hound.register_check('42 Checker', check_fn)
        """
        self.check_functions[name] = {
            'check_fn': check_fn,
            'last_notifcation': None,
            'notify_every': notify_every
        }

    def remove_check(self, name):
        """Removes a registered check."""
        if name in self.check_functions:
            del self.check_functions[name]

    def run_checks(self, check_interval=30):
        """Runs checks that are currently registred.

        `check_interval` specifies how often the checks are run.
        The default is every 30 seconds.
        """
        while True:
            for check_name, check_data in self.check_functions.items():
                try:
                    check_data['check_fn']()
                except ReportCrash, e:
                    if self._should_send_notification(check_data):
                        self._send_notification(check_name, str(e))
                        check_data['last_notifcation'] = datetime.utcnow()
                except:
                    self._send_notification(check_name, 'Crash checker crashed!')
                    raise
            time.sleep(check_interval)

    #--- Private ----------------------------------------------
    def _send_notification(self, name, crash_message):
        status = self.sender.send_notification(name, crash_message)
        print 'Sending error report [%s] %s' % (name, crash_message)
        print 'Status: %s' % status
        print '--------'

    def _should_send_notification(self, check_data):
        last_notifcation = check_data.get('last_notifcation')
        if not last_notifcation:
            return True
        else:
            n_ago = datetime.utcnow() - timedelta(seconds=check_data['notify_every'])
            if n_ago > last_notifcation:
                return True
            else:
                return False


class CommonChecks:

    @staticmethod
    def website_check(url):
        code = 'UNKNOWN'

        try:
            fp = urllib.urlopen(url)
            code = fp.getcode()
        except:
            pass

        if code not in [200, 302]:
            raise ReportCrash('Could not open %s. Error code was %s.' % (url, code))
