# -*- coding: utf-8 -*-
"""xMatters PaginationLinks

Reference:
    https://help.xmatters.com/xmAPI/#paginationLinks
    
@author: jolin

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import json

class PaginationLinks(object):

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a PaginationLinks.
    
        Args:
            param1: The first parameter.
            param2: The second parameter.
    
        Returns:
            The return value. True for success, False otherwise.
    
        """
        new_obj = cls(
            json_self['next'] if 'next' in json_self else None,
            json_self['previous'] if 'previous' in json_self else None,
            json_self['self'] if 'self' in json_self else None)
        return new_obj
    
    @classmethod
    def from_json_str(cls, json_self: str):
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)
    
    def __init__(
            self, next_link: str = None, previous_link: str = None,
            self_link: str = None ):
        self.next: str = next_link
        self.previous: str = previous_link
        self.self: str = self_link
    
def main():
    pass

if __name__ == '__main__':
    main()
