import unittest
from client import TroiaClient
from testSettings import *

class TestJobs(unittest.TestCase):   
    
        def setUp(self):
            self.client = TroiaClient(ADDRESS)
            
        def tearDown(self):
            self.client.delete()
        
        def assertJobData(self, response, expDSKind, expNoAssigns, expNoGoldObjects, expNoObjects, expNoWorkers):
            self.assertEqual('OK', response['status'])
            self.assertEqual(expDSKind, response['result']['DS kind'])
            self.assertEqual(expNoAssigns, response['result']['Number of assigns'])
            self.assertEqual(expNoGoldObjects, response['result']['Number of gold objects'])
            self.assertEqual(expNoObjects, response['result']['Number of objects'])
            self.assertEqual(expNoWorkers, response['result']['Number of workers'])
            
        def test_createJob_NoJobType(self):
            response = self.client.create(CATEGORIES)
            print response
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])
            
            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')

        def test_createJob_BatchJobType(self):
            response = self.client.create(CATEGORIES, 'batch')
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])
            
            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])           
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
   
        def test_createJob_IncrementalJobType(self):
            response = self.client.create(CATEGORIES, 'incremental')
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])
            
            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.IncrementalDawidSkene', '0', '0', '0', '0')

        def test_createJob_WrongJobType(self):
            response = self.client.create(CATEGORIES, 'test')
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Unknown Job type: test', response['result'])
                    
        def test_createJob_NoCategories(self):
            response = self.client.create()
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('You should provide categories list', response['result'])
        
        def test_createJob_EmptyCategories(self):
            response = self.client.create([])
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('There should be at least two categories', response['result'])
                   
        def test_createJob_SumOfPriorsLessThanOne_NoCostMatrix(self):
            categories = [{"prior":"0.3", "name":"porn"}, {"prior":"0.5", "name":"notporn"}]
            response = self.client.create(categories)
            self.assertEqual('ERROR', response['status']) 
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])
        
        def test_createJob_SumOfPriorsGreaterThanOne_NoCostMatrix(self):
            categories = [{"prior":"0.6", "name":"porn"}, {"prior":"0.5", "name":"notporn"}]
            response = self.client.create(categories)
            self.assertEqual('ERROR', response['status']) 
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])
        
        def test_createJob_SumOfPriorsEqualsOne_NoCostMatrix(self):
            categories = [{"prior":"0.234", "name":"porn"}, {"prior":"0.766", "name":"notporn"}]
            response = self.client.create(categories)
            print response
            self.assertEqual('OK', response['status']) 
            
            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])          
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
                    
        def test_createJob_SumOfPriorsLessThanOne_WithCostMatrix(self):
            categories = [{"prior":"0.3", "name":"porn", "misclassificationCost": [{'categoryName': 'porn', 'value': 0}, {'categoryName': 'notporn', 'value': 1}]}, 
                          {"prior":"0.5", "name":"notporn", "misclassificationCost":[{'categoryName': 'porn', 'value': 1}, {'categoryName': 'notporn', 'value': 0}]}]
            response = self.client.create(categories)
            self.assertEqual('ERROR', response['status']) 
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])
        
        def test_createJob_SumOfPriorsGreaterThanOne_WithCostMatrix(self):
            categories = [{"prior":"0.5", "name":"porn", "misclassificationCost": [{'categoryName': 'porn', 'value': 0}, {'categoryName': 'notporn', 'value': 1}]}, 
                          {"prior":"0.52", "name":"notporn", "misclassificationCost":[{'categoryName': 'porn', 'value': 1}, {'categoryName': 'notporn', 'value': 0}]}]
            response = self.client.create(categories)
            self.assertEqual('ERROR', response['status']) 
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])
        
        def test_createJob_SumOfPriorsEqualsOne_WithCostMatrix(self):
            categories = [{"prior":"0.1234", "name":"porn", "misclassificationCost": [{'categoryName': 'porn', 'value': 0}, {'categoryName': 'notporn', 'value': 1}]}, 
                          {"prior":"0.8766", "name":"notporn", "misclassificationCost":[{'categoryName': 'porn', 'value': 1}, {'categoryName': 'notporn', 'value': 0}]}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status']) 
            
            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])            
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
            
        def test_createJob_NoPriors_NoCostMatrix(self):
            categories = [{"name":"porn"}, {"name":"notporn"}]

            response = self.client.create(categories)
            self.assertEqual('OK', response['status']) 

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])       
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
        
        def test_createJob_NoPriors_WithCostMatrix(self):
            categories = [{"name":"porn", "misclassificationCost": [{'categoryName': 'porn', 'value': 0}, {'categoryName': 'notporn', 'value': 1}]}, 
                          {"name":"notporn", "misclassificationCost":[{'categoryName': 'porn', 'value': 1}, {'categoryName': 'notporn', 'value': 0}]}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status']) 
            
            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])          
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
        
        def test_deleteJob_ExistingJobId(self):
            response = self.client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + self.client.jid, response['result'])
            
            response = self.client.delete()
            self.assertEqual('OK', response['status'])
            self.assertEqual('Removed job with ID: ' + self.client.jid, response['result'])
