import unittest
from client.gal import TroiaClient
from testSettings import *
import time


class TestJobs(unittest.TestCase):

        def setUp(self):
            self.client = TroiaClient(ADDRESS)

        def tearDown(self):
            self.client.delete()

        def assertJobData(self, response, expAlgorithm, expNoAssigns, expNoGoldObjects, expNoObjects, expNoWorkers):
            self.assertEqual('OK', response['status'])
            self.assertEqual(expAlgorithm, response['result']['Initialization data']['algorithm'])
            self.assertEqual(expNoAssigns, response['result']['Number of assigns'])
            self.assertEqual(expNoGoldObjects, response['result']['Number of gold objects'])
            self.assertEqual(expNoObjects, response['result']['Number of objects'])
            self.assertEqual(expNoWorkers, response['result']['Number of workers'])

        def test_createJob_NoJobType(self):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS)
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'BDS', 0, 0, 0, 0)

        def test_createJob_BDSJobType(self):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS, algorithm='BDS')
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])

            response = self.client.get_job_status()
            jobStatus = response['status']
            if (jobStatus == 'NOT READY'):
                time.sleep(5)
                response = self.client.get_job_status()
                jobStatus = response['status']

            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'BDS', 0, 0, 0, 0)

        def test_createJob_IDSJobType(self):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS, algorithm='IDS')
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'IDS', 0, 0, 0, 0)

        def test_createJob_BMVJobType(self):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS, algorithm='BMV')
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'BMV', 0, 0, 0, 0)

        def test_createJob_IMVJobType(self):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS, algorithm='IMV')
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'IMV', 0, 0, 0, 0)

        def test_createJob_WrongJobType(self):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS, algorithm='test')
            self.assertEqual('ERROR', response['status'])
            self.assertTrue('Unknown Job' in response['result'])

        def test_createJob_EmptyCategories(self):
            response = self.client.create([])
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('There should be at least two categories', response['result'])

        def get_priors(self, categories, priors):
            return [{'categoryName': c, "value": p} for c, p in zip(categories, priors)]
            
        def test_createJob_SumOfPriorsLessThanOne_NoCostMatrix(self):
            categories = ["porn", "notporn"]
            priors = [0.3, 0.5]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors))
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])

        def test_createJob_SumOfPriorsGreaterThanOne_NoCostMatrix(self):
            categories = ["porn", "notporn"]
            priors = [0.6, 0.5]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors))
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])

        def test_createJob_SumOfPriorsEqualsOne_NoCostMatrix(self):
            categories = ["porn", "notporn"]
            priors = [0.234, 0.766]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors))
            self.assertEqual('OK', response['status'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'BDS', 0, 0, 0, 0)

        def test_createJob_SumOfPriorsLessThanOne_WithCostMatrix(self):
            categories = ["porn", "notporn"]
            priors = [0.3, 0.5]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), costMatrix=COST_MATRIX)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])

        def test_createJob_SumOfPriorsGreaterThanOne_WithCostMatrix(self):
            categories = ["porn", "notporn"]
            priors = [0.6, 0.5]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), costMatrix=COST_MATRIX)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])

        def test_createJob_SumOfPriorsEqualsOne_WithCostMatrix(self):
            categories = ["porn", "notporn"]
            priors = [0.1234, 0.8766]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), costMatrix=COST_MATRIX)
            self.assertEqual('OK', response['status'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'BDS', 0, 0, 0, 0)

        def test_createJob_NoPriors_NoCostMatrix(self):
            categories = ["porn", "notporn"]

            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'BDS', 0, 0, 0, 0)

        def test_createJob_NoPriors_WithCostMatrix(self):
            categories = ['porn', 'notporn']
            response = self.client.create(categories, costMatrix=COST_MATRIX)
            self.assertEqual('OK', response['status'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, 'BDS', 0, 0, 0, 0)

        def test_deleteJob_ExistingJobId(self):
            response = self.client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + self.client.jid, response['result'])

            response = self.client.delete()
            self.assertEqual('OK', response['status'])
            self.assertEqual('Removed job with ID: ' + self.client.jid, response['result'])
