#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for EventAuditReport.xMatters.recipients.
"""

import unittest
import json

from xMatters.recipients import RecipientPointer
from xMatters.recipients import PersonReference
from xMatters.recipients import Recipient

from xMatters.common import SelfLink

class RecipientPointerTest(unittest.TestCase):
    """Collection of unit tests cases for the RecipientPointer class
    """

    def setUp(self):
        print("RecipientPointerTest.setUp")
        self.id_p = "438e9245-b32d-445f-916bd3e07932c892"
        self.recipient_type_p = "PERSON"
        self.rp_p_json_str = (
            '{"id": "%s", "recipientType": "%s"}'
            )%(self.id_p, self.recipient_type_p)
        self.id_g = "f0c572a8-45ec-fe23-289c-df749cf19a5e"
        self.recipient_type_g = "GROUP"
        self.rp_g_json_str = (
            '{"id": "%s", "recipientType": "%s"}'
            )%(self.id_g, self.recipient_type_g)
        self.id_d = "8f2d98ed-eaa9-4b0b-b366-c1db06b27e1f"
        self.recipient_type_d = "DEVICE"
        self.rp_d_json_str = (
            '{"id": "%s", "recipientType": "%s"}'
            )%(self.id_d, self.recipient_type_d)

    def tearDown(self):
        print("RecipientPointerTest.tearDown")

    def test_RecipientPointer(self):
        print("Start test_RecipientPointer")
        obj = RecipientPointer(self.id_p, self.recipient_type_p)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_p)
        self.assertEqual(obj.recipient_type, self.recipient_type_p)
        obj = RecipientPointer(self.id_g, self.recipient_type_g)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_g)
        self.assertEqual(obj.recipient_type, self.recipient_type_g)
        obj = RecipientPointer(self.id_d, self.recipient_type_d)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_d)
        self.assertEqual(obj.recipient_type, self.recipient_type_d)
        print("test_RecipientPointer Successful")

    def test_RecipientPointer_from_json_obj(self):
        print("Start test_RecipientPointer_from_json_obj")
        json_obj = json.loads(self.rp_p_json_str);
        obj = RecipientPointer.from_json_obj(json_obj)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_p)
        self.assertEqual(obj.recipient_type, self.recipient_type_p)
        json_obj = json.loads(self.rp_g_json_str);
        obj = RecipientPointer.from_json_obj(json_obj)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_g)
        self.assertEqual(obj.recipient_type, self.recipient_type_g)
        json_obj = json.loads(self.rp_d_json_str);
        obj = RecipientPointer.from_json_obj(json_obj)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_d)
        self.assertEqual(obj.recipient_type, self.recipient_type_d)
        print("test_RecipientPointer_from_json_obj Successful")

    def test_RecipientPointer_from_json_str(self):
        print("Start test_RecipientPointer_from_json_str")
        obj = RecipientPointer.from_json_str(self.rp_p_json_str)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_p)
        self.assertEqual(obj.recipient_type, self.recipient_type_p)
        obj = RecipientPointer.from_json_str(self.rp_g_json_str)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_g)
        self.assertEqual(obj.recipient_type, self.recipient_type_g)
        obj = RecipientPointer.from_json_str(self.rp_d_json_str)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_d)
        self.assertEqual(obj.recipient_type, self.recipient_type_d)
        print("test_RecipientPointer_from_json_str Successful")

class PersonReferenceTest(unittest.TestCase):
    """Collection of unit tests cases for the PersonReference class
    """

    def setUp(self):
        print("PersonReferenceTest.setUp")
        self.id = "481086d8-357a-4279-b7d5-d7dce48fcd12"
        self.target_name = "mmcbride"
        self.self = "/api/xm/1/people/481086d8-357a-4279-b7d5-d7dce48fcd12"
        self.links_json_str = ('{"self": "%s"}')%(self.self)
        self.links =SelfLink.from_json_str(self.links_json_str)
        self.pr_json_str = (
            '{"id": "%s", "targetName": "%s", "links": %s}'
            )%(self.id, self.target_name, self.links_json_str)

    def tearDown(self):
        print("PersonReferenceTest.tearDown")

    def test_PersonReference(self):
        print("Start test_PersonReference")
        obj = PersonReference(self.id, self.target_name, self.links)
        self.assertIsInstance(obj, PersonReference)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        print("test_PersonReference Successful")

    def test_PersonReference_from_json_obj(self):
        print("Start test_PersonReference_from_json_obj")
        json_obj = json.loads(self.pr_json_str);
        obj = PersonReference.from_json_obj(json_obj)
        self.assertIsInstance(obj, PersonReference)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        print("test_PersonReference_from_json_obj Successful")

    def test_PersonReference_from_json_str(self):
        print("Start test_PersonReference_from_json_str")
        obj = PersonReference.from_json_str(self.pr_json_str)
        self.assertIsInstance(obj, PersonReference)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        print("test_PersonReference_from_json_str Successful")

""" 
Test Base Recipient
{
  "id":"9407eb2e-8eb2-43d9-88a8-875237af941d",
  "targetName":"mmcbride",
  "recipientType":"PERSON",
  "status":"ACTIVE",
  "externalKey" : "20160112MCK-FLY",
  "externallyOwned":false,
  "locked":[],
  "links":    
  {
    "self":"/api/xm/1/people/9407eb2e-8eb2-43d9-88a8-875237af941d"
  }
}
"""
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
