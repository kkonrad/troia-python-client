import unittest
from contClient import TroiaContClient
from testSettings import *

class TestPrediction(unittest.TestCase):
    
    def setUp(self):
        self.client = TroiaContClient(ADDRESS)
        response = self.client.createNewJob()
        self.assertEqual('OK', response['status'])
        
        for worker, obj, label in ASSIGNED_LABELS_CONT:
            response = self.client.await_completion(self.client.post_assigned_label(worker, obj, float(label)), 0.5)
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
        
        for obj, label, zeta in GOLD_LABELS_CONT:
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
        response = self.client.await_completion(self.client.post_compute())
        self.assertEqual('OK', response['status'])
            
        response = self.client.await_completion(self.client.get_prediction_objects())
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(EXPECTED_PREDICTION_OBJECTS) ,len(response['result']))

        predictionObjects =[]
        for object in response['result']:
            predictionObject = () 
            objectName = object['object']['name']
            goldLabel = {}
            try:
                goldLabel['value'] = object['object']['goldLabel']['value']['value']
                goldLabel['zeta'] = object['object']['goldLabel']['value']['zeta']
            except:
                print 'No gold labels for object ' + objectName
            
            estimatedZeta = object['est_zeta']
            if goldLabel:
                predictionObject = (estimatedZeta, objectName, goldLabel)
            else:
                predictionObject = (estimatedZeta, objectName)
                
            predictionObjects.append(predictionObject)
        print predictionObjects
        for expPredictionObject in EXPECTED_PREDICTION_OBJECTS:
            self.assertTrue(expPredictionObject in predictionObjects)
      
     
    def test_GetPredictionWorkers_WithoutCompute(self):
        response = self.client.await_completion(self.client.get_prediction_workers())
        self.assertEqual('Internal error: Run compute first!', response['result'])

    def test_GetPredictionWorkers_WithCompute(self):
        response = self.client.await_completion(self.client.post_compute())
        self.assertEqual('OK', response['status'])
        
        response = self.client.await_completion(self.client.get_prediction_workers())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(5, len(result))
        
        for worker in result:
            #check the assigned labels
            estimatedMu = worker['est_mu']
            workerName = worker['worker']
            estimatedSigma = worker['est_sigma']
            estimatedRho = worker['est_rho']
            workerTouple = (workerName, estimatedMu, estimatedSigma, estimatedRho)
            print workerTouple
            print EXPECTED_PREDICTION_WORKERS
            self.assertTrue(workerTouple in EXPECTED_PREDICTION_WORKERS)
                
if __name__ == '__main__':
    unittest.main()
