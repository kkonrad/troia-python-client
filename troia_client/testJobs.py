import unittest
from client import TroiaClient
from testSettings import TestSettings
import random
import string

class TestJobs(unittest.TestCase):
    
        def generateId(self, length):
            return "".join([random.choice(string.ascii_lowercase) for x in xrange(length)])
        
        def assertJobData(self, response, expDSKind, expNoAssigns, expNoGoldObjects, expNoObjects, expNoWorkers):
            self.assertEqual('OK', response['status'])
            self.assertEqual(expDSKind, response['result']['DS kind'])
            self.assertEqual(expNoAssigns, response['result']['Number of assigns'])
            self.assertEqual(expNoGoldObjects, response['result']['Number of gold objects'])
            self.assertEqual(expNoObjects, response['result']['Number of objects'])
            self.assertEqual(expNoWorkers, response['result']['Number of workers'])
            
        def test_createJob_NoJobId_NoJobType(self):
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(TestSettings.CATEGORIES)
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
            
        def test_createJob_NoJobId_BatchJobType(self):
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(TestSettings.CATEGORIES, 'batch')
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])           
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
            
        def test_createJob_NoJobId_IncrementalJobType(self):
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(TestSettings.CATEGORIES, 'incremental')
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.IncrementalDawidSkene', '0', '0', '0', '0')
        
        def test_createJob_NoJobId_WrongJobType(self):
            client = TroiaClient(TestSettings.ADDRESS)
            response = client.createNewJob(TestSettings.CATEGORIES, 'test')
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Unknown Job type: test', response['result'])
            
        def test_createJob_GivenJobId_NoJobType(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(TestSettings.CATEGORIES)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])           
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
        
        def test_createJob_GivenJobId_BatchJobType(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(TestSettings.CATEGORIES, 'batch')
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])         
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
            
        def test_createJob_GivenJobId_IncrementalJobType(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(TestSettings.CATEGORIES, 'incremental')
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])         
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.IncrementalDawidSkene', '0', '0', '0', '0')

        def test_createJob_GivenJobId_WrongJobType(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(TestSettings.CATEGORIES, 'test')
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Unknown Job type: test', response['result'])

        def test_createJob_AlreadyExistingJobId(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            client.createNewJob([])
            response = client.createNewJob(TestSettings.CATEGORIES)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Job with ID ' + jobId + ' already exists', response['result']) 
                        
        def test_createJob_GivenJobId_NoCategories(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob()
            self.assertEqual('ERROR', response['status'])
            self.assertFalse('Internal error' in response['result'])
        
        def test_createJob_GivenJobId_EmptyCategories(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob([])
            self.assertEqual('ERROR', response['status'])
                   
        def test_createJob_SumOfPriorsLessThanOne_NoCostMatrix(self):
            jobId = self.generateId(10).join('job')
            categories = [{"prior":"0.3", "name":"porn"}, {"prior":"0.5", "name":"notporn"}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('ERROR', response['status']) 
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])
        
        def test_createJob_SumOfPriorsGreaterThanOne_NoCostMatrix(self):
            jobId = self.generateId(10).join('job')
            categories = [{"prior":"0.6", "name":"porn"}, {"prior":"0.5", "name":"notporn"}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('ERROR', response['status']) 
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])
        
        def test_createJob_SumOfPriorsEqualsOne_NoCostMatrix(self):
            jobId = self.generateId(10).join('job')
            categories = [{"prior":"0.234", "name":"porn"}, {"prior":"0.766", "name":"notporn"}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status']) 
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])          
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
                    
        def test_createJob_SumOfPriorsLessThanOne_WithCostMatrix(self):
            jobId = self.generateId(10).join('job')
            categories = [{"prior":"0.3", "name":"porn", "misclassification_cost": { "porn":"0", "notporn":"1"}}, {"prior":"0.5", "name":"notporn", "misclassification_cost": { "porn":"1", "notporn":"0"}}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('ERROR', response['status']) 
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])
        
        def test_createJob_SumOfPriorsGreaterThanOne_WithCostMatrix(self):
            jobId = self.generateId(10).join('job')
            categories = [{"prior":"0.81", "name":"porn", "misclassification_cost": { "porn":"0", "notporn":"1"}}, {"prior":"0.5", "name":"notporn", "misclassification_cost": { "porn":"1", "notporn":"0"}}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('ERROR', response['status']) 
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])
        
        def test_createJob_SumOfPriorsEqualsOne_WithCostMatrix(self):
            jobId = self.generateId(10).join('job')
            categories = [{"prior":"0.1234", "name":"porn", "misclassification_cost": { "porn":"0", "notporn":"1"}}, {"prior":"0.8766", "name":"notporn", "misclassification_cost": { "porn":"1", "notporn":"0"}}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status']) 
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])            
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
            
        def test_createJob_NoPriors_NoCostMatrix(self):
            jobId = self.generateId(10).join('job')
            categories = [{"prior":"0.1234", "name":"porn"}, {"prior":"0.8766", "name":"notporn"}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status']) 
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])       
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
        
        def test_createJob_NoPriors_WithCostMatrix(self):
            jobId = self.generateId(10).join('job')
            categories = [{"name":"porn", "misclassification_cost": { "porn":"0", "notporn":"1"}}, {"name":"notporn", "misclassification_cost": { "porn":"1", "notporn":"0"}}]
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(categories)
            self.assertEqual('OK', response['status']) 
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.get_job_status()
            self.assertEqual('OK', response['status'])          
            response = client.get_command_status(response['redirect'])
            self.assertJobData(response, 'class com.datascience.gal.BatchDawidSkene', '0', '0', '0', '0')
        
        def test_deleteJob_ExistingJobId(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(TestSettings.CATEGORIES)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.delete()
            self.assertEqual('OK', response['status'])
            self.assertEqual('Removed job with ID: ' + jobId, response['result'])
            
        def test_deleteJob_NonExistingJobId(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(TestSettings.CATEGORIES)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + jobId, response['result'])
            
            response = client.delete()
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Job with ID ' + jobId + ' does not exist', response['result'])
            

