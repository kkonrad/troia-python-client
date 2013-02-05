import unittest
from contClient import TroiaContClient
from testSettings import TestSettings

class TestPrediction(unittest.TestCase):

        def test_Calculate(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(TestSettings.ASSIGNED_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #post the gold labels
            response = client.await_completion(client.post_gold_data(TestSettings.GOLD_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Correct data added', response['result'])
            
            #calculate
            response = client.await_completion(client.post_calculate())
            self.assertEqual('OK', response['status'])
            
        def test_GetPredictionObjects(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(TestSettings.ASSIGNED_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #post the gold labels
            response = client.await_completion(client.post_gold_data(TestSettings.GOLD_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Correct data added', response['result'])
            
            response = client.await_completion(client.get_prediction_objects())
            self.assertEqual('OK', response['status'])
        
        def test_GetPredictionWorkers(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(TestSettings.ASSIGNED_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #post the gold labels
            response = client.await_completion(client.post_gold_data(TestSettings.GOLD_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Correct data added', response['result'])
            
            response = client.await_completion(client.get_prediction_workers())
            self.assertEqual('OK', response['status'])
        
            
    