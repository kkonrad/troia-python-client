import unittest
from client.galc import TroiaContClient
from testSettings import *


class TestWorkers(unittest.TestCase):

    def setUp(self):
        self.client = TroiaContClient(ADDRESS)
        response = self.client.create()
        self.assertEqual('OK', response['status'])

    def tearDown(self):
        self.client.delete()

    def load_assigns(self):
        #post the assigned labels
        response = self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS_CONT))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Assigns added', response['result'])

    def test_GetAllWorkers(self):
        self.load_assigns()
        #get all workers
        response = self.client.await_completion(self.client.get_workers())
        for w in response['result']:
            self.assertEqual(5, w['value']['assigns'])
        self.assertEqual(5, len(response['result']))
        self.assertEqual('OK', response['status'])

    def test_GetWorkerInfo(self):
        self.load_assigns()
        #get the data for the given worker
        response = self.client.await_completion(self.client.get_worker_info("worker1"))
        self.assertEqual('worker1', response['result']['workerName'])
        self.assertEqual(5, response['result']['value']['assigns'])
        self.assertEqual('OK', response['status'])

    def test_GetWorkerAssigns(self):
        self.load_assigns()
        #get the assigns for the given worker
        response = self.client.await_completion(self.client.get_worker_assigns("worker1"))
        for al in response['result']:
            self.assertEqual(al['worker'], 'worker1')
        self.assertEqual(5, len(response['result']))
        self.assertEqual('OK', response['status'])
