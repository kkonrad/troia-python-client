import unittest
from client import TroiaClient
from testSettings import TestSettings
import random
import string

class TestCostMatrix(unittest.TestCase):
    
        def generateId(self, length):
            return "".join([random.choice(string.ascii_lowercase) for x in xrange(length)])
        
        def test_CostMatrix_01Values(self):
            jobId = self.generateId(10)
            categories = [{"name":"porn", "prior":0.5,  "misclassification_cost":{"porn":0.0, "notporn":1.0}}, 
                          {"name":"notporn", "prior":0.5, "misclassification_cost":{"porn":1.0, "notporn":0.0}}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_cost_matrix()
            self.assertEqual('OK', response['status'])
            command_id = response['redirect']
            response = client.get_command_status(command_id)
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(len(categories), len(result))
            for retrievedCategories in result:
                category = str(retrievedCategories).replace('u\'', '\'')
                self.assertTrue(category in str(categories))
            
        def test_CostMatrix_DoubleValues(self):
            jobId = self.generateId(10)
            categories = [{"prior":0.3, "name":"porn", "misclassification_cost": { "porn":0.4, "notporn":0.6}}, 
                          {"prior":0.7, "name":"notporn", "misclassification_cost":{"porn":0.6, "notporn":0.4}}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_cost_matrix()
            self.assertEqual('OK', response['status'])
            command_id = response['redirect']
            response = client.get_command_status(command_id)
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(len(categories), len(result))
            for retrievedCategories in result:
                category = str(retrievedCategories).replace('u\'', '\'')
                self.assertTrue(category in str(categories))
                
        def test_UpdateCostMatrix(self):
            #create a job with some default categories
            jobId = self.generateId(10)
            categories = [{"name":"porn", "prior":0.5,  "misclassification_cost":{"porn":0.0, "notporn":1.0}}, 
                          {"name":"notporn", "prior":0.5, "misclassification_cost":{"porn":1.0, "notporn":0.0}}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            #update the cost matrix
            newCostMatrix = [{"categoryTo":"porn", "cost":0.3, "categoryFrom":"porn"}, {"categoryTo":"porn", "cost":1.7, "categoryFrom":"notporn"}, {"categoryTo":"notporn", "cost":1.7, "categoryFrom":"porn"}, {"categoryTo":"notporn", "cost":0.3, "categoryFrom":"notporn"}]
            response = client.post_cost_matrix(newCostMatrix)
            self.assertEqual('OK', response['status'])
            command_id = response['redirect']
            response = client.get_command_status(command_id)
            self.assertEqual('OK', response['status'])
            self.assertEqual('Costs set', response['result'])
            
            #retrieve the cost matrix and check that it is updated correctly
            response = client.get_cost_matrix()
            self.assertEqual('OK', response['status'])
            command_id = response['redirect']
            response = client.get_command_status(command_id)
            result = response['result']
            expectedCategories = [{'prior':0.5, 'name':'porn', 'misclassification_cost': {'notporn': 1.7, 'porn': 0.3}}, 
                                  {'prior':0.5, 'name':'notporn', 'misclassification_cost': {'notporn': 0.3, 'porn': 1.7}}]
            self.assertEqual(len(expectedCategories), len(result))
            for retrievedCategories in result:
                category = str(retrievedCategories).replace('u\'', '\'')
                self.assertTrue(category in str(expectedCategories))
       
            
            
            