import unittest
from client.gal import TroiaClient
from ddt import ddt, data
from testSettings import *
import time

@ddt
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
            self.assertEqual('ERROR', response['status'])
            print response

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob(self, algorithm):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS, algorithm=algorithm)
            self.assertEqual('OK', response['status'])
            self.assertTrue('New job created with ID: RANDOM_' in response['result'])

            response = self.client.get_job_status()
            jobStatus = response['status']
            if (jobStatus == 'NOT_READY'):
                time.sleep(5)
                response = self.client.get_job_status()
                jobStatus = response['status']

            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, algorithm, 0, 0, 0, 0)

        def test_createJob_WrongJobType(self):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS, algorithm='test')
            self.assertEqual('ERROR', response['status'])
            self.assertTrue('Unknown Job' in response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_NoCategories(self, algorithm):
            response = self.client.create(None, algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('There is no categories collection', response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_EmptyCategories(self, algorithm):
            response = self.client.create([], algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('There should be at least two categories', response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_2Categories_SameCategoryNames(self, algorithm):
            categories = [u'category1', u'category1']
            response = self.client.create(categories, algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Category names should be different', response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_3Categries_SameCategoryNames(self, algorithm):
            categories = [u'category1', u'category1', u'category2']
            response = self.client.create(categories, algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Category names should be different', response['result'])

        def get_priors(self, categories, priors):
            return [{'categoryName': c, "value": p} for c, p in zip(categories, priors)]

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_SumOfPriorsLessThanOne_NoCostMatrix(self, algorithm):
            categories = ["porn", "notporn"]
            priors = [0.3, 0.5]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_SumOfPriorsGreaterThanOne_NoCostMatrix(self, algorithm):
            categories = ["porn", "notporn"]
            priors = [0.6, 0.5]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_SumOfPriorsEqualsOne_NoCostMatrix(self, algorithm):
            categories = ["porn", "notporn"]
            priors = [0.234, 0.766]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), algorithm=algorithm)
            self.assertEqual('OK', response['status'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, algorithm, 0, 0, 0, 0)

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_SumOfPriorsLessThanOne_WithCostMatrix(self, algorithm):
            categories = ["porn", "notporn"]
            priors = [0.3, 0.5]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), costMatrix=COST_MATRIX, algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_SumOfPriorsGreaterThanOne_WithCostMatrix(self, algorithm):
            categories = ["porn", "notporn"]
            priors = [0.6, 0.5]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), costMatrix=COST_MATRIX, algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Priors should sum up to 1. or not to be given (therefore we initialize the priors to be uniform across classes)', response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_SumOfPriorsEqualsOne_WithCostMatrix(self, algorithm):
            categories = ["porn", "notporn"]
            priors = [0.1234, 0.8766]
            response = self.client.create(categories, categoryPriors=self.get_priors(categories, priors), costMatrix=COST_MATRIX, algorithm=algorithm)
            self.assertEqual('OK', response['status'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, algorithm, 0, 0, 0, 0)

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_NoPriors_NoCostMatrix(self, algorithm):
            categories = ["porn", "notporn"]

            response = self.client.create(categories, algorithm=algorithm)
            self.assertEqual('OK', response['status'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, algorithm, 0, 0, 0, 0)

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_NoPriors_WithCostMatrix(self, algorithm):
            categories = ['porn', 'notporn']
            response = self.client.create(categories, costMatrix=COST_MATRIX, algorithm=algorithm)
            self.assertEqual('OK', response['status'])

            response = self.client.get_job_status()
            self.assertEqual('OK', response['status'])
            response = self.client.get_status(response['redirect'])
            self.assertJobData(response, algorithm, 0, 0, 0, 0)

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_createJob_CostMatrixContainsNotExistingCategories(self, algorithm):
            categories = [u'category1', u'category2']
            response = self.client.create(categories, costMatrix=COST_MATRIX, algorithm=algorithm)
            self.assertEqual('ERROR', response['status'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_deleteJob_ExistingJobId(self, algorithm):
            response = self.client.create(CATEGORIES, algorithm=algorithm)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + self.client.jid, response['result'])

            response = self.client.delete()
            self.assertEqual('OK', response['status'])
            self.assertEqual('Removed job with ID: ' + self.client.jid, response['result'])

        @data('BDS', 'IDS', 'BMV', 'IMV')
        def test_deleteJob_NonExistingJobId(self, algorithm):
            response = self.client.create(CATEGORIES, algorithm=algorithm)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + self.client.jid, response['result'])

            response = self.client.delete('NotExistingJob')
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Job with ID NotExistingJob does not exist', response['result'])
