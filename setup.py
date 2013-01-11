#!/usr/bin/env python
# Copyright (c) 2007 Qtrac Ltd. All rights reserved.
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

import os

from setuptools import setup

setup(name='crash_hound',
      version = '2.2',
      author="amix",
      author_email="amix@amix.dk",
      url="http://www.amix.dk/",
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      packages=['crash_hound', 'test'],
      platforms=["Any"],
      license="BSD",
      keywords='tropo crash hound notification sms crash reports monitoring',
      description="Monitor anything and get notifications directly on your iPhone",
      long_description="""\
crash_hound
---------------

Crash Hound lets you script monitoring and lets you receive notifications directly on your mobile phone.

It works via Tropo and a http://tropo.com acocunt is required.

For more information check out:

 * http://amix.dk/blog/post/19637#Monitor-anything-and-get-SMS-notifications
 * http://amix.dk/blog/post/19625#International-SMS-messaging-The-cheap-way

To install it do following:

    sudo easy_install crash_hound

Examples
----------

Registers::

    from crash_hound import CrashHound, ReportCrash, CommonChecks, SenderTropo

    def check_fn():
        if 42:
            raise ReportCrash('42 is true!')
        else:
            pass #Ignore

    crash_sender = SenderTropo('YOUR TROPO.COM API KEY',
                               '+56 ... YOUR MOBILE NUMBER ...')

    crash_checker = CrashHound(crash_sender)

    crash_checker.register_check('42 Checker',
                                 check_fn,
                                 notify_every=60)

    crash_checker.register_check('Google.com Blah test',
                                 lambda: CommonChecks.website_check('http://google.com/blah'),
                                 notify_every=60)

    crash_checker.run_checks(check_interval=10)

Copyright: 2011 by amix
License: BSD.""")
