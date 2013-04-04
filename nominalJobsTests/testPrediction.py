# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *
import math


class TestPrediction(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        self.client.create(CATEGORIES, costMatrix=COST_MATRIX, categoryPriors=CATEGORY_PRIORS, algorithm=self.algorithm)
        self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
        self.client.await_completion(self.client.post_compute())

    def tearDown(self):
        self.client.delete()

    def _getPredictedCategories(self, method, expectedResults):
        response = self.client.await_completion(self.client.get_objects_prediction(method))
        self.assertEqual('OK', response['status'])
        actualCategories = {}
        for categories in response['result']:
            actualCategories[categories['objectName']] = categories['categoryName']
        self.assertEqual(expectedResults, actualCategories)

    def _getPredictedDataCost(self, costMethod, expectedCosts):
        response = self.client.await_completion(self.client.get_estimated_objects_cost(costMethod))
        self.assertEqual('OK', response['status'])
        actualCosts = {}
        for cost in response['result']:
            actualCosts[cost['objectName']] = cost['value']
        self.assertEqual(expectedCosts, actualCosts)

    def _getPredictedDataQuality(self, costAlgorithm, expectedDataQuality):
        response = self.client.await_completion(self.client.get_estimated_objects_quality(costAlgorithm))
        self.assertEqual('OK', response['status'])
        actualDataQuality = {}
        for dataQuality in response['result']:
            actualDataQuality[dataQuality['objectName']] = dataQuality['value']
        self.assertEqual(expectedDataQuality, actualDataQuality)

    def _getPredictedWorkerQuality(self, costAlgorithm, expectedWorkerQuality):
        response = self.client.await_completion(self.client.get_estimated_workers_quality(costAlgorithm))
        self.assertEqual('OK', response['status'])
        actualWorkerQuality = {}
        for workerQuality in response['result']:
            actualWorkerQuality[workerQuality['workerName']] = workerQuality['value']
        self.assertEqual(expectedWorkerQuality, actualWorkerQuality)

    def _getEvaluatedDataCost(self, labelChoosingMethod):
        response = self.client.await_completion(self.client.get_evaluated_objects_cost(labelChoosingMethod))
        self.assertEqual('OK', response['status'])
        self.assertEqual([], response['result'])

    def _getEvaluatedDataQuality(self, labelChoosingMethod):
        response = self.client.await_completion(self.client.get_evaluated_objects_quality(labelChoosingMethod))
        self.assertEqual('OK', response['status'])
        self.assertEqual([], response['result'])

    def _getEvaluatedWorkerQuality(self, costAlgorithm):
        response = self.client.await_completion(self.client.get_evaluated_workers_quality(costAlgorithm))
        self.assertEqual('OK', response['status'])
        for workerQuality in response['result']:
            self.assertTrue(math.isnan(workerQuality['value']))

    def _getCategoryProbability(self, expectedProbabilities):
        for object in set((x[1] for x in ASSIGNED_LABELS)):
            response = self.client.await_completion(self.client.get_probability_distribution(object))
            self.assertEqual('OK', response['status'])
            self.assertEqual(expectedProbabilities[object], response['result'])

class TestPredictionMV(TestPrediction):

    algorithm = "BMV"

    def test_GetCategoryProbability(self):
        expectedProbabilities = {'url1': [{u'categoryName': u'porn', u'value': 0.4}, {u'categoryName': u'notporn', u'value': 0.6000000000000001}],
                                 'url2': [{u'categoryName': u'porn', u'value': 0.8}, {u'categoryName': u'notporn', u'value': 0.2}],
                                 'url3': [{u'categoryName': u'porn', u'value': 0.4}, {u'categoryName': u'notporn', u'value': 0.6000000000000001}],
                                 'url4': [{u'categoryName': u'porn', u'value': 0.8}, {u'categoryName': u'notporn', u'value': 0.2}],
                                 'url5': [{u'categoryName': u'porn', u'value': 0.6000000000000001}, {u'categoryName': u'notporn', u'value': 0.4}]} 
        self._getCategoryProbability(expectedProbabilities)

    def test_GetPredictedDataCost_ExpectedCost(self):
        expectedCosts = {'url1':0.4800000000000001, 'url2':0.32000000000000006, 'url3':0.4800000000000001, 'url4':0.32000000000000006, 'url5':0.4800000000000001 }
        self._getPredictedDataCost("ExpectedCost", expectedCosts)

    def test_GetPredictedDataCost_MinCost(self):
        expectedCosts = {'url1':0.4, 'url2':0.2, 'url3':0.4, 'url4':0.2, 'url5':0.4}
        self._getPredictedDataCost("MinCost", expectedCosts)

    def test_GetPredictedDataQuality_ExpectedCost(self):
        expectedDataQuality = {'url1':0.039999999999999813, 'url2':0.3599999999999999, 'url3':0.039999999999999813, 'url4':0.3599999999999999, 'url5':0.039999999999999813}
        self._getPredictedDataQuality("ExpectedCost", expectedDataQuality)

    def test_GetPredictedDataQuality_MinCost(self):
        expectedDataQuality = {'url1':0.19999999999999996, 'url2':0.6, 'url3':0.19999999999999996, 'url4':0.6, 'url5':0.19999999999999996}
        self._getPredictedDataQuality("MinCost", expectedDataQuality)

    def test_GetPredictedCategories_MaxLikelihood(self):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'porn'}
        self._getPredictedCategories("MaxLikelihood", expectedCategories)

    def test_GetPredictedCategories_MinCost(self):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'porn'}
        self._getPredictedCategories("MinCost", expectedCategories)


class TestPredictionIDS(TestPrediction):

    algorithm = "IDS"

    def test_GetPredictedCategories_MaxLikelihood(self):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'notporn'}
        self._getPredictedCategories("MaxLikelihood", expectedCategories)

    def test_GetPredictedCategories_MinCost(self):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'notporn'}
        self._getPredictedCategories("MinCost", expectedCategories)


class TestPredictionBDS(TestPrediction):

    algorithm = "BDS"

    def test_GetCategoryProbability(self):
        expectedProbabilities = {'url1': [{u'categoryName': u'porn', u'value': 0.0}, {u'categoryName': u'notporn', u'value': 1.0}],
                                 'url2': [{u'categoryName': u'porn', u'value': 1.0}, {u'categoryName': u'notporn', u'value': 0.0}],
                                 'url3': [{u'categoryName': u'porn', u'value': 0.0}, {u'categoryName': u'notporn', u'value': 1.0}],
                                 'url4': [{u'categoryName': u'porn', u'value': 1.0}, {u'categoryName': u'notporn', u'value': 0.0}],
                                 'url5': [{u'categoryName': u'porn', u'value': 0.0}, {u'categoryName': u'notporn', u'value': 1.0}]} 
        self._getCategoryProbability(expectedProbabilities)

    def test_GetPredictedCategories_MaxLikelihood(self):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'notporn'}
        self._getPredictedCategories("MaxLikelihood", expectedCategories)

    def test_GetPredictedCategories_MinCost(self):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'notporn'}
        self._getPredictedCategories("MinCost", expectedCategories)

    def test_GetPredictedDataQuality_ExpectedCost(self):
        #Not good
        expectedDataQuality = {'url1':1.0, 'url2':1.0, 'url3':1.0, 'url4':1.0, 'url5':1.0}
        self._getPredictedDataQuality("ExpectedCost", expectedDataQuality)

    def test_GetPredictedDataQuality_MinCost(self):
        #Not good
        expectedDataQuality = {'url1':1.0, 'url2':1.0, 'url3':1.0, 'url4':1.0, 'url5':1.0}
        self._getPredictedDataQuality("MinCost", expectedDataQuality)

    def test_GetPredictedWorkersQuality_ExpectedCost(self):
        expectedWorkerQuality = {'worker1':0.0, 'worker2':0.4444444444444444, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0}
        self._getPredictedWorkerQuality("ExpectedCost", expectedWorkerQuality)

    def test_GetPredictedWorkersQuality_MaxLikelihood(self):
        expectedWorkerQuality = {'worker1':0.0, 'worker2':0.6666666666666667, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0}
        self._getPredictedWorkerQuality("MaxLikelihood", expectedWorkerQuality)

    def test_GetPredictedWorkersQuality_MinCost(self):
        expectedWorkerQuality = {'worker1':0.0, 'worker2':0.6666666666666667, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0}
        self._getPredictedWorkerQuality("MinCost", expectedWorkerQuality)

    def test_GetPredictedDataCost_ExpectedCost(self):
        #This is not good at all 
        expectedCosts = {'url1':0.0, 'url2':0.0, 'url3':0.0, 'url4':0.0, 'url5':0.0 }
        self._getPredictedDataCost("ExpectedCost", expectedCosts)

    def test_GetPredictedDataCost_MinCost(self):
        #This is also not good at all 
        expectedCosts = {'url1':0.0, 'url2':0.0, 'url3':0.0, 'url4':0.0, 'url5':0.0 }
        self._getPredictedDataCost("MinCost", expectedCosts)

    def testGetPredictionZip(self):
        response = self.client.await_completion(self.client.get_prediction_zip())
        self.assertEqual('OK', response['status'])
        self.assertTrue('/media/downloads/' in response['result'])

    def test_GetEvaluatedDataCosts_NoEvaluationData(self):
        for labelChoosingMethod in ["MaxLikelihood", "MinCost"]:
            self._getEvaluatedDataCost(labelChoosingMethod)

    def test_GetEvaluatedDataQuality_NoEvaluationData(self):
        for labelChoosingMethod in ["MaxLikelihood", "MinCost"]:
            self._getEvaluatedDataCost(labelChoosingMethod)

    def test_GetEvaluatedWorkersQuality_NoEvaluationData(self):
        costAlgorithms = ["ExpectedCost", "MaxLikelihood", "MinCost"] 
        for costAlgorithm in costAlgorithms:
            self._getEvaluatedWorkerQuality(costAlgorithm)
