import unittest
from client import TroiaClient
from testSettings import *

class TestStatus(unittest.TestCase):

    def setUp(self):
        self.tc = TroiaClient(ADDRESS)
        
    def test_GetStatus(self):
        response = self.tc.status()
        self.assertEqual('OK', response['status'])
        self.assertEqual('OK', response['result']['status'])
        self.assertEqual('OK', response['result']['job_storage_status'])            
        self.assertTrue('DataBase' in response['result']['job_storage'])
