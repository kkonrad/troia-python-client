import unittest
from contClient import TroiaContClient
from testSettings import TestSettings

class TestWorkers(unittest.TestCase):

        def test_GetAllWorkers(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(TestSettings.ASSIGNED_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #get all workers
            response = client.await_completion(client.get_workers())
            print response

        def test_GetWorkerData(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(TestSettings.ASSIGNED_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #get the data for the given worker
            response = client.await_completion(client.get_worker_data("worker1"))
            print response


        def test_GetWorkerAssigns(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(TestSettings.ASSIGNED_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #get the assigns for the given worker
            response = client.await_completion(client.get_worker_assigns("worker1"))
            print response