import unittest
from client import TroiaClient
from testSettings import *

class TestLabels(unittest.TestCase):
    
        def est_AddGetEmptyAssignedLabels(self):
            client = TroiaClient(ADDRESS)
            response = client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the empty assigned labels
            response = client.await_completion(client.post_assigned_labels([]))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
           
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertFalse(result)
        
        def test_AddAssignedLabelsWithNonExistingCategories(self):
            client = TroiaClient(ADDRESS)
            categories = [{"prior":1, "name":"~!@#$%^&)(*[]()-_+=<>?/.,;:"}]
            response = client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the empty assigned labels
            assignedLabels = [
            ('worker1', 'url1', 'porn'),
            ('worker1', 'url2', 'porn'),
            ('worker1', 'url3', 'porn'),
            ('worker1', 'url4', 'porn')]
            response = client.await_completion(client.post_assigned_labels(assignedLabels))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
           
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertFalse(result)
            
            
            
        def test_AddGetAssignedLabels_SpecialChars(self):
            client = TroiaClient(ADDRESS)
            categories = [{"prior":1, "name":"~!@#$%^&)(*[]()-_+=<>?/.,;:"}]
            response = client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the empty assigned labels
            assignedLabels = [
            ('worker1', 'url1', 'porn'),
            ('worker1', 'url2', 'porn'),
            ('worker1', 'url3', 'porn'),
            ('worker1', 'url4', 'porn')]
            response = client.await_completion(client.post_assigned_labels(assignedLabels))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
           
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertFalse(result)

           
        def est_AddGetAssignedLabels(self):
            client = TroiaClient(ADDRESS)
            response = client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(ASSIGNED_LABELS))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            assignedLabels = str(result).replace('u\'', '\'')
            
            keys = ["workerName", "objectName", "categoryName"]
            for initialLabel in ASSIGNED_LABELS:
                dictionary = dict(zip(keys, initialLabel))
                self.assertTrue(str(dictionary) in assignedLabels)
                
        def est_AddGetGoldLabels(self):
            client = TroiaClient(ADDRESS)
            response = client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the gold labels
            goldLabels = [{"correctCategory": "notporn", "objectName": "url1"}]
            post_gold_labels = [("url1", "notporn")]
            response = client.await_completion(client.post_gold_data(post_gold_labels))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Correct data added', response['result'])
            
            #get the gold labels
            response = client.await_completion(client.get_gold_data())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(1, len(result))
            self.assertTrue(goldLabels[0] == result[0])          
        
        def est_AddGetUnassignedLabels(self):
            client = TroiaClient(ADDRESS)
            categories = [
            {"prior":"0.32", "name":"porn", "misclassificationCost": [{'categoryName': 'porn', 'value': 0}, {'categoryName': 'notporn', 'value': 1}]}, 
            {"prior":"0.68", "name":"notporn", "misclassificationCost":[{'categoryName': 'porn', 'value': 1}, {'categoryName': 'notporn', 'value': 0}]}]
            response = client.create(categories)
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
            self.assertTrue("{'categoryName': 'porn', 'value': 0.5}" in categoryProbabilities)
            self.assertTrue("{'categoryName': 'notporn', 'value': 0.5}" in categoryProbabilities)
        
        def est_AddGetEvaluationLabels(self):
            client = TroiaClient(ADDRESS)
            response = client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
            
            response = client.await_completion(client.post_evaluation_data(EVALUATION_DATA))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Evaluation datums added', response['result'])
            
            #get the unassigned labels
            response = client.await_completion(client.get_evaluation_data())

            self.assertEqual('OK', response['status'])
            self.assertEqual(5, len(response['result']))
            results = []
            for evaluationLabel in response['result']:
                label = (str(evaluationLabel['objectName']).replace('u\'', '\''), str(evaluationLabel['correctCategory']).replace('u\'', '\''))
                results.append(label)
            for evalLabel in EVALUATION_DATA:
                self.assertTrue(evalLabel in results)
            
            
        
            

if __name__ == '__main__':
    unittest.main()

