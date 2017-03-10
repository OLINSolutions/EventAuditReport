# -*- coding: utf-8 -*-
"""xMatters Recipient Objects

Recipient objects used throughout the xMatters API.

Reference:
    https://help.xmatters.com/xmAPI/index.html#recipient-object
    https://help.xmatters.com/xmAPI/index.html#dynamic-team-object
    https://help.xmatters.com/xmAPI/index.html#group-object

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import json

from EventAuditReport.xMatters.common import SelfLink
from EventAuditReport.xMatters.common import ReferenceByIdAndSelfLink
from EventAuditReport.xMatters.common import Pagination
from EventAuditReport.xMatters.common import PaginationLinks

class RecipientPointer(object):
    """xMatters RecipientPointer representation

    A reference to a recipient.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipientpointer-object

    Args:
        id (str, optional): The unique identifier or target name of the
            group member.
        recipient_type (str, optional): The type of the group member.

    Attributes:
        id (str): The unique identifier or target name of the group member.
        recipient_type (str, optional): The type of the group member.
            Providing this optional field allows xMatters to process your
            request more efficiently and improves performance.
            Use one of the following values:
            “PERSON”
            “GROUP”
            “DEVICE”
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an RecipientPointer instance from a JSON object

        Args:
            cls (:class:`RecipientPointer`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a RecipientPointer.

        Returns:
            RecipientPointer: An instance populated with json_self.
        """
        new_obj = cls(
            json_self['id'] if 'id' in json_self else None,
            json_self['recipientType'] if 'recipientType' in json_self
            else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a RecipientPointer instance from JSON payload str

        Args:
            cls (:class:`RecipientPointer`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a RecipientPointer.

        Returns:
            RecipientPointer: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, ref_id: str = None, recipient_type: str = None):
        self.id: str = ref_id
        self.recipient_type: str = recipient_type

class PersonReference(object):
    """xMatters PersonReference representation

    Refers to a person in xMatters.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#person-reference-object

    Args:

    Attributes:
        id (str): The unique identifier of the person.
        targetName (str): The user id of the person.
        links (:obj:`SelfLink`): A link that can be used to retrieve the person
            using this API.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an PersonReference instance from a JSON object

        Args:
            cls (:class:`PersonReference`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a PersonReference.

        Returns:
            PersonReference: An instance populated with json_self.
        """
        new_obj = cls()
        new_obj.id = json_self['id'] if 'id' in json_self else None
        new_obj.targetName = (json_self['targetName']
                              if 'targetName' in json_self else None)
        new_obj.links = (SelfLink.from_json_obj(json_self['links'])
                         if 'links' in json_self else SelfLink())
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an PersonReference instance from a JSON payload string

        Args:
            cls (:class:`PersonReference`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a PersonReference.

        Returns:
            PersonReference: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        self.id: str = None
        self.targetName: str = None
        self.links: SelfLink = SelfLink()

class Recipient(object):
    """xMatters Recipient representation

    A recipient is a user, group, device or dynamic team in xMatters that can
    receive notifications. The recipient object provides a base for Group
    object, Device object, Person object, and Dynamic team object.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:

    Attributes:
        id (str): A unique identifier that represents the recipient.
        target_name (str): The common name of the recipient.
        receipient_type (str): The type of this object. Values include:
            “GROUP”
            “PEOPLE”
            “DEVICE”
            “DYNAMIC_TEAM”
        external_key (str): Identifies a resource in an external system.
        externally_owned (bool): True if the object is managed by an external
            system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xMatters
            user interface by most users.
        locked (:obj:`list` of :obj:`str`): A list of fields that cannot be
            modified in the xMatters user interface.
        status (str): Whether the recipient is active. Inactive recipients do
            not receive notifications. Use one of the following values:
                “ACTIVE”
                “INACTIVE”
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the object
            from within the API. This link is not included with Dynamic Team
            Recipients because they cannot yet be directly manipulated with
            this API.
    """

    @staticmethod
    def _init_from_json_obj(new_obj, json_self: object):
        """Common initializer converting json object to a Recipient"""
        new_obj.id = json_self['id'] if 'id' in json_self else None
        new_obj.target_name = (
            json_self['targetName'] if 'targetName' in json_self else None)
        new_obj.recipient_type = (
            json_self['recipientType']
            if 'recipientType' in json_self else None)
        new_obj.external_key = (
            json_self['externalKey'] if 'externalKey' in json_self else None)
        new_obj.externally_owned = (
            json_self['externallyOwned']
            if 'externallyOwned' in json_self else False)
        new_obj.locked = json_self['locked'] if 'locked' in json_self else []
        new_obj.status = json_self['status'] if 'status' in json_self else None
        new_obj.links = (
            SelfLink.from_json_obj(json_self['links'])
            if 'links' in json_self else SelfLink())

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an Recipient instance from a JSON object

        Args:
            cls (:class:`Recipient`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Recipient.

        Returns:
            Recipient: An instance populated with json_self.
        """
        new_obj = cls()
        cls._init_from_json_obj(new_obj, json_self)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an Recipient instance from a JSON payload string

        Args:
            cls (:class:`Recipient`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Recipient.

        Returns:
            Recipient: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        self.id: str = None
        self.target_name: str = None
        self.recipient_type: str = None
        self.external_key: str = None
        self.externally_owned: bool = None
        self.locked: [str] = []
        self.status: str = None
        self.links: SelfLink = SelfLink()

class DynamicTeam(Recipient):
    """xMatters DynamicTeam representation

    A dynamic team is a set of users that are automatically generated based on
    a common attribute such as their skills, location, or other attributes.
    Dynamic teams cannot be accessed and manipulated directly with the xMatters
    API. However, when a dynamic team is a member of a group it is included in
    the returned list of group members.
    A dynamic team is based on the Recipient object but does not include the
    status field (because dynamic teams are always active) and does not include
    the links field (because dynamic teams cannot be accessed with the xMatters
    API).

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object
        https://help.xmatters.com/xmAPI/index.html#dynamic-team-object

    Args:

    Attribute:
        id (str): A unique identifier that represents the dynamic team.
        target_name (str): The name of the dynamic team.
        recipient_type (str): For dynamic teams, this value is “DYNAMIC_TEAM”.
        externally_owned (bool): True if the object is managed by an external
            system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xMatters
            user interface by most users.
        use_emergency_device (bool): True if the dynamic team is configured to
            contact failsafe devices when no other devices are configured to
            receive notifications.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a DynamicTeam instance from a JSON object

        Args:
            cls (:class:`DynamicTeam`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a DynamicTeam.

        Returns:
            DynamicTeam: An instance populated with json_self.
        """
        new_obj = cls()
        Recipient._init_from_json_obj(new_obj, json_self)
        new_obj.recipient_type = "DYNAMIC_TEAM"
        new_obj.status = "ACTIVE"
        new_obj.links = SelfLink()
        new_obj.use_emergency_device = (
            json_self['useEmergencyDevice']
            if 'useEmergencyDevice' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a DynamicTeam instance from a JSON payload string

        Args:
            cls (:class:`DynamicTeam`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a DynamicTeam.

        Returns:
            DynamicTeam: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        super().__init__()
        self.recipient_type: str = "DYNAMIC_TEAM"
        self.status: str = "ACTIVE"
        self.links: SelfLink = SelfLink()
        self.use_emergency_device: bool = None

class Group(Recipient):
    """xMatters Group representation

    Group objects include the fields defined in Recipient object in addition to
    fields specific to group recipients.
    To view information about group supervisors and group observers, log on to
    the xMatters user interface and view the group.
    See also Recipient object.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object
        https://help.xmatters.com/xmAPI/index.html#group-object

    Args:

    Attributes:
        allow_duplicates (bool): True if recipients can receive more than one
            notification for the same event.
        description (str): A description of the group.
        observed_by_all (bool): True if users can locate and send notifications
            to the group regardless of their role. If this value is false, only
            users who have the selected roles can observe the group. To view or
            set the list of group observer roles, log on to the xMatters user
            interface and edit the group.
        recipient_type (str): For groups, the recipient type field is “GROUP”.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you can use to
            access the site the group uses for holidays.
        target_name (str): For groups, the target name is the group name.
        use_default_devices (bool): True if group recipients may be notified on
            their default device when they do not have a device with an active
            timeframe.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a Group instance from a JSON object

        Args:
            cls (:class:`Group`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Group.

        Returns:
            Group: An instance populated with json_self.
        """
        new_obj = cls()
        Recipient._init_from_json_obj(new_obj, json_self)
        new_obj.allow_duplicates = (
            json_self['allowDuplicates']
            if 'allowDuplicates' in json_self else None)
        new_obj.description = (
            json_self['description'] if 'description' in json_self else None)
        new_obj.observed_by_all = (
            json_self['observedByAll']
            if 'observedByAll' in json_self else None)
        new_obj.site = (
            ReferenceByIdAndSelfLink.from_json_obj(json_self['site'])
            if 'site' in json_self else ReferenceByIdAndSelfLink())
        new_obj.use_default_devices = (
            json_self['useDefaultDevices']
            if 'useDefaultDevices' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a Group instance from a JSON payload string

        Args:
            cls (:class:`Group`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Group.

        Returns:
            Group: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        super().__init__()
        self.recipient_type = "GROUP"
        self.allow_duplicates: bool = None
        self.description: str = None
        self.observed_by_all: bool = None
        self.site: ReferenceByIdAndSelfLink = None
        self.use_default_devices: bool = None

class Role(object):
    """xMatters Role representation

    Refers to a role in xMatters.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#role-object

    Args:

    Attributes:
        id (str): The unique identifier of the role.
        name (str): The name of the role.
    """

    @staticmethod
    def from_role_array(role_array: []):
        """Build an array of Role instances from a JSON object

        Args:
            json_array (:obj:`list` of :obj:`JSON`): JSON array of Roles.

        Returns:
            list: Array of Roles from json_array.
        """
        roles = []
        for role in role_array:
            roles.append(Role.from_json_obj(role))
        return roles

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a Role instance from a JSON object

        Args:
            cls (:class:`Role`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Role.

        Returns:
            Role: An instance populated with json_self.
        """
        new_obj = cls()
        new_obj.id = json_self['id'] if 'id' in json_self else None
        new_obj.id = json_self['name'] if 'name' in json_self else None
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a Role instance from a JSON payload string

        Args:
            cls (:class:`Role`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Role.

        Returns:
            Role: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        self.id: str = None
        self.name: str = None

class RolePagination(Pagination):
    """xMatters Pagination of Role object

    Reference:
        https://help.xmatters.com/xmAPI/index.html#role-object
        https://help.xmatters.com/xmAPI/index.html#pagination-object

    Args:

    Attributes:
        count (int): The number of items in this page of results.
        data (:obj:`list` of :obj:`Role`): An array of the paginated object.
        links (:obj:`PaginationLinks`): Links to the current, previous, and
            next pages of results.
        total (int): The total number of items in the result set.

    """
    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a RolePagination.

        Args:
            cls (:class:`RolePagination`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a RolePagination.

        Returns:
            RolePagination: An instance populated with json_self.
        """
        new_obj = cls(
            json_self['count'] if 'count' in json_self else None,
            (Role.from_role_array(json_self['data']) if 'data' in json_self
             else []),
            (PaginationLinks.from_json_obj(json_self['links'])
             if 'links' in json_self else PaginationLinks()),
            json_self['total'] if 'self' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a Pagination.

        Args:
            cls (:class:`Pagination`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Pagination.

        Returns:
            Pagination: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(
            self, rp_count: int = None, rp_data: [] = None,
            rp_links: PaginationLinks = None, rp_total: int = None):
        super().__init__(rp_count, None, rp_links, rp_total)
        self.data = rp_data

class Person(Recipient):
    """xMatters Person representation

    Describes a person in xMatters. A person object is a Recipient object with
    a recipientType of PERSON.
    A Person object contains the attributes of the Recipient object as well as
    the attributes described here.
    The Person object includes a list of the person’s roles when the
    ?embed=roles query parameter is used with the request.
    See also: Recipient object.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object
        https://help.xmatters.com/xmAPI/index.html#person-object

    Args:

    Attributes:
        first_name (str): The first name of the person.
        language (str): The person’s default language.
        last_name (str): The last name of the person.
        phone_login (str): An access code that the person can use to identify
            themselves when they phone in to xMatters to retrieve messages.
        properties (:obj:`JSON`): A list of the custom fields and attributes
            that are defined for this person.
        roles (:obj:`RolePagination`, optional): A list of the user’s roles.
            This optional field is included when the request uses the
            ?embed=roles query parameter.
        site (:obj:`ReferenceByIdAndSelfLink`): A link to a resource that you
            can use to find out information about the site to which the
            person is assigned.
        timezone (str): The person’s time zone. Example: “US/Eastern”
        web_login (str): The identifier the person can use to log in to the
            xMatters user interface. This is often identical to the
            targetName value.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a Person instance from a JSON object

        Args:
            cls (:class:`Person`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Person.

        Returns:
            Person: An instance populated with json_self.
        """
        new_obj = cls()
        Recipient._init_from_json_obj(new_obj, json_self)
        new_obj.first_name = (
            json_self['firstName']
            if 'firstName' in json_self else None)
        new_obj.language = (
            json_self['language'] if 'language' in json_self else None)
        new_obj.last_name = (
            json_self['lastName']
            if 'lastName' in json_self else None)
        new_obj.phone_login = (
            json_self['phoneLogin']
            if 'phoneLogin' in json_self else None)
        new_obj.properties = (
            json_self['properties']
            if 'properties' in json_self else None)
        new_obj.roles = (
            RolePagination.from_json_obj(json_self['roles'])
            if 'roles' in json_self else RolePagination())
        new_obj.site = (
            ReferenceByIdAndSelfLink.from_json_obj(json_self['site'])
            if 'site' in json_self else ReferenceByIdAndSelfLink())
        new_obj.timezone = (
            json_self['timezone']
            if 'timezone' in json_self else None)
        new_obj.web_login = (
            json_self['webLogin']
            if 'webLogin' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a Person instance from a JSON payload string

        Args:
            cls (:class:`Person`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Person.

        Returns:
            Person: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        super().__init__()
        self.recipient_type = "PERSON"
        self.first_name: str = None
        self.language: str = None
        self.last_name: str = None
        self.phone_login: str = None
        self.properties = []
        self.roles = RolePagination()
        self.site: ReferenceByIdAndSelfLink = None
        self.timezone = None
        self.web_login = None

def main():
    """In case we ever need to run this stand-alone"""
    pass

if __name__ == '__main__':
    main()
