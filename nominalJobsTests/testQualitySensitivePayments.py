import unittest
from client.gal import TroiaClient
from testSettings import *


class TestQualitySensitivePayments(unittest.TestCase):
    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def testQSP(self):
        assignedLabels = [
                            ('worker1', 'url1', 'cat2'),
                            ('worker1', 'url2', 'cat1'),
                            ('worker2', 'url1', 'cat1'),
                            ('worker2', 'url2', 'cat1'),
                            ('worker3', 'url1', 'cat1'),
                            ('worker3', 'url2', 'cat2')]
        goldLabels = [
                      ('url1', 'cat1'),
                      ('url2', 'cat2')
                      ]
        response = self.client.create(["cat1", "cat2"])
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.post_assigned_labels(assignedLabels))
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])

        response = self.client.post_compute()
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.get_workers_quality_payment())
        print response