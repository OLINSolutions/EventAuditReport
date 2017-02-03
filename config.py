# -*- coding: utf-8 -*-
"""Holds variables shared between modules

@author:     jolin

@copyright:  2017 xMatters, Inc. All rights reserved.

@license:    Apache License 2.0
             http://www.apache.org/licenses/LICENSE-2.0

@contact:    jolin@xmatters.com
@deffield    updated: 2017-01-28

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

# Used by command line processor
version = 0.1
date = '2017-01-28'
updated = '2017-01-28'

# Global Constants
DEBUG = 0
TESTRUN = 0
PROFILE = 0

""" Global Variables
    Defaults are set from configuration file via processArgs()
"""
program_name = None
event_range_start: str = None
event_range_end: str = None
xmod_url = None
out_directory = None
events_filename = None
log_filename = None
notifs_filename = None
events_file = None
notifs_file = None
dir_sep = "/"
basic_auth = None
verbosity = 0
noisy = False

# Error codes
ERR_CLI_EXCEPTION = -1
ERR_CLI_MISSING_DEFAULTS_CODE = -2
ERR_CLI_MISSING_DEFAULTS_MSG = "Missing defaults file: "
ERR_CLI_MISSING_XMOD_URL_CODE = -3
ERR_CLI_MISSING_XMOD_URL_MSG = ("xMatters URL was not specified on the command"
                                " line or via defaults")
ERR_CLI_MISSING_USER_CODE = -4
ERR_CLI_MISSING_USER_MSG = ("xMatters User was not specified on the command "
                            "line or via defaults")
ERR_CLI_MISSING_PASSWORD_CODE = -5
ERR_CLI_MISSING_PASSWORD_MSG = ("xMatters Password was not specified on the "
                                "command line or via defaults")
ERR_CLI_MISSING_OUTPUT_DIR_CODE = -6
ERR_CLI_MISSING_OUTPUT_DIR_MSG = ("Output directory was not specified on the "
                                  "command line or via defaults")
ERR_CLI_MISSING_EVENTS_FILENAME_CODE = -7
ERR_CLI_MISSING_EVENTS_FILENAME_MSG = ("Event output filename was not specified"
                                       " on the command line or via defaults")
ERR_CLI_MISSING_NOTIFS_FILENAME_CODE = -8
ERR_CLI_MISSING_NOTIFS_FILENAME_MSG = ("Notifications output filename was not "
                                       "specified on the command line or via "
                                       "defaults")
ERR_CLI_INVALID_START_DATE_CODE = -9
ERR_CLI_INVALID_START_DATE_MSG = ("Invalid Event Range Start Date (evStart=%s)."
                                  " Expecting an ISO 8601 formatted value: "
                                  "yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-25T10:"
                                  "45:48.011), but found: ")
ERR_CLI_INVALID_END_DATE_CODE = -10
ERR_CLI_INVALID_END_DATE_MSG = ("Invalid Event Range End Date (evStart=%s)."
                                "Expecting an ISO 8601 formatted value: "
                                "yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-25T10:"
                                "45:48.011), but found: ")
ERR_REQUEST_EXCEPCTION_CODE = -11
ERR_REQUEST_EXCEPTION_MSG = ("Request Exception while trying to GET %s\n"
                             "Exception: %s")
ERR_REQUEST_NEXT_EXCEPCTION_CODE = -12
ERR_INITIAL_REQUEST_FAILED_CODE = -13
ERR_INITIAL_REQUEST_FAILED_MSG = ("Error %d on initial request to %s.\nPlease "
                                  "verify instance address, user, and password")

def main():
    pass

if __name__ == '__main__':
    main()
