# -*- coding: utf-8 -*-
"""xMatters Recipients

Reference:
    https://help.xmatters.com/xmAPI/#recipient-object
    https://help.xmatters.com/xmAPI/index.html#dynamic-team-object
    https://help.xmatters.com/xmAPI/#group-object

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import json

from xMatters.References import SelfLink
from xMatters.References import ReferenceByIdAndSelfLink

class Recipient(object):
    """xMatters Recipient representation

    This class represents a view of the xMatters Recipient

    Reference:
        https://help.xmatters.com/xmAPI/#recipient-object
    """

    @staticmethod
    def _init_from_json_obj(new_obj, json_self: object):
        """Common initializer converting json object to a Recipient"""
        new_obj.id = json_self['id'] if 'id' in json_self else ""
        new_obj.target_name = (
            json_self['targetName'] if 'targetName' in json_self else "")
        new_obj.recipient_type = (
            json_self['recipientType']
            if 'recipientType' in json_self else "")
        new_obj.external_key = (
            json_self['externalKey'] if 'externalKey' in json_self else "")
        new_obj.externally_owned = (
            json_self['externallyOwned']
            if 'externallyOwned' in json_self else False)
        new_obj.locked = json_self['locked'] if 'locked' in json_self else []
        new_obj.status = json_self['status'] if 'status' in json_self else ""
        new_obj.links = (
            SelfLink.from_json_obj(json_self['links'])
            if 'links' in json_self else SelfLink())

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an Recipient instance from a JSON object"""
        new_obj = cls()
        cls._init_from_json_obj(new_obj, json_self)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an Recipient instance from a JSON payload string"""
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        self.id: str = None
        self.target_name: str = None
        self.recipient_type: str = None
        self.external_key: str = None
        self.externally_owned: bool = None
        self.locked: [str] = None
        self.status: str = None
        self.links: SelfLink = None

class DynamicTeam(Recipient):
    """xMatters DynamicTeam representation

    This class represents a view of the xMatters Dynamic Team

    Reference:
        https://help.xmatters.com/xmAPI/index.html#dynamic-team-object
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a DynamicTeam instance from a JSON object"""
        new_obj = cls()
        Recipient._init_from_json_obj(new_obj, json_self)
        new_obj.recipient_type = "DYNAMIC_TEAM"
        new_obj.status = "ACTIVE"
        new_obj.links = SelfLink()
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a DynamicTeam instance from a JSON payload string"""
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        super().__init__()
        self.recipient_type: str = None
        self.status: str = None
        self.links: SelfLink = None

class Group(Recipient):
    """xMatters Group representation

    This class represents a view of the xMatters Group

    Reference:
        https://help.xmatters.com/xmAPI/#group-object
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a Group instance from a JSON object"""
        new_obj = cls()
        Recipient._init_from_json_obj(new_obj, json_self)
        new_obj.allow_duplicates = (
            json_self['allowDuplicates']
            if 'allowDuplicates' in json_self else False)
        new_obj.description = (
            json_self['description'] if 'description' in json_self else "")
        new_obj.observed_by_all = (
            json_self['observedByAll']
            if 'observedByAll' in json_self else False)
        new_obj.site = (
            ReferenceByIdAndSelfLink.from_json_obj(json_self['site'])
            if 'site' in json_self else ReferenceByIdAndSelfLink())
        new_obj.use_default_devices = (
            json_self['useDefaultDevices']
            if 'useDefaultDevices' in json_self else False)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a Group instance from a JSON payload string"""
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        super().__init__()
        self.allow_duplicates: bool = None
        self.description: str = None
        self.observed_by_all: bool = None
        self.site: ReferenceByIdAndSelfLink = None
        self.use_default_devices: bool = None

def main():
    """In case we ever need to run this stand-alone"""
    pass

if __name__ == '__main__':
    main()
