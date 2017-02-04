# -*- coding: utf-8 -*-
"""xMatters PaginationLinks

Reference:
    https://help.xmatters.com/xmAPI/#paginationLinks
    
@author: jolin

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

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
