#!/usr/local/bin/python2.7
# encoding: utf-8
'''
EventAuditReport -- Generate an xMatters event audit report for a date range.
                    
EventAuditReport is a command utility that uses the xMatters REST APIs to
request the event and notification information for the Notification Events
that occurred over a given date range.
The utility first parses the requested range of dates.  If a single date is
given, then all events that occurred on that date and later are retrieved.
If a smaller range is requried, then specify both the start and end date.
Note that the date is actually a timestamp and should contain the time element.

It defines classes_and_methods

@author:     jolin

@copyright:  2017 xMatters, Inc. All rights reserved.

@license:    Apache License 2.0
             http://www.apache.org/licenses/LICENSE-2.0

@contact:    jolin@xmatters.com
@deffield    updated: 2017-01-26
'''

import sys
import os
import json
import requests
# import logging
# import logging.getLogger
import logging.config
from requests.auth import HTTPBasicAuth
from builtins import str
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import Action
import getpass
from datetime import datetime

# Used by command line processor
__all__ = []
__version__ = 0.1
__date__ = '2017-01-26'
__updated__ = '2017-01-26'

# Global Constants
DEBUG = 0
TESTRUN = 0
PROFILE = 0

""" Global Variables
    Defaults are set from configuration file via processArgs()
"""
verbose: int = 0
quiety: bool = False
eventRangeStart: str = ''
eventRangeEnd: str = ''
xmodURL = None
authUser = None
authPassword = None
outDirectory = None
outFilename = None
outFile = None
dirSep = "/"
niceNames = None
basicAuth = None
logger = None
xmGetLimit = 1000
eventPropList = ['eventId', 'id', 'created', 'terminated', 'status',
            'priority', 'incident', 'expirationInMinutes', 'submitter:targetName']

def configure_logger(name: str, log_path: str):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_path,
                'maxBytes': (10*1024*1024),
                'backupCount': 3
            }
        },
        'loggers': {
            'default': {
                'level': 'DEBUG',
                'handlers': ['file']
            }
        },
        'disable_existing_loggers': False
    })
    return logging.getLogger(name)

def logAndExit(url, response):
    global logger
    json = response.json()
    logger.error("Error %d on initial request to %s.\nPlease verify" +\
                 " instance address, user, and password\n",
                 response.status_code, url)
    logger.error("Response - code: %d, reason: %s, message: %s", 
                 json['code'], str(json['reason']), str(json['message']))
    sys.exit()

def createEventOutFile():
    # Create the output file, overwriting existing file if any
    outFile = open(outDirectory + dirSep + 'Events-' + outFilename, 'w')
    return outFile

def writeEventHeader():
    # Write out the header row
    propMax = len(eventPropList) - 1
    i = 0
    for p in eventPropList:
        if (p == 'submitter:targetName'):
            outFile.write('"submitter"')
        else:
            outFile.write('"' + p + '"')
        if (i < propMax):
            outFile.write(',')
        i += 1
    outFile.write('\n')

def writeEvent(anEvent: dict):
    # Write out the header row
    keysMax = len(eventPropList) - 1
    i = 0
    for p in eventPropList:
        if (p == 'submitter:targetName'):
            outFile.write('"' + anEvent['submitter']['targetName'] + '"')
        else:
            outFile.write('"' + anEvent[p] + '"')
        if (i < keysMax):
            outFile.write(',')
        i += 1
    outFile.write('\n')

def getEventDetails(eventId: str) -> dict:
    """ Get the detailed properties for the event defined by eventId.
    """
#    global xmodURL, basicAuth, logger
    
    # Set our resource URI
    url = xmodURL + '/api/xm/1/events/' + eventId
    
    # Get the member
    response = requests.get (url, auth=basicAuth)
    if (response.status_code not in [200,404]):
        logAndExit(url, response)

    # Process the response
    json = response.json()
    eventProperties = {}

    for p in eventPropList:
        if (p == 'eventId'):
            eventProperties['eventId'] = eventId
        elif (response.status_code == 200):
            eventProperties[p] = json[p]
        else:
            eventProperties[p] = "Not Found"

    return eventProperties

def processEvent(eventId: str, includeNotifications: bool):
#    global outFile, logger
    logger.info("Processing Event Id: %s", eventId)
    eventDetails = getEventDetails(eventId)
    writeEvent(eventDetails)

def getEvents(includeNotifications: bool):
    """ Request the list of events from this instance.
        Iterate through the events and if requested, get the
        notifications to be written to the output file.
    """
    global basicAuth, outFile, logger, xmGetLimit, \
            eventRangeStart, eventRangeEnd
    # Create and open the output file, then insert the header row
    outFile = createEventOutFile()
    writeEventHeader()
    
    # Set our resource URLs
    baseURL = xmodURL + '/reapi/2015-01-01/events'
    url = baseURL + '?range=' + eventRangeStart + '/' + eventRangeEnd
    
    # Initialize loop with first request
    cnt = 0
    nEvents = 1
    response = requests.get (url, auth=basicAuth)
    # If the initial response fails, then just terminate the process
    if (response.status_code != 200):
        logAndExit(url, response)

    # Continue until we exhaust the group list
    while (response.status_code == 200):
        
        # Iterate through the result set
        json = response.json()
        nEvents = json['total']
        strNEvents = str(json['total'])
        logger.info ("Retrieved a batch of %d events.", json['total'])
        nextRecordsUrl = json['nextRecordsUrl']
        logger.info ("nextRecordsUrl: %s", json['nextRecordsUrl'])
        for d in json['records']:
            cnt += 1
            logger.info('Processing Event #' + str(cnt) + ' of ' + strNEvents + \
                  ': href="' + d['href'] + '"')
            # Parse off the event id
            eventId = d['href'].split("/")[4]
            processEvent( eventId, includeNotifications )
            
        
        # If there are more groups to get, then request the next page
        if (nextRecordsUrl is None):
            break
        
        logger.info ("Getting next set of events from %s", nextRecordsUrl)
        url = xmodURL + nextRecordsUrl
        response = requests.get (url, auth=basicAuth)
    
    else:
        logger.info ("Retrieved a total of %d from a possible %d events.", 
                     cnt, nEvents)
            
def processEvents(args):
    global logger, verbose, quiet, eventRangeStart, eventRangeEnd
    logger.info('Processing Events: Range start=%s, Range end=%s', args.evStart, args.evEnd)
    getEvents(False)
    return

def processNotifications(args):
    global logger, verbose, quiet, eventRangeStart, eventRangeEnd
    logger.info('Processing Notifications: Range start=%s, Range end=%s', eventRangeStart, args.evEnd)
    getEvents(True)
    return

def processBoth(args):
    global logger, verbose, quiet, eventRangeStart, eventRangeEnd
    logger.info('Processing Events and Notifications: Range start=%s, Range end=%s', args.evStart, eventRangeEnd)
    getEvents(True)
    return

def validate_date(d):
    if (len(d) != 23): return False
    try:
        datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%f')
        return True
    except ValueError:
        return False

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

class Password(Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)

def processCommandLine(argv=None):
    '''Command line options.'''
    global logger, verbose, quiet, eventRangeStart, eventRangeEnd, \
           xmodURL, authUser, authPassword, outDirectory, outFilename, \
           basicAuth, niceNames, dirSep

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # First try to read in the defaults from defaults.json
    cfg = json.load(open('defaults.json'))
    if (cfg['instance'] != ''):
        xmodURL = cfg['instance']
    if (cfg['user'] != ''):
        authUser = cfg['user']
    if (cfg['password'] != ''):
        authPassword = cfg['password']
    if (cfg['nicenames'] != ''):
        niceNames = ((cfg['nicenames'].lower() == "true") or
                     (cfg['nicenames'] == "1"))
    if (cfg['odir'] != ''):
        outDirectory = cfg['odir']
    if (cfg['ofile'] != ''):
        outFilename = cfg['ofile']
    if (cfg['dirsep'] != ''):
        dirSep = cfg['dirsep']
    
    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_doc: str = __import__('__main__').__doc__
    program_shortdesc = program_doc.split("\n")[1]
    program_user_name = (program_doc.split("\n")[13][13:]).strip()
    program_copyright = (program_doc.split("\n")[15][13:]).strip()
    program_license1 = (program_doc.split("\n")[17][13:]).strip()
    program_license2 = (program_doc.split("\n")[18][13:]).strip()
    program_license = '''%s

  Created by %s on %s.
  Copyright %s

  Licensed under the %s
  %s

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, program_user_name, str(__date__), program_copyright,
       program_license1, program_license2)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        subparsers = parser.add_subparsers(dest='commandName')
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", dest="verbose", 
                            action="count", default=0,
                            help="set verbosity level [default: %(default)s]")
        group.add_argument("-q", "--quiet", dest="quiet", 
                            action="store_true", default=False,
                            help="when set limits the amount of output [default: %(default)s]")
        parser.add_argument('-V', '--version', 
                            action='version', version=program_version_message)
        parser.add_argument('-p', action=Password, nargs='?', dest='password',\
                            default=authPassword,
                            help="If not specified in the defaults.json file, use -p to specify a password either on the command line, or be prompted")

        event_parser = subparsers.add_parser('events',description='Outputs just the events in the specified range',help='Use this command in order to create a file containing the details of the events within the specified date range.')
        event_parser.add_argument('evStart',
                            help="Specify the event range start date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-25T10:45:48.011)")
        event_parser.add_argument('evEnd',
                            help="Specify the event range end date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-26T10:45:48.011)")
        event_parser.set_defaults(func=processEvents)
        notif_parser = subparsers.add_parser('notifications',description='Outputs just the notifications in the specified range',help='Use this command in order to create a file containing the details of the notifications for the events within the specified date range.')
        notif_parser.add_argument('evStart',
                            help="Specify the notification range start date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-25T10:45:48.011)")
        notif_parser.add_argument('evEnd',
                            help="Specify the notification range end date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-26T10:45:48.011)")
        notif_parser.set_defaults(func=processNotifications)
        both_parser = subparsers.add_parser('both',description='Outputs the events and notifications in the specified range',help='Use this command in order to create a file containing the details of the events and notifications within the specified date range.')
        both_parser.add_argument('evStart',
                            help="Specify the event and notification range start date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-25T10:45:48.011)")
        both_parser.add_argument('evEnd',
                            help="Specify the event and notification range end date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-26T10:45:48.011)")        
        both_parser.set_defaults(func=processBoth)
        
        # Process arguments
        logger.info('Before parser.parse_args()')
        args = parser.parse_args()
        logger.info('After parser.parse_args(), commandName=%s', args.commandName)

        # Dereference the arguments
        verbose = args.verbose
        quiet = args.quiet
        eventRangeStart = args.evStart
        eventRangeEnd = args.evEnd

        # Validate the format for date and times is correct
        if (not validate_date(eventRangeStart)):
            errStr = "Invalid Event Range Start Date (evStart=%s). "\
            "Expecting an ISO 8601 formatted value: yyyy-MM-dd'T'HH:mm:ssZ "\
            "(e.g. 2017-01-25T10:45:48.011)"\
                             %(eventRangeStart)
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-2)
        if (not validate_date(eventRangeEnd)):
            errStr = "Invalid Event Range End Date (evEnd=%s). "\
            "Expecting an ISO 8601 formatted value: yyyy-MM-dd'T'HH:mm:ssZ "\
            "(e.g. 2017-01-25T10:45:48.011)"\
                             %(eventRangeEnd)
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-3)

        # Setup the basic auth object for subsequent REST calls
        basicAuth = HTTPBasicAuth(authUser, authPassword)

        return args
    
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        sys.exit(0)
    
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        logger.error(program_name + ": " + repr(e))
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        sys.exit(-1)

def main(argv=None): # IGNORE:C0111
    global verbose, queit, logger, dirSep, \
           outFile, outDirectory, outFilename

    # Initialize logging
    logger = configure_logger('default', 'EventAuditReport.log')
    logger.info('EventAuditReport Started.')
    
    # Process commandline arguments
    args = processCommandLine(argv)
    logger.debug('before args.func(args)')

    args.func(args)
    logger.debug('after args.func(args)')
    
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
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