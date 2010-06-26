Monitor anything and get notifications directly on your iPhone
===========================================

Crash Hound lets you script monitoring and lets you receive notifications directly on your iPhone (for free!).

It works via http://notifo.com and a notifo.com account is required.

For more information check out http://amix.dk/blog/post/19526#Crash-Hound-scriptable-monitoring-and-free-phone-notifications
    
To install it do following:

    sudo easy_install notifo
    sudo easy_install crash_hound


Examples
========

Example of list wrapper:

    from crash_hound import CrashHound, ReportCrash, CommonChecks

    def check_fn():
        if 42:
            raise ReportCrash('42 is true!')
        else:
            pass #Ignore


    crash_checker = CrashHound(YOUR_USERNAME,
                               YOUR_API_TOKEN)

    crash_checker.register_check('42 Checker',
                                 check_fn,
                                 notify_every=60)

    crash_checker.register_check('Google.com Blah test',
                                 lambda: CommonChecks.website_check('http://google.com/blah'),
                                 notify_every=60)

    crash_checker.run_checks(check_interval=10)
