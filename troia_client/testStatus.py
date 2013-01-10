import unittest
from client import TroiaClient
from testSettings import TestSettings

class TestStatus(unittest.TestCase):

        def setUp(self):
            self.tc = TroiaClient(TestSettings.ADDRESS)
            
        def test_GetStatus(self):
            response = self.tc.status()
            print response
            self.assertEqual('OK', response['status'])
            self.assertEqual('OK', response['result']['status'])
            self.assertEqual('OK', response['result']['job_storage_status'])            
            self.assertEqual('CachedDataBase', response['result']['job_storage'])