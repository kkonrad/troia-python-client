import unittest
from client import TroiaClient
from testSettings import *
import time


class TestCommandStatus(unittest.TestCase):

    def setUp(self):
        self.tc = TroiaClient(ADDRESS)

    def tearDown(self):
        self.tc.delete()

    def test_GetRedirectData(self):
        self.tc.create(CATEGORIES)
        assigend_labels_response = self.tc.get_assigned_labels()
        time.sleep(0.5)
        self.assertLessEqual(self.tc.get_status(assigend_labels_response['redirect'])['result'], [])
        self.tc.await_completion(self.tc.post_assigned_labels(ASSIGNED_LABELS))
        self.assertEqual(len(ASSIGNED_LABELS), len(self.tc.await_completion(self.tc.get_assigned_labels())['result']))
        #still empty
        self.assertListEqual(self.tc.get_status(assigend_labels_response['redirect'])['result'], [])
