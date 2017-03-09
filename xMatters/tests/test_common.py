#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for EventAuditReport.xMatters.common.
"""

import unittest
import json

from EventAuditReport.xMatters.common import Error
from EventAuditReport.xMatters.common import PaginationLinks
from EventAuditReport.xMatters.common import Pagination

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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
