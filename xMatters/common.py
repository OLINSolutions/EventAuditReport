# -*- coding: utf-8 -*-
"""xMatters Common Objects

Common objects used throughout the xMatters API.

Reference:
    https://help.xmatters.com/xmAPI/index.html#common-objects

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import json

class Error(object):
    """xMatters Error object representation

    Describes an error.
    For a complete list of error response codes, see HTTP response codes.
    https://help.xmatters.com/xmAPI/index.html#HTTP-response-codes

    Reference:
        https://help.xmatters.com/xmAPI/index.html#error-object

    Args:
        code (int, optional): The HTTP error code.
        reason (str, optional): A description of the error code.
        message (str, optional): A description of specific err that occurred.

    Attributes:
        code (int): The HTTP error code.
        reason (str): A description of the error code.
        message (str): A description of the specific error that occurred.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a Error.

        Args:
            cls (:class:`Error`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Error.

        Returns:
            Error: An instance populated with json_self.
        """
        new_obj = cls(
            json_self['code'] if 'code' in json_self else None,
            json_self['reason'] if 'reason' in json_self else None,
            json_self['message'] if 'message' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a Error.

        Args:
            cls (:class:`Error`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Error.

        Returns:
            Error: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(
            self, code: int = None, reason: str = None,
            message: str = None):
        self.code: int = code
        self.reason: str = reason
        self.message: str = message

class PaginationLinks(object):
    """xMatters PaginationLinks object representation

    Provides links to cur, prev, and next pages of a paginated result set.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#paginationLinks

    Args:
        next_link (str, optional): URI to next page of results.
        previous_link (str, optional): URI to the previous page of results.
        self_link (str, optional): URI to the parent object.

    Attributes:
        next (str): URI to next page of results.
        previous (str): URI to the previous page of results.
        self (str): URI to the parent object.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a PaginationLinks.

        Args:
            cls (:class:`PaginationLinks`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a PaginationLink.

        Returns:
            PaginationLinks: An instance populated with json_self.
        """
        if 'links' in json_self:
            new_obj = cls(
                (json_self['links']['next'] if 'next' in json_self['links']
                 else None),
                (json_self['links']['previous'] if 'previous' in
                 json_self['links'] else None),
                (json_self['links']['self'] if 'self' in json_self['links']
                 else None)
                )
        else:
            new_obj = cls(
                (json_self['next'] if 'next' in json_self
                 else None),
                (json_self['previous'] if 'previous' in
                 json_self else None),
                (json_self['self'] if 'self' in json_self
                 else None)
                )
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a PaginationLinks.

        Args:
            cls (:class:`PaginationLinks`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a PaginationLink.

        Returns:
            PaginationLinks: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(
            self, next_link: str = None, previous_link: str = None,
            self_link: str = None):
        self.next: str = next_link
        self.previous: str = previous_link
        self.self: str = self_link

class Pagination(object):
    """xMatters Pagination object representation

    A page of results. Use the links in the links field to retrieve the rest
    of the result set. See also Results pagination.
    This Class really is a pattern that is followed when the xMatters
    API is returning a paginated set of results.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#pagination-object
        https://help.xmatters.com/xmAPI/index.html#results-pagination

    Args:
        count (int, optional): The number of items in this page of results.
        data (:obj:`list` of :obj:`JSON`, optional):
            An array of the paginated object.
        links (:obj:`PaginationLinks`, optional): Links to the current,
            previous, and next pages of results.
        total (int, optional): The total number of items in the result set.

    Attributes:
        count (int): The number of items in this page of results.
        data (:obj:`list` of :obj:`JSON`): An array of the paginated object.
        links (:obj:`PaginationLinks`): Links to the current, previous, and
            next pages of results.
        total (int): The total number of items in the result set.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a Pagination.

        Args:
            cls (:class:`Pagination`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Pagination.

        Returns:
            Pagination: An instance populated with json_self.
        """
        new_obj = cls(
            json_self['count'] if 'count' in json_self else None,
            json_self['data'] if 'data' in json_self else [],
            (PaginationLinks.from_json_obj(json_self['links'])
             if 'links' in json_self else PaginationLinks()),
            json_self['total'] if 'total' in json_self else None)
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
            self, count: int = None, data: [] = None,
            links: PaginationLinks = None, total: int = None):
        self.count: int = count
        self.data: [] = data if data is not None else []
        self.links: PaginationLinks = links
        self.total: int = total

class SelfLink(object):
    """xMatters SelfLink representation

    A link that can be used to reference this object in the xMatters API.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#selfLink

    Args:
        link (str, optional): A link that can be used to access this resource
            with a GET request.

    Attributes:
        self (str): A link that can be used to access this resource
            with a GET request.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an SelfLink instance from a JSON object

        Args:
            cls (:class:`SelfLink`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a SelfLink.

        Returns:
            SelfLink: An instance populated with json_self.
        """
        new_obj = cls(json_self['self'] if 'self' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an SelfLink instance from a JSON payload string

        Args:
            cls (:class:`SelfLink`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a SelfLink.

        Returns:
            SelfLink: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, link: str = None):
        self.self: str = link

class ReferenceById(object):
    """xMatters ReferenceById representation

    The identifier of a resource.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#referenceByID-object

    Args:
        ref_id (str, optional): The identifier of a resource.

    Attributes:
        id (str): The identifier of a resource.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an ReferenceById instance from a JSON object

        Args:
            cls (:class:`ReferenceById`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a ReferenceById.

        Returns:
            ReferenceById: An instance populated with json_self.
        """
        new_obj = cls(json_self['id'] if 'id' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an ReferenceById instance from a JSON payload string

        Args:
            cls (:class:`ReferenceById`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a ReferenceById.

        Returns:
            ReferenceById: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, ref_id: str = None):
        self.id: str = ref_id

class ReferenceByIdAndSelfLink(object):
    """xMatters ReferenceByIdAndSelfLink representation

    The identifier of a resource and a SelfLink object that contains a URL
    to the resource.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#referenceByIdAndSelfLink-object

    Args:
        ref_id (str, optional): URI to next page of results.
        links (:obj:`SelfLink`, optional): A link that can be used to
            retrieve the person using this API.

    Attributes:
        id (str): The unique identifier of the person.
        links (:obj:`SelfLink`): A link that can be used to retrieve the person
            using this API.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an ReferenceByIdAndSelfLink instance from a JSON object

        Args:
            cls (:class:`ReferenceByIdAndSelfLink`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a ReferenceByIdAndSelfLink.

        Returns:
            ReferenceByIdAndSelfLink: An instance populated with json_self.
        """
        new_obj = cls(
            json_self['id'] if 'id' in json_self else None,
            (SelfLink.from_json_obj(json_self['links'])
             if 'links' in json_self else SelfLink())
            )
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a ReferenceByIdAndSelfLink instance from JSON payload str

        Args:
            cls (:class:`ReferenceByIdAndSelfLink`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a ReferenceByIdAndSelfLink.

        Returns:
            ReferenceByIdAndSelfLink: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, ref_id: str = None, links: SelfLink = None):
        self.id: str = ref_id
        self.links: SelfLink = links

def main():
    """In case we ever need to run this stand-alone"""
    pass

if __name__ == '__main__':
    main()
