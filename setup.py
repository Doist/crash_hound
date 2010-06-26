#!/usr/bin/env python
# Copyright (c) 2007 Qtrac Ltd. All rights reserved.
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

import os
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(name='crash_hound',
      version = '1.0',
      author="amix",
      author_email="amix@amix.dk",
      url="http://www.amix.dk/",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      packages=['crash_hound', 'test'],
      platforms=["Any"],
      license="BSD",
      keywords='notifo crash hound notification sms crash reports monitoring',
      description="Monitor anything and get notifications directly on your iPhone",
      long_description="""\
crash_hound
---------------

Crash Hound lets you script monitoring and lets you receive notifications directly on your iPhone (for free!).

It works via notifo.com and a notifo.com account is required.

For more information check out:
http://amix.dk/blog/post/19526#Crash-Hound-scriptable-monitoring-and-free-phone-notifications

Examples
----------

Registers::

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

Copyright: 2010 by amix
License: BSD.""")
