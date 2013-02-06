import unittest
from client import TroiaClient
from testSettings import TestSettings
import random
import string

class TestCostMatrix(unittest.TestCase):
    
        def generateId(self, length):
            return "".join([random.choice(string.ascii_lowercase) for x in xrange(length)])
        
        def test_CostMatrix_01Values(self):
            categories = [{"name":"porn", "prior":0.3, "misclassificationCost": [{'categoryName': 'porn', 'value': 0.0}, {'categoryName': 'notporn', 'value': 1.0}]}, 
                          {"name":"notporn", "prior":0.7, "misclassificationCost":[{'categoryName': 'porn', 'value': 1.0}, {'categoryName': 'notporn', 'value': 0.0}]}]
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + client.jid, response['result'])
            
            response = client.await_completion(client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(len(categories), len(result))
            for retrievedCategories in result:
                category = str(retrievedCategories).replace('u\'', '\'')
                self.assertTrue(category in str(categories))

        def test_CostMatrix_DoubleValues(self):
            categories = [{"name":"porn", "prior":0.3, "misclassificationCost": [{'categoryName': 'porn', 'value': 0.4}, {'categoryName': 'notporn', 'value': 0.6}]}, 
                          {"name":"notporn", "prior":0.7, "misclassificationCost":[{'categoryName': 'porn', 'value': 0.6}, {'categoryName': 'notporn', 'value': 0.4}]}]
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + client.jid, response['result'])
            
            response = client.await_completion(client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(len(categories), len(result))
            for retrievedCategories in result:
                category = str(retrievedCategories).replace('u\'', '\'')
                self.assertTrue(category in str(categories))
                
        def test_UpdateCostMatrix(self):
            #create a job with some default categories
            categories = [{"name":"porn", "prior":0.5, "misclassificationCost": [{'categoryName': 'porn', 'value': 0.0}, {'categoryName': 'notporn', 'value': 1.0}]}, 
                          {"name":"notporn", "prior":0.5, "misclassificationCost":[{'categoryName': 'porn', 'value': 1.0}, {'categoryName': 'notporn', 'value': 0.0}]}]
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + client.jid, response['result'])
            
            #update the cost matrix
            newCostMatrix = [{"categoryTo":"porn", "cost":0.3, "categoryFrom":"porn"}, {"categoryTo":"porn", "cost":1.7, "categoryFrom":"notporn"}, {"categoryTo":"notporn", "cost":1.7, "categoryFrom":"porn"}, {"categoryTo":"notporn", "cost":0.3, "categoryFrom":"notporn"}]
            
            response = client.await_completion(client.post_cost_matrix(newCostMatrix))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Costs set', response['result'])
            
            #retrieve the cost matrix and check that it is updated correctly
            response = client.await_completion(client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            result = response['result']
            expectedCategories = [{'prior':0.5, 'misclassificationCost': [{'categoryName': 'porn', 'value': 0.3}, {'categoryName': 'notporn', 'value': 1.7}], 'name':'porn'}, 
                                  {'prior':0.5, 'misclassificationCost': [{'categoryName': 'porn', 'value': 1.7}, {'categoryName': 'notporn', 'value': 0.3}], 'name':'notporn'}]
            self.assertEqual(len(expectedCategories), len(result))
            for retrievedCategories in result:
                category = str(retrievedCategories).replace('u\'', '\'')
                self.assertTrue(category in str(expectedCategories))
            
            
            