import unittest
from contClient import TroiaContClient
from testSettings import TestSettings

class TestPrediction(unittest.TestCase):
    
    def setUp(self):
        self.client = TroiaContClient(TestSettings.ADDRESS)
        response = self.client.createNewJob()
        self.assertEqual('OK', response['status'])
        
        for worker, obj, label in TestSettings.ASSIGNED_LABELS_CONT:
            response = self.client.await_completion(self.client.post_assigned_label(worker, obj, float(label)), 0.5)
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
        
        for obj, label, zeta in TestSettings.GOLD_LABELS_CONT:
            response = self.client.await_completion(self.client.post_gold_datum(obj, label, zeta))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Gold object added', response['result'])

    def test_Compute(self):
        response = self.client.await_completion(self.client.post_compute())
        self.assertEqual('OK', response['status'])
            
    def test_GetPredictionObjects_WithoutCompute(self):               
        response = self.client.await_completion(self.client.get_prediction_objects())
        self.assertEqual('Internal error: Run compute first!', response['result'])
        
    def test_GetPredictionObjects_WithCompute(self):
        response = self.client.await_completion(self.client.get_prediction_objects())
        self.assertEqual('OK', response['status'])
            
        response = self.client.await_completion(self.client.get_prediction_objects())
        self.assertEqual('OK', response['status'])
     
    def test_GetPredictionWorkers_WithoutCompute(self):
        response = self.client.await_completion(self.client.get_prediction_workers())
        self.assertEqual('Internal error: Run compute first!', response['result'])
        
    def test_GetPredictionWorkers_WithCompute(self):
        response = self.client.await_completion(self.client.get_prediction_objects())
        self.assertEqual('OK', response['status'])
        
        response = self.client.await_completion(self.client.get_prediction_workers())
        self.assertEqual('OK', response['status'])
        
            
    