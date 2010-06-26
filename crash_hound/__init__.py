import time
import urllib
import notifo

from datetime import datetime, timedelta


class ReportCrash(Exception): pass


class CrashHound:

    def __init__(self, api_user, api_token):
        self.check_functions = {}
        self.api_user = api_user
        self.api_token = api_token

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
        notifo.send_notification(
            self.api_user,
            self.api_token,
            to=self.api_user,
            title=name,
            msg=crash_message,
            label='CrashHound'
        )

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
