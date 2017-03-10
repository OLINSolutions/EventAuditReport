#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for EventAuditReport.xMatters.common.
"""

import unittest
import json

from xMatters.common import Error
from xMatters.common import PaginationLinks
from xMatters.common import Pagination
from xMatters.common import SelfLink
from xMatters.common import ReferenceById
from xMatters.common import ReferenceByIdAndSelfLink

class ErrorTest(unittest.TestCase):
    """Collection of unit tests cases for the Error class
    """

    def setUp(self):
        print("ErrorTest.setUp")
        self.code = 404
        self.reason = "Not Found"
        self.message = (
            "Could not find a person with id 0313142d3-4703-a90e-36cc5f5f6209")
        self.err_json_str = (
            '{"code" : %d,"reason" : "%s","message" : '
            '"%s"}')%(self.code, self.reason, self.message)

    def tearDown(self):
        print("ErrorTest.tearDown")

    def test_Error(self):
        print("Start test_Error")
        err_obj = Error(self.code, self.reason, self.message)
        self.assertIsInstance(err_obj, Error)
        self.assertEqual(err_obj.code, self.code)
        self.assertEqual(err_obj.reason, self.reason)
        self.assertEqual(err_obj.message, self.message)
        print("test_Error Successful")

    def test_Error_from_json_obj(self):
        print("Start test_Error_from_json_obj")
        err_json_obj = json.loads(self.err_json_str);
        err_obj = Error.from_json_obj(err_json_obj)
        self.assertIsInstance(err_obj, Error)
        self.assertEqual(err_obj.code, self.code)
        self.assertEqual(err_obj.reason, self.reason)
        self.assertEqual(err_obj.message, self.message)
        print("test_Error_from_json_obj Successful")

    def test_Error_from_json_str(self):
        print("Start test_Error_from_json_str")
        err_obj = Error.from_json_str(self.err_json_str)
        self.assertIsInstance(err_obj, Error)
        self.assertEqual(err_obj.code, self.code)
        self.assertEqual(err_obj.reason, self.reason)
        self.assertEqual(err_obj.message, self.message)
        print("test_Error_from_json_str Successful")

class PaginationLinksTest(unittest.TestCase):
    """Collection of unit tests cases for the PaginationLinks class
    """

    def setUp(self):
        print("PaginationLinksTest.setUp")
        self.self = "/api/xm/1/people?offset=100&limit=100"
        self.previous = "/api/xm/1/people?offset=0&limit=100"
        self.next = "/api/xm/1/people?offset=200&limit=100"
        self.links_json_str = (
            '{"links":{"self": "%s", "previous": "%s", "next": "%s" }}'
            )%(self.self, self.previous, self.next)

    def tearDown(self):
        print("PaginationLinksTest.tearDown")

    def test_PaginationLinks(self):
        print("Start test_PaginationLinks")
        obj = PaginationLinks(self.next, self.previous, self.self)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertEqual(obj.self, self.self)
        self.assertEqual(obj.previous, self.previous)
        self.assertEqual(obj.next, self.next)
        print("test_PaginationLinks Successful")

    def test_PaginationLinks_from_json_obj(self):
        print("Start test_PaginationLinks_from_json_obj")
        json_obj = json.loads(self.links_json_str);
        obj = PaginationLinks.from_json_obj(json_obj)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertEqual(obj.self, self.self)
        self.assertEqual(obj.previous, self.previous)
        self.assertEqual(obj.next, self.next)
        print("test_PaginationLinks_from_json_obj Successful")

    def test_PaginationLinks_from_json_str(self):
        print("Start test_PaginationLinks_from_json_str")
        obj = PaginationLinks.from_json_str(self.links_json_str)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertEqual(obj.self, self.self)
        self.assertEqual(obj.previous, self.previous)
        self.assertEqual(obj.next, self.next)
        print("test_PaginationLinks_from_json_str Successful")

class PaginationTest(unittest.TestCase):
    """Collection of unit tests cases for the Pagination class
    """

    def setUp(self):
        print("PaginationTest.setUp")
        self.count = 100
        self.total = 235
        self.data_id1 = "8f2d98ed-eaa9-4b0b-b366-c1db06b27e1f"
        self.data_id2 = "8f2d98ed-eaa9-4b0b-b366-c1db06b27e1f"
        self.data = [{"id": self.data_id1},{"id": self.data_id2}]
        self.self = "/api/xm/1/people?offset=0&limit=100"
        self.previous = None
        self.next = "/api/xm/1/people?offset=100&limit=100"
        self.links_json_str = (
            '"links":{"self": "%s", "next": "%s"}'
            )%(self.self, self.next)
        self.links = PaginationLinks.from_json_str('{%s}'%self.links_json_str)
        self.pagi_json_str = (
            '{"count": %d, "total": %d, '
            '"data": [{"id": "%s"},{"id": "%s"}], '
            '%s}'
            )%(self.count, self.total, self.data_id1, 
               self.data_id2, self.links_json_str)

    def tearDown(self):
        print("PaginationTest.tearDown")

    def test_Pagination(self):
        print("Start test_Pagination")
        obj = Pagination(self.count, self.data, self.links, self.total)
        self.assertIsInstance(obj, Pagination)
        self.assertEqual(obj.count, self.count)
        self.assertEqual(obj.data, self.data)
        self.assertIsInstance(obj.links, PaginationLinks)
        self.assertEqual(obj.links, self.links)
        self.assertEqual(obj.total, self.total)
        print("test_Pagination Successful")

    def test_Pagination_from_json_obj(self):
        print("Start test_Pagination_from_json_obj")
        json_obj = json.loads(self.pagi_json_str);
        obj = Pagination.from_json_obj(json_obj)
        self.assertIsInstance(obj, Pagination)
        self.assertEqual(obj.count, self.count)
        self.assertEqual(obj.data, self.data)
        self.assertIsInstance(obj.links, PaginationLinks)
        self.assertEqual(obj.links.self, self.links.self)
        self.assertEqual(obj.links.next, self.links.next)
        self.assertEqual(obj.total, self.total)
        print("test_Pagination_from_json_obj Successful")

    def test_Pagination_from_json_str(self):
        print("Start test_Pagination_from_json_str")
        obj = Pagination.from_json_str(self.pagi_json_str)
        self.assertIsInstance(obj, Pagination)
        self.assertEqual(obj.count, self.count)
        self.assertEqual(obj.data, self.data)
        self.assertIsInstance(obj.links, PaginationLinks)
        self.assertEqual(obj.links.self, self.links.self)
        self.assertEqual(obj.links.next, self.links.next)
        self.assertEqual(obj.total, self.total)
        print("test_Pagination_from_json_str Successful")

class SelfLinkTest(unittest.TestCase):
    """Collection of unit tests cases for the SelfLink class
    """

    def setUp(self):
        print("SelfLinkTest.setUp")
        self.self = "/api/xm/1/people/84a6dde7-82ad-4e64-9f4d-3b9001ad60de"
        self.self_json_str = ('{"self": "%s"}')%(self.self)

    def tearDown(self):
        print("SelfLinkTest.tearDown")

    def test_SelfLink(self):
        print("Start test_SelfLink")
        obj = SelfLink(self.self)
        self.assertIsInstance(obj, SelfLink)
        self.assertEqual(obj.self, self.self)
        print("test_SelfLink Successful")

    def test_SelfLink_from_json_obj(self):
        print("Start test_SelfLink_from_json_obj")
        json_obj = json.loads(self.self_json_str);
        obj = SelfLink.from_json_obj(json_obj)
        self.assertIsInstance(obj, SelfLink)
        self.assertEqual(obj.self, self.self)
        print("test_SelfLink_from_json_obj Successful")

    def test_SelfLink_from_json_str(self):
        print("Start test_SelfLink_from_json_str")
        obj = SelfLink.from_json_str(self.self_json_str)
        self.assertIsInstance(obj, SelfLink)
        self.assertEqual(obj.self, self.self)
        print("test_SelfLink_from_json_str Successful")

class ReferenceByIdTest(unittest.TestCase):
    """Collection of unit tests cases for the ReferenceById class
    """

    def setUp(self):
        print("ReferenceByIdTest.setUp")
        self.id = "/api/xm/1/people/84a6dde7-82ad-4e64-9f4d-3b9001ad60de"
        self.id_json_str = ('{"id": "%s"}')%(self.id)

    def tearDown(self):
        print("ReferenceByIdTest.tearDown")

    def test_ReferenceById(self):
        print("Start test_ReferenceById")
        obj = ReferenceById(self.id)
        self.assertIsInstance(obj, ReferenceById)
        self.assertEqual(obj.id, self.id)
        print("test_ReferenceById Successful")

    def test_ReferenceById_from_json_obj(self):
        print("Start test_ReferenceById_from_json_obj")
        json_obj = json.loads(self.id_json_str);
        obj = ReferenceById.from_json_obj(json_obj)
        self.assertIsInstance(obj, ReferenceById)
        self.assertEqual(obj.id, self.id)
        print("test_ReferenceById_from_json_obj Successful")

    def test_ReferenceById_from_json_str(self):
        print("Start test_ReferenceById_from_json_str")
        obj = ReferenceById.from_json_str(self.id_json_str)
        self.assertIsInstance(obj, ReferenceById)
        self.assertEqual(obj.id, self.id)
        print("test_ReferenceById_from_json_str Successful")

class ReferenceByIdAndSelfLinkTest(unittest.TestCase):
    """Collection of unit tests cases for the ReferenceByIdAndSelfLink class
    """
    def setUp(self):
        print("ReferenceByIdAndSelfLinkTest.setUp")
        self.id = "f0c572a8-45ec-fe23-289c-df749cf19a5e"
        self.self = "/api/xm/1/sites/f0c572a8-45ec-fe23-289c-df749cf19a5e"
        self.previous = None
        self.next = None
        self.links_json_str = ('{"self": "%s"}')%(self.self)
        self.links =SelfLink.from_json_str(self.links_json_str)
        self.id_json_str = (
            '{"id": "%s", "links": %s}'
            )%(self.id, self.links_json_str)

    def tearDown(self):
        print("ReferenceByIdAndSelfLinkTest.tearDown")

    def test_ReferenceByIdAndSelfLink(self):
        print("Start test_ReferenceByIdAndSelfLink")
        obj = ReferenceByIdAndSelfLink(self.id, self.links)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.id, self.id)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        print("test_ReferenceByIdAndSelfLink Successful")

    def test_ReferenceByIdAndSelfLink_from_json_obj(self):
        print("Start test_ReferenceByIdAndSelfLink_from_json_obj")
        json_obj = json.loads(self.id_json_str);
        obj = ReferenceByIdAndSelfLink.from_json_obj(json_obj)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.id, self.id)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        print("test_ReferenceByIdAndSelfLink_from_json_obj Successful")

    def test_ReferenceByIdAndSelfLink_from_json_str(self):
        print("Start test_ReferenceByIdAndSelfLink_from_json_str")
        obj = ReferenceByIdAndSelfLink.from_json_str(self.id_json_str)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.id, self.id)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        print("test_ReferenceByIdAndSelfLink_from_json_str Successful")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
