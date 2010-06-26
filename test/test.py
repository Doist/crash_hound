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
