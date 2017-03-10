"""Command line and argument processor

.. _Following Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.htm
"""

import sys
import time
import json
import argparse
import getpass
from datetime import datetime

from requests import auth

import config
import ear_logger
import event_processor


def process_events(args):
    """Called when command line specifies a specific event range"""
    ear_logger.get_logger().info(
        'Processing Events only: Range start=%s, Range end=%s',
        args.start, args.end)
    event_processor.get_events(False)
    return


def process_all(args):
    """Called when command line specifies all events"""
    ear_logger.get_logger().info(
        'Processing Events and Notifications: Range start=%s, Range end=%s',
        args.start, args.end)
    event_processor.get_events(True)
    return


def __validate_date(test_date):
    """Make sure date is in ISO 8601"""
    if len(test_date) != 23:
        return False
    try:
        datetime.strptime(test_date, '%Y-%m-%dT%H:%M:%S.%f')
        return True
    except ValueError:
        return False


class _CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""
    def __init__(self, msg, rc=config.ERR_CLI_EXCEPTION):
        super(_CLIError).__init__(type(self))
        self.result_code = rc
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg

class __Password(argparse.Action):
    """Container to get and/or hold incoming password"""
    def __call__(self, parser, namespace, values, option_string): # pylint: disable=signature-differs
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)

def process_command_line(argv=None, prog_doc=''): # pylint: disable=too-many-branches,too-many-statements
    """Evaluates and responds to passed in command line arguments"""
    logger = None

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_version_message = '%%(prog)s %s (%s)' % (
        "v%s" % config.VERSION, config.UPDATED)
    program_license = """%s

  Created by %s on %s.
  Copyright %s

  Licensed under the %s
  %s

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
""" % (prog_doc.split("\n")[1], config.AUTHOR, config.DATE,
       config.COPYRIGHT, config.LICENSE, config.LICENSE_REF)

    try:
        # Setup argument parser
        parser = argparse.ArgumentParser(
            description=program_license,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        subparsers = parser.add_subparsers(dest='command_name')
        # Add common arguments
        parser.add_argument('-V', '--version',
                            action='version', version=program_version_message)
        parser.add_argument("-v", dest="verbose",
                            action="count", default=0,
                            help=(
                                "set verbosity level.  Each occurrence of v "
                                "increases the logging level.  By default it "
                                "is ERRORs only, a single v (-v) means add "
                                "WARNING logging, a double v (-vv) means add "
                                "INFO logging, and a tripple v (-vvv) means "
                                "add DEBUG logging [default: %(default)s]"))
        parser.add_argument("-c", "--console", dest="noisy",
                            action='store_true',
                            help=(
                                "If specified, will echo all log output to "
                                "the console at the requested verbosity based "
                                "on the -v option"))
        parser.add_argument("-d", "--defaults", dest="defaults_filename",
                            default="defaults.json",
                            help=(
                                "Specifes the name of the file containing "
                                "default settings [default: %(default)s]"))
        parser.add_argument("-e", "--efile", dest="events_filename",
                            default=None,
                            help=(
                                "If not specified in the defaults file, use "
                                "-e to specify the base name of the file that "
                                "will contain event information.  The name "
                                "will have a timestamp and .csv appended to "
                                "the end. [default: %(default)s]"))
        parser.add_argument("-l", "--lfile", dest="log_filename",
                            default=None,
                            help=(
                                "If not specified in the defaults file, use "
                                "-l to specify the base name of the log file. "
                                "The name will have a timestamp and .log "
                                "appended to the end."))
        parser.add_argument("-n", "--nfile", dest="notifs_filename",
                            default=None,
                            help=(
                                "If not specified in the defaults file, use -n"
                                " to specify the base name of the file that "
                                "will contain notification information.  The "
                                "name will have a timestamp and .csv appended "
                                "to the end. [default: %(default)s]"))
        parser.add_argument("-o", "--odir", dest="out_directory",
                            default=None,
                            help=(
                                "If not specified in the defaults file, use -o"
                                " to specify the file system location where "
                                "the output files will be written."))
        parser.add_argument('-p', action=__Password, nargs='?',
                            dest='password', default=None,
                            help=(
                                "If not specified in the defaults file, use -p"
                                " to specify a password either on the command"
                                " line, or be prompted"))
        parser.add_argument("-u", "--user", dest="user",
                            default=None,
                            help=("If not specified in the defaults file, use "
                                  "-u to specify the xmatters user id that has"
                                  " permissions to get Event and Notification "
                                  "data."))
        parser.add_argument("-x", "--xmodurl", dest="xmod_url",
                            default=None,
                            help=("If not specified in the defaults file, use "
                                  "-i to specify the base URL of your xmatters"
                                  " instance.  For example, 'https://myco.host"
                                  "ed.xmatters.com' without quotes."))
        #Add in event command parsers
        event_parser = subparsers.add_parser(
            'events', description=("Outputs just the events in the specified "
                                   "range"),
            help=("Use this command in order to create a file containing the "
                  "details of the events within the specified date range."))
        event_parser.add_argument(
            'start', help=("Specify the event range start date/time in ISO "
                           "8601 format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-"
                           "01-25T10:45:48.011)"))
        event_parser.add_argument(
            'end', help=("Specify the event range end date/time in ISO 8601 "
                         "format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-26T"
                         "10:45:48.011)"))
        event_parser.set_defaults(func=process_events)
        all_parser = subparsers.add_parser(
            'all', description=("Outputs the events and notifications in the "
                                "specified range"),
            help=("Use this command in order to create a file containing the "
                  "details of the events and notifications within the "
                  "specified date range."))
        all_parser.add_argument(
            'start', help=("Specify the event range start date/time in ISO "
                           "8601 format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-"
                           "01-25T10:45:48.011)"))
        all_parser.add_argument(
            'end', help=("Specify the event range end date/time in ISO 8601 "
                         "format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-26T"
                         "10:45:48.011)"))
        all_parser.set_defaults(func=process_all)

        # Process arguments
        args = parser.parse_args()

        # Dereference the arguments into the configuration object
        user = None
        password = None
        if args.events_filename:
            config.events_filename = args.events_filename
        if args.log_filename:
            config.log_filename = args.lFilog_filenamele
        if args.notifs_filename:
            config.notifs_filename = args.notifs_filename
        if args.out_directory:
            config.out_directory = args.out_directory
        if args.noisy > 0:
            config.noisy = args.noisy
        if args.password:
            password = args.password
        if args.user:
            user = args.user
        if args.verbose > 0:
            config.verbosity = args.verbose
        if args.xmod_url:
            config.xmod_url = args.xmod_url
        config.event_range_start = args.start
        config.event_range_end = args.end

        # Try to read in the defaults from defaults.json
        try:
            with open(args.defaults_filename) as defaults:
                cfg = json.load(defaults)
        except FileNotFoundError:
            raise(_CLIError(
                config.ERR_CLI_MISSING_DEFAULTS_MSG % args.defaults_filename,
                config.ERR_CLI_MISSING_DEFAULTS_CODE))

        # Process the defaults
        if user is None and 'user' in cfg:
            user = cfg['user']
        if password is None and 'password' in cfg:
            password = cfg['password']
        if config.dir_sep is None and 'dirSep' in cfg:
            config.dir_sep = cfg['dirSep']
        if config.events_filename is None and 'eventsFilename' in cfg:
            config.events_filename = cfg['eventsFilename']
        if config.log_filename is None and 'logFilename' in cfg:
            config.log_filename = cfg['logFilename']
        if config.notifs_filename is None and 'notifsFilename' in cfg:
            config.notifs_filename = cfg['notifsFilename']
        if config.out_directory is None and 'outDirectory' in cfg:
            config.out_directory = cfg['outDirectory']
        if config.xmod_url is None and 'xmodURL' in cfg:
            config.xmod_url = cfg['xmodURL']
        if config.verbosity == 0 and 'verbosity' in cfg:
            if cfg['verbosity'] in [1, 2, 3]:
                config.verbosity = cfg['verbosity']

        # Fix file names
        time_str = time.strftime("-%Y%m%d-%H%M")
        if config.events_filename:
            config.events_filename = (
                config.out_directory + config.dir_sep +
                config.events_filename + time_str + '.csv')
        if config.log_filename:
            config.log_filename = (
                config.out_directory + config.dir_sep +
                config.log_filename + time_str + '.log')
        if config.notifs_filename:
            config.notifs_filename = (
                config.out_directory + config.dir_sep +
                config.notifs_filename + time_str + '.csv')

        # Initialize logging
        logger = ear_logger.get_logger()
        logger.info("event_audit_report Started.")
        logger.info("After parser.parse_args(), command_name=%s",
                    args.command_name)

        # Final verification of arguments
        if config.xmod_url:
            logger.info("xmatters Instance URL is: %s", config.xmod_url)
        else:
            raise(_CLIError(config.ERR_CLI_MISSING_XMOD_URL_MSG,
                            config.ERR_CLI_MISSING_XMOD_URL_CODE))
        if user:
            logger.info("User is: %s", user)
        else:
            raise(_CLIError(config.ERR_CLI_MISSING_USER_MSG,
                            config.ERR_CLI_MISSING_USER_CODE))
        if password:
            logger.info("Password was provided.")
        else:
            raise(_CLIError(config.ERR_CLI_MISSING_PASSWORD_MSG,
                            config.ERR_CLI_MISSING_PASSWORD_CODE))
        if config.out_directory:
            logger.info("Output directory is: %s", config.out_directory)
        else:
            raise(_CLIError(config.ERR_CLI_MISSING_OUTPUT_DIR_MSG,
                            config.ERR_CLI_MISSING_OUTPUT_DIR_CODE))
        if config.events_filename:
            logger.info("Events output filename is: %s",
                        config.events_filename)
        else:
            raise(_CLIError(config.ERR_CLI_MISSING_EVENTS_FILENAME_MSG,
                            config.ERR_CLI_MISSING_EVENTS_FILENAME_CODE))
        if config.notifs_filename:
            logger.info("Notifications output filename is: %s",
                        config.notifs_filename)
        else:
            raise(_CLIError(config.ERR_CLI_MISSING_NOTIFS_FILENAME_MSG,
                            config.ERR_CLI_MISSING_NOTIFS_FILENAME_CODE))

        # Validate the format for date and times is correct
        if not __validate_date(config.event_range_start):
            raise(_CLIError(
                config.ERR_CLI_INVALID_START_DATE_MSG%(
                    config.event_range_start),
                config.ERR_CLI_INVALID_START_DATE_CODE))
        if not __validate_date(config.event_range_end):
            raise(_CLIError(
                config.ERR_CLI_INVALID_START_DATE_MSG%(config.event_range_end),
                config.ERR_CLI_INVALID_START_DATE_CODE))

        # Setup the basic auth object for subsequent REST calls
        config.basic_auth = auth.HTTPBasicAuth(user, password)

        return args

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        sys.exit(0)

    except _CLIError as cli_except:
        if config.DEBUG or config.TESTRUN:
            raise cli_except # pylint: disable=raising-bad-type
        msg = config.program_name + ": " + repr(cli_except) + "\n"
        if logger:
            logger.error(msg)
        sys.stderr.write(msg)
        indent = len(config.program_name) * " "
        sys.stderr.write(indent + "  for help use --help")
        sys.exit(cli_except.rc)

    except Exception as exc: # pylint: disable=broad-except
        if config.DEBUG or config.TESTRUN:
            raise exc # pylint: disable=raising-bad-type
        sys.stderr.write(
            config.program_name + ": Unexpected exception " + repr(exc) + "\n")
        indent = len(config.program_name) * " "
        sys.stderr.write(indent + "  for help use --help")
        sys.exit(config.ERR_CLI_EXCEPTION)

def main():
    """ By convention and for completeness """
    pass

if __name__ == '__main__':
    main()
