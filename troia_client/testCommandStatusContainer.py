import unittest
from client import TroiaClient
from testSettings import TestSettings
from test_on_data import COST_MATRIX, WORKERS_LABELS
import time

class TestCommandStatus(unittest.TestCase):

        def setUp(self):
            self.tc = TroiaClient(TestSettings.ADDRESS)
            
        def test_GetRedirectData(self):
            try:
                self.tc.delete()
                time.sleep(1)
            except:
                pass
            self.tc.create(COST_MATRIX)
            assigend_labels_response = self.tc.get_assigned_labels()
            time.sleep(0.5)
            self.assertDictEqual(self.tc.get_status(assigend_labels_response['redirect'])['result'], {})
            self.tc.await_completion(self.tc.post_assigned_labels(WORKERS_LABELS))
            self.assertIsNotNone(self.tc.await_completion(self.tc.get_assigned_labels())['result'])
            #still empty
            self.assertDictEqual(self.tc.get_status(assigend_labels_response['redirect'])['result'], {})
