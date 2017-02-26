#!/usr/bin/env python3
# encoding: utf-8
"""Generate an xMatters event audit report for a date range.
                    
event_audit_report is a command utility that uses the xMatters REST APIs to
request the event and notification information for the Notification Events
that occurred over a given date range.
The utility first parses the requested range of dates.  If a single date is
given, then all events that occurred on that date and later are retrieved.
If a smaller range is requried, then specify both the start and end date.
Note that the date is actually a timestamp and should contain the time element.

@author:     jolin

@copyright:  2017 xMatters, Inc. All rights reserved.

@license:    Apache License 2.0
             http://www.apache.org/licenses/LICENSE-2.0

@contact:    jolin@xmatters.com
@deffield    updated: 2017-01-28

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import sys

import config
import ear_logger
import cli

# sys.path.append('.')

__all__ = []
__version__ = config.version
__date__ = config.date
__updated__ = config.updated


def main(argv=None):  # IGNORE:C0111

    args = cli.process_command_line(argv, __doc__)
    
    # Get local logger (must wait until after process_command_line runs)
    logger = ear_logger.get_logger()

    logger.debug('before args.func(args)')
    args.func(args)
    logger.debug('after args.func(args)')
    
if __name__ == "__main__":
    if config.DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
    if config.TESTRUN:
        import doctest
        doctest.testmod()
    if config.PROFILE:
        import cProfile
        import pstats
        profile_filename = 'EventAuditReport_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
