import unittest
from client.gal import TroiaClient
from testSettings import *
from pprint import pprint


class TestQualitySensitivePayments(unittest.TestCase):
    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def testQSP_ZeroWorkerQUality(self):
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

        response = self.client.await_completion(self.client.get_estimated_workers_quality("ExpectedCost"))
        self.assertEqual('OK', response['status'])
        pprint(response)

        response = self.client.await_completion(self.client.get_workers_quality_payment())
        pprint(response)

    def testQSP_NegativeWorkerQuality(self):
        assignedLabels = [
                            ('worker1', 'url1', 'cat2'),
                            ('worker1', 'url2', 'cat1'),
                            ('worker1', 'url3', 'cat2'),
                            ('worker2', 'url1', 'cat1'),
                            ('worker2', 'url2', 'cat1'),
                            ('worker2', 'url3', 'cat1'),
                            ('worker3', 'url1', 'cat1'),
                            ('worker3', 'url2', 'cat2'),
                            ('worker3', 'url3', 'cat1')
                            ]
        goldLabels = [
                      ('url1', 'cat1'),
                      ('url2', 'cat2'),
                      ('url3', 'cat1')
                      ]
        response = self.client.create(["cat1", "cat2"], categoryPriors= [{"categoryName": "cat1", "value": 0.1}, {"categoryName": "cat2", "value": 0.9}])
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.post_assigned_labels(assignedLabels))
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])

        response = self.client.post_compute()
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.get_workers_confusion_matrix())
        pprint(response)

        response = self.client.await_completion(self.client.get_estimated_workers_quality("ExpectedCost"))
        self.assertEqual('OK', response['status'])
        pprint(response)

        response = self.client.await_completion(self.client.get_workers_quality_payment())
        pprint(response)