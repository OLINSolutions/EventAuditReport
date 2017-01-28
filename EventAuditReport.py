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
@deffield    updated: 2017-01-28
'''

import sys
import os
import time
import json
import pprint
import requests
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
__date__ = '2017-01-28'
__updated__ = '2017-01-28'

# Global Constants
DEBUG = 0
TESTRUN = 0
PROFILE = 0

""" Global Variables
    Defaults are set from configuration file via processArgs()
"""
eventRangeStart: str = ''
eventRangeEnd: str = ''
xmodURL = None
authUser = None
authPassword = None
outDirectory = None
eventFilename = None
notifFilename = None
eventFile = None
notifFile = None
dirSep = "/"
basicAuth = None
logger = None
xmGetLimit = 1000
eventPropList = ['eventId', 'created', 'terminated', 'submitter.targetName', 
                 'status', 'priority', 'incident', 
                 'recipients.total', 'recipients.count',
                 'recipients:recipientType|targetName|status',
                 'responseOptions.total', 'responseOptions.count', 
                 'responseOptions:number|text|action|contribution', 
                 'expirationInMinutes', 'id', 'form.id'
                ]

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
    body = response.json()
    logger.error("Error %d on initial request to %s.\nPlease verify" +\
                 " instance address, user, and password\n",
                 response.status_code, url)
    logger.error("Response - code: %d, reason: %s, message: %s", 
                 body['code'], str(body['reason']), str(body['message']))
    sys.exit()

def createEventOutFile():
    # Create the output file, overwriting existing file if any
    outFile = open(outDirectory + dirSep + eventFilename, 'w')
    return outFile

def writeEventHeader():
    # Write out the event header row
    eventFile.write(','.join(['"' + p + '"' for p in eventPropList]))
    eventFile.write('\n')

def writeEvent(anEvent: dict):
    # Write out the event details
    eventFile.write(','.join(['"' + \
        str(anEvent[p if (':' not in p) else p.split(':')[0]]) + '"' \
        for p in eventPropList]))
    eventFile.write('\n')

def getEventDetails(eventId: str) -> dict:
    """ Get the detailed properties for the event defined by eventId.
    """
    # Set our resource URI
    url = xmodURL + '/api/xm/1/events/' + eventId
    
    # Get the member
    response = requests.get (url, auth=basicAuth)
    if (response.status_code not in [200,404]):
        logAndExit(url, response)

    # Process the response
    body = response.json()
    logger.debug("Event %s - json body: %s", eventId, pprint.pformat(body))
    eventProperties = {}

    for p in eventPropList:
        propName = p if (':' not in p) else p.split(':')[0]
        eventProperties[propName] = "N/A"

        if (p == 'eventId'):
            eventProperties['eventId'] = eventId
        elif (response.status_code == 200):
            if ('.' in p):
                pParts = p.split('.')
                if pParts[0] in body:
                    eventProperties[p] = body[pParts[0]][pParts[1]]
            elif ':' in p:
                pParts = p.split(':')
                if pParts[0] in body:
                    pData = body[pParts[0]]['data']
                    pNames = pParts[1].split('|')
                    eventProperties[pParts[0]] = ','.join([ \
                        '|'.join([str(aProp[pName] if aProp[pName] is not None else "") for pName in pNames]) \
                        for aProp in pData \
                        ])
            else:
                if p in body:
                    eventProperties[p] = body[p]
                
    return eventProperties

def processEvent(eventId: str, includeNotifications: bool):
    logger.info("Processing Event Id: %s", eventId)
    eventDetails = getEventDetails(eventId)
    writeEvent(eventDetails)

def getEvents(includeNotifications: bool):
    """ Request the list of events from this instance.
        Iterate through the events and if requested, get the
        notifications to be written to the output file.
    """
    global eventFile

    # Create and open the output file, then insert the header row
    eventFile = createEventOutFile()
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
        body = response.json()
        nEvents = body['total']
        logger.info ("Retrieved a batch of %d events.", body['total'])
        nextRecordsUrl = body['nextRecordsUrl']
        logger.debug ("nextRecordsUrl: %s", body['nextRecordsUrl'])
        for d in body['records']:
            cnt += 1
            logger.info('Processing Event #%d of %d: href="%s"', \
                  cnt, body['total'], d['href'])
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
    logger.info('Processing Events: Range start=%s, Range end=%s', args.evStart, args.evEnd)
    getEvents(False)
    return

def processAll(args):
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
           xmodURL, authUser, authPassword, outDirectory, eventFilename, \
           notifFilename, basicAuth, dirSep

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

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
        parser.add_argument("-d", "--defaults", dest="dFile", 
                            default="defaults.json",
                            help="Specifes the name of the file containing default settings [default: %(default)s]")
        parser.add_argument("-e", "--efile", dest="eFile", 
                            default=None,
                            help="If not specified in the defaults file, use -e to specify the base name of the file that will contain event information.  The name will have a timestamp and .csv appended to the end. [default: %(default)s]")
        parser.add_argument("-l", "--lfile", dest="lFile", 
                            default=None,
                            help="If not specified in the defaults file, use -l to specify the base name of the log file.  The name will have a timestamp and .log appended to the end.")
        parser.add_argument("-n", "--nfile", dest="nFile", 
                            default=None,
                            help="If not specified in the defaults file, use -n to specify the base name of the file that will contain notification information.  The name will have a timestamp and .csv appended to the end. [default: %(default)s]")
        parser.add_argument("-o", "--odir", dest="oDir", 
                            default=None,
                            help="If not specified in the defaults file, use -o to specify the file system location where the output files will be written.")
        parser.add_argument('-p', action=Password, nargs='?', dest='password',\
                            default=None,
                            help="If not specified in the defaults file, use -p to specify a password either on the command line, or be prompted")
        parser.add_argument("-u", "--user", dest="user", 
                            default=None,
                            help="If not specified in the defaults file, use -u to specify the xMatters user id that has permissions to get Event and Notification data.")
        parser.add_argument("-x", "--xmurl", dest="xmurl", 
                            default=None,
                            help='If not specified in the defaults file, use -i to specify the base URL of your xMatters instance.  For example, "https://myco.hosted.xmatters.com" wihtout quotes.')

        event_parser = subparsers.add_parser('events',description='Outputs just the events in the specified range',help='Use this command in order to create a file containing the details of the events within the specified date range.')
        event_parser.add_argument('evStart',
                            help="Specify the event range start date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-25T10:45:48.011)")
        event_parser.add_argument('evEnd',
                            help="Specify the event range end date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-26T10:45:48.011)")
        event_parser.set_defaults(func=processEvents)
        all_parser = subparsers.add_parser('all',description='Outputs the events and notifications in the specified range',help='Use this command in order to create a file containing the details of the events and notifications within the specified date range.')
        all_parser.add_argument('evStart',
                            help="Specify the event and notification range start date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-25T10:45:48.011)")
        all_parser.add_argument('evEnd',
                            help="Specify the event and notification range end date/time in ISO 8601 \
                            format: yyyy-MM-dd'T'HH:mm:ssZ (e.g. 2017-01-26T10:45:48.011)")        
        all_parser.set_defaults(func=processAll)
        
        # Process arguments
        args = parser.parse_args()

        # Dereference the arguments
        logFilename = None
        if (args.eFile is not None): eventFilename = args.eFile
        if (args.lFile is not None): logFilename = args.lFile
        if (args.nFile is not None): notifFilename = args.nFile
        if (args.oDir is not None): outDirectory = args.oDir
        if (args.password is not None): authPassword = args.password
        if (args.user is not None): authUser = args.user
        if (args.xmurl is not None): xmodURL = args.xmurl
        eventRangeStart = args.evStart
        eventRangeEnd = args.evEnd

        # Try to read in the defaults from defaults.json
        cfg = json.load(open(args.dFile))
        if (authUser is None) and (cfg['user'] != ''):
            authUser = cfg['user']
        if (authPassword is None) and (cfg['password'] != ''):
            authPassword = cfg['password']
        if (dirSep is None) and (cfg['dirsep'] != ''):
            dirSep = cfg['dirsep']
        if (eventFilename is None) and (cfg['efile'] != ''):
            eventFilename = cfg['efile']
        if (logFilename is None) and (cfg['lfile'] != ''):
            logFilename = cfg['lfile']
        if (notifFilename is None) and (cfg['nfile'] != ''):
            notifFilename = cfg['nfile']
        if (outDirectory is None) and (cfg['odir'] != ''):
            outDirectory = cfg['odir']
        if (xmodURL is None) and (cfg['xmurl'] != ''):
            xmodURL = cfg['xmurl']

        # Fix file names        
        timeStr = time.strftime("-%Y%m%d-%H%M")
        if (eventFilename is not None):
            eventFilename = outDirectory + dirSep + eventFilename + timeStr + '.csv'
        if (logFilename is not None):
            logFilename = outDirectory + dirSep + logFilename + timeStr + '.log'
        if (notifFilename is not None):
            notifFilename = outDirectory + dirSep + notifFilename + timeStr + '.csv'
        
        # Initialize logging
        logger = configure_logger('default', logFilename)
        logger.info('EventAuditReport Started.')
        logger.info('After parser.parse_args(), commandName=%s', args.commandName)

        # Final verification of arguments
        if (xmodURL is None):
            errStr = "xMatters URL was not specified on the command line or via defaults"
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-2)
        else:
            logger.info ('xMatters Instance URL is: %s', xmodURL)
        if (authUser is None):
            errStr = "xMatters User was not specified on the command line or via defaults"
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-3)
        else:
            logger.info ('User is: %s', authUser)
        if (authPassword is None):
            errStr = "xMatters Password was not specified on the command line or via defaults"
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-4)
        else:
            logger.info ('Password len is: %d', len(authPassword))
        if (outDirectory is None):
            errStr = "Output directory was not specified on the command line or via defaults"
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-5)
        else:
            logger.info ('Output directory is: %s', outDirectory)
        if (eventFilename is None):
            errStr = "Event output filename was not specified on the command line or via defaults"
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-6)
        else:
            logger.info ('Event output filename is: %s', eventFilename)
        if (notifFilename is None):
            errStr = "Notification output filename was not specified on the command line or via defaults"
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-7)
        else:
            logger.info ('Notification output filename is: %s', notifFilename)
        
        # Validate the format for date and times is correct
        if (not validate_date(eventRangeStart)):
            errStr = "Invalid Event Range Start Date (evStart=%s). "\
            "Expecting an ISO 8601 formatted value: yyyy-MM-dd'T'HH:mm:ssZ "\
            "(e.g. 2017-01-25T10:45:48.011)"\
                             %(eventRangeStart)
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-8)
        if (not validate_date(eventRangeEnd)):
            errStr = "Invalid Event Range End Date (evEnd=%s). "\
            "Expecting an ISO 8601 formatted value: yyyy-MM-dd'T'HH:mm:ssZ "\
            "(e.g. 2017-01-25T10:45:48.011)"\
                             %(eventRangeEnd)
            logger.error(errStr)
            sys.stderr.write("\n%s\n\n"\
                             %(errStr) + parser.format_help())
            sys.exit(-9)

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