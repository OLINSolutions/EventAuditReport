# -*- coding: utf-8 -*-
"""xMatters References

Reference:
    https://help.xmatters.com/xmAPI/index.html#selfLink
    https://help.xmatters.com/xmAPI/index.html#referenceByID-object
    https://help.xmatters.com/xmAPI/index.html#referenceByIdAndSelfLink-object
    https://help.xmatters.com/xmAPI/index.html#person-reference-object

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import json

class SelfLink(object):
    """xMatters SelfLink representation

    This class represents a view of the xMatters SelfLink

    Reference:
        https://help.xmatters.com/xmAPI/index.html#selfLink
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an SelfLink instance from a JSON object"""
        new_obj = cls(json_self['self'] if 'self' in json_self else "")
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an SelfLink instance from a JSON payload string"""
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, link: str = None):
        self.self: str = link

class ReferenceById(object):
    """xMatters ReferenceById representation

    This class represents a view of the xMatters ReferenceById

    Reference:
        https://help.xmatters.com/xmAPI/index.html#referenceByID-object
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an ReferenceById instance from a JSON object"""
        new_obj = cls(json_self['id'] if 'id' in json_self else "")
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an ReferenceById instance from a JSON payload string"""
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, ref_id: str = None):
        self.id: str = ref_id

class ReferenceByIdAndSelfLink(object):

    @classmethod
    def from_json_obj(cls, json_self: object):
        new_obj = cls(
            json_self['id'] if 'id' in json_self else None,
            SelfLink(json_self['links']) if 'links' in json_self else "")
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, ref_id: str = None, links: SelfLink = None):
        self.id: str = ref_id
        self.links: SelfLink = links

class PersonReference(object):

    @classmethod
    def from_json_obj(cls, json_self: object):
        new_obj = cls()
        new_obj.id = json_self['id'] if 'id' in json_self else ""
        new_obj.targetName = (json_self['targetName']
                              if 'targetName' in json_self else "")
        new_obj.links = (SelfLink.from_json_obj(json_self['links'])
                         if 'links' in json_self else SelfLink())
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        self.id: str = None
        self.targetName: str = None
        self.links: SelfLink = None

def main():
    pass

if __name__ == '__main__':
    main()
