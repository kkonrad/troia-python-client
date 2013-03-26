import unittest
from client.galc import TroiaContClient
from testSettings import *


class TestPrediction(unittest.TestCase):

    def setUp(self):
        self.client = TroiaContClient(ADDRESS)
        response = self.client.create()
        self.assertEqual('OK', response['status'])

        #post the assigned labels
        response = self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS_CONT))
        self.assertEqual('OK', response['status'])

        #post golds
        response = self.client.await_completion(self.client.post_gold_data(GOLD_LABELS_CONT))
        self.assertEqual('OK', response['status'])

    def tearDown(self):
        self.client.delete()

    def test_Compute(self):
        response = self.client.await_completion(self.client.post_compute())
        self.assertEqual('OK', response['status'])

    def test_GetPredictionObjects_WithCompute(self):
        response = self.client.await_completion(self.client.post_compute())
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.get_objects_prediction())
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(EXPECTED_PREDICTION_OBJECTS), len(response['result']))
        for object in response['result']:
            object_name = object['object']['name']
            self.assertAlmostEqual(EXPECTED_PREDICTION_OBJECTS[object_name][0], object['est_zeta'], 5)
            if 'goldLabel' in object['object']:
                self.assertAlmostEqual(EXPECTED_PREDICTION_OBJECTS[object_name][1]['zeta'], object['object']['goldLabel']['zeta'], 5)
                self.assertAlmostEqual(EXPECTED_PREDICTION_OBJECTS[object_name][1]['value'], object['object']['goldLabel']['value'], 5)

    def test_GetPredictionForOneObject_WithCompute(self):
        response = self.client.await_completion(self.client.post_compute())
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.get_object_prediction('url1'))
        self.assertEqual('OK', response['status'])
        self.assertNotEqual({}, response['result'])

    def test_GetPredictionWorkers_WithCompute(self):
        response = self.client.await_completion(self.client.post_compute())
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.get_workers_prediction())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(5, len(result))

        for worker in result:
            #check the assigned labels
            worker_name = worker['worker']
            self.assertAlmostEqual(EXPECTED_PREDICTION_WORKERS[worker_name][0], worker['est_mu'], 5)
            self.assertAlmostEqual(EXPECTED_PREDICTION_WORKERS[worker_name][1], worker['est_sigma'], 5)
            self.assertAlmostEqual(EXPECTED_PREDICTION_WORKERS[worker_name][2], worker['est_rho'], 5)

    def test_GetPredictionForOneWorker_WithCompute(self):
        response = self.client.await_completion(self.client.post_compute())
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.get_worker_prediction('worker1'))
        self.assertEqual('OK', response['status'])
        self.assertNotEqual({}, response['result'])

if __name__ == '__main__':
    unittest.main()
