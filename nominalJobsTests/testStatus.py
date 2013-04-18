import unittest
from client.gal import TroiaClient
from testSettings import *


class TestStatus(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def test_GetStatus(self):
        response = self.client.status()
        self.assertEqual('OK', response['status'])
        self.assertEqual('OK', response['result']['status'])
        self.assertEqual('OK', response['result']['job_storage_status'])
