# -*- coding: utf-8 -*-
"""xMatters PaginationLinks

Reference:
    https://help.xmatters.com/xmAPI/#paginationLinks
    
This module contains the declaration of class PaginationLinks.

"""

import json

class PaginationLinks(object):
    """Provides links to cur, prev, and next pages of a paginated result set.

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
            json_self (:obj:`JSON`): Payload for a PaginationLink.
    
        Returns:
            A PaginationLinks instance populated with json_self.
            
        """
        new_obj = cls(
            json_self['next'] if 'next' in json_self else None,
            json_self['previous'] if 'previous' in json_self else None,
            json_self['self'] if 'self' in json_self else None)
        return new_obj
    
    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a PaginationLinks.
    
        Args:
            cls (:class:`PaginationLinks`): Class to instantiate.
            json_self (:str:`JSON`): String for a PaginationLink.
    
        Returns:
            A PaginationLinks instance populated with json_self.
            
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)
    
    def __init__(
            self, next_link: str = None, previous_link: str = None,
            self_link: str = None ):
        """Initializes a new instance of a PaginationLinks.
    
        Args:
            next_link (str): URI of next page of results.
            previous_link (str): URI of previous page of results.
            self_link: (str): URI of self.
    
        Returns:
            A PaginationLinks instance populated with json_self.
            
        """
        self.next: str = next_link
        self.previous: str = previous_link
        self.self: str = self_link
    
def main():
    pass

if __name__ == '__main__':
    main()
