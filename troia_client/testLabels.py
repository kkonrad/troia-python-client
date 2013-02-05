import unittest
from client import TroiaClient
from testSettings import TestSettings
import random
import string

class TestLabels(unittest.TestCase):
    
        def generateId(self, length):
            return "".join([random.choice(string.ascii_lowercase) for x in xrange(length)])
        
        def test_AddGetAssignedLabels(self):
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(TestSettings.CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(TestSettings.ASSIGNED_LABELS))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            assignedLabels = str(result).replace('u\'', '\'')
            
            keys = ["workerName", "objectName", "categoryName"]
            for initialLabel in TestSettings.ASSIGNED_LABELS:
                dictionary = dict(zip(keys, initialLabel))
                self.assertTrue(str(dictionary) in assignedLabels)
                
        def test_AddGetGoldLabels(self):
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(TestSettings.CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            goldLabels = [{"correctCategory": "notporn", "objectName": "url1"}]
            response = client.await_completion(client.post_gold_data(goldLabels))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Correct data added', response['result'])
            
            #get the assigned labels
            response = client.await_completion(client.get_gold_data())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(1, len(result))
            self.assertTrue(goldLabels[0] == result[0])          
        
        def test_AddGetUnassignedLabels(self):
            client = TroiaClient(TestSettings.ADDRESS)
            categories = [
            {"prior":"0.32", "name":"porn", "misclassificationCost": [{'categoryName': 'porn', 'value': 0}, {'categoryName': 'notporn', 'value': 1}]}, 
            {"prior":"0.68", "name":"notporn", "misclassificationCost":[{'categoryName': 'porn', 'value': 1}, {'categoryName': 'notporn', 'value': 0}]}]
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status'])
             
            #post the unassigned labels
            response = client.await_completion(client.post_data(["testObject1"]))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Object without labels added', response['result'])
            
            #get the unassigned labels
            response = client.await_completion(client.get_data("unassigned"))
            self.assertEqual('OK', response['status'])
            self.assertEqual(1, len(response['result']))
            result = dict(response['result'][0])
                  
            self.assertFalse(result['isGold'])
            self.assertEqual("testObject1", result['name'])
            categoryProbabilities = str(result['categoryProbability']).replace('u\'', '\'')
            self.assertTrue("{'categoryName': 'porn', 'value': 0.32}" in categoryProbabilities)
            self.assertTrue("{'categoryName': 'notporn', 'value': 0.68}" in categoryProbabilities)
            
       
                
            
