#!/usr/bin/env python3
# encoding: utf-8
"""Generate an xmatters event audit report for a date range.

event_audit_report is a command utility that uses the xmatters REST APIs to
request the event and notification information for the Notification Events
that occurred over a given date range.
The utility first parses the requested range of dates.  If a single date is
given, then all events that occurred on that date and later are retrieved.
If a smaller range is requried, then specify both the start and end date.
Note that the date is actually a timestamp and should contain the time element.

Example:
    Arguments are described via the -H command
    Here are some examples::

        $ python3 event_audit_report.py -vv -c -d defaults.json events
            2017-01-27T16:15:00.000 2017-01-27T16:30:00.000

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import sys

import config
import cli

__all__ = []
__version__ = config.VERSION
__date__ = config.DATE
__updated__ = config.UPDATED

def main(argv=None):
    """ Begins the Event Audit Report process """

    args = cli.process_command_line(argv, __doc__)
    args.func(args)

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
