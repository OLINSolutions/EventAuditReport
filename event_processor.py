'''
Created on Jan 28, 2017

@author: jolin
'''

import sys
import pprint
import requests
import config
import ear_logger

_logger = None

_event_prop_list = [
    'eventId', 'created', 'terminated', 'submitter.targetName', 'status',
    'priority', 'incident', 'recipients.total', 'recipients.count',
    'recipients:recipientType|targetName|status', 'responseOptions.total',
    'responseOptions.count', 'responseOptions:number|text|action|contribution',
    'expirationInMinutes', 'id', 'form.id'
]

def _log_and_exit(url, response, event_file):
    body = response.json()
    _logger.error(config.ERR_INITIAL_REQUEST_FAILED_MSG,
                  response.status_code, url)
    _logger.error("Response - code: %s, reason: %s, message: %s", 
                  str(body['code']) if 'code' in body else "none",
                  str(body['reason']) if 'reason' in body else "none", 
                  str(body['message']) if 'message' in body else "none")
    event_file.close()
    sys.exit(config.ERR_INITIAL_REQUEST_FAILED_CODE)

def _create_event_out_file(event_filename):
    outFile = open(event_filename, 'w')
    return outFile

def _write_event_header(event_file):
    event_file.write(','.join(['"' + p + '"' for p in _event_prop_list]))
    event_file.write('\n')

def _write_event(event_file, event: dict):
    event_file.write(
        ','.join(
            [
                '"' + str(event[p if ':' not in p else p.split(':')[0]]) + '"' 
                for p in _event_prop_list
            ]
        ))
    event_file.write('\n')

def _get_event_details(event_id: str, event_file) -> dict:
    """Get the detailed properties for the event defined by event_id."""

    # Set our resource URI
    url = config.xmod_url + '/api/xm/1/events/' + event_id
    
    # Get the member
    response = requests.get(url, auth=config.basic_auth)
    if response.status_code not in [200,404]:
        _log_and_exit(url, response, event_file)

    # Process the response
    body = response.json()
    _logger.debug("Event %s - json body: %s", event_id, pprint.pformat(body))
    event_properties = {}

    for prop_key in _event_prop_list:
        prop_name = prop_key if ':' not in prop_key else prop_key.split(':')[0]
        event_properties[prop_name] = "N/A"

        if prop_key == 'event_id':
            event_properties['event_id'] = event_id
        elif response.status_code == 200:
            if '.' in prop_key:
                #dot notation means a reference to a sub-element
                pk_parts = prop_key.split('.')
                if pk_parts[0] in body:
                    event_properties[prop_key] = body[pk_parts[0]][pk_parts[1]]
            elif ':' in prop_key:
                #colon notation is a reference to a list of sub-elements
                pk_parts = prop_key.split(':')
                if pk_parts[0] in body:
                    list_data = body[pk_parts[0]]['data']
                    item_names = pk_parts[1].split('|')
                    #tupples are separated by commas, values by pipe (|)
                    event_properties[pk_parts[0]] = ','.join(
                        [
                        '|'.join([
                                str(el[item] if item in el else "") 
                                for item in item_names
                                ]) 
                        for el in list_data 
                        ])
            else:
                if prop_key in body:
                    event_properties[prop_key] = body[prop_key]
                
    return event_properties

def _process_event(event_file, event_id: str, include_notifs: bool):
    _logger.info("Processing Event Id: %s", event_id)
    event_details = _get_event_details(event_id, event_file)
    _write_event(event_file, event_details)

def get_events(include_notifs: bool):
    """ Request the list of events from this instance.
        Iterate through the events and if requested, get the
        notifications to be written to the output file.
    """
    global _logger
    
    ### Get the current logger
    _logger = ear_logger.get_logger()
    
    # Create and open the output file, then insert the header row
    event_file = _create_event_out_file(config.events_filename)
    _write_event_header(event_file)
    
    # Set our resource URLs
    baseURL = config.xmod_url + '/reapi/2015-01-01/events?range='
    url = baseURL + config.event_range_start + '/' + config.event_range_end
    
    # Initialize loop with first request
    try:
        response = requests.get(url, auth=config.basic_auth)
    except requests.exceptions.RequestException as e:
        _logger.error(config.ERR_REQUEST_EXCEPCTION_CODE, url, repr(e))
        event_file.close()
        sys.exit(config.ERR_REQUEST_EXCEPCTION_CODE)

    # If the initial response fails, then just terminate the process
    if response.status_code != 200:
        _log_and_exit(url, response, event_file)

    # Continue until we exhaust the group list
    cnt = 0
    num_events = 1
    while response.status_code == 200:
        
        # Iterate through the result set
        body = response.json()
        num_events = body['total']
        _logger.info ("Retrieved a batch of %d events.", body['total'])
        next_records_url = body['nextRecordsUrl']
        _logger.debug ("nextRecordsUrl: %s", str(next_records_url))
        for d in body['records']:
            cnt += 1
            _logger.info('Processing Event #%d of %d: href="%s"', \
                  cnt, body['total'], d['href'])
            # Parse off the event id
            eventId = d['href'].split("/")[4]
            _process_event( event_file, eventId, include_notifs )
            
        
        # If there are more groups to get, then request the next page
        if not next_records_url:
            break
        
        _logger.info ("Getting next set of events from %s", next_records_url)
        url = config.xmod_url + next_records_url
        try:
            response = requests.get (url, auth=config.basic_auth)
        except requests.exceptions.RequestException as e:
            _logger.error(config.ERR_REQUEST_EXCEPCTION_CODE, url, repr(e))
            event_file.close()
            sys.exit(config.ERR_REQUEST_NEXT_EXCEPCTION_CODE)
    
    else:
        _logger.info ("Retrieved a total of %d from a possible %d events.", 
                     cnt, num_events)
        
    event_file.close()
        
def main():
    pass

if __name__ == '__main__':
    main()
