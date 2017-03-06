"""xMatters Event

This class represents a view of the xMatters Event that is created as part of a
request for a notification to occur.  The Event class contains both controlling
methods (typically static) for retrieving a list of Event instances, as well as
methods for manipulating instances of events.

Ref:
    https://help.xmatters.com/xmAPI/#event-objects

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import json

from References import PersonReference

class Event(object):
    """xMatters Event representation
    
    This class represents a view of the xMatters Event that is created as part 
    of a request for a notification to occur.  The Event class contains both 
    controlling methods (typically static) for retrieving a list of Event 
    instances, as well as methods for manipulating instances of events.
    
    Attributes:
        See https://help.xmatters.com/xmAPI/?python#event-objects
    """

    @classmethod
    def from_json_obj(cls, json_self:object):
        new_event = cls()
        new_event.id = json_self['id'] if 'id' in json_self else ""
        new_event.event_id = (
            json_self['eventId'] if 'eventId' in json_self else "")
        new_event.created = (
            json_self['created'] if 'created' in json_self else "")
        new_event.terminated = (
            json_self['terminated'] if 'terminated' in json_self else "")
        new_event.status = (
            json_self['status'] if 'status' in json_self else "")
        new_event.priority = (
            json_self['priority'] if 'priority' in json_self else "")
        new_event.incident = (
            json_self['incident'] if 'incident' in json_self else "")
        new_event.expiration_in_minutes = (
            json_self['expirationInMinutes'] 
            if 'expirationInMinutes' in json_self else 0)
        new_event.submitter = (
            PersonReference.from_json_obj(json_self['submitter']) 
            if 'submitter' in json_self else PersonReference())
        new_event.recipients = (
            json_self['recipients'] if 'recipients' in json_self else None)
        new_event.form = json_self['form'] if 'form' in json_self else None
        new_event.conference = (
            json_self['conference'] if 'conference' in json_self else None)
        new_event.response_options = (
            json_self['responseOptions'] 
            if 'responseOptions' in json_self else None)
        return new_event
    
    @classmethod
    def from_json_str(cls, json_self:str):
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)
    
    def __init__(self):
        """Inits Event and defines properties"""
        self.id: str = None
        self.event_id: str = None
        self.created: str = None
        self.terminated: str = None
        self.status: str = None
        self.priority: str = None
        self.incident: str = None
        self.expiration_in_minutes: int = None
        self.submitter: PersonReference = None
        self.recipients: object = None
        self.form: object = None
        self.conference: object = None
        self.response_options: object = None
     
def main():
    pass

if __name__ == '__main__':
    main()
