# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *
import math


class TestPrediction(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        self.client.create(CATEGORIES)
        self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
        self.client.await_completion(self.client.post_compute())

    def tearDown(self):
        self.client.delete()

    def _getPredictedCategories(self, algorithm, method, expectedResults):
        response = self.client.await_completion(self.client.get_predictions_objects(algorithm, method))
        self.assertEqual('OK', response['status'])
        actualCategories = {}
        for categories in response['result']:
            actualCategories[categories['objectName']] = categories['categoryName']
        self.assertEqual(expectedResults, actualCategories)

    def _getPredictedDataCost(self, algorithm, costMethod, expectedCosts):
        response = self.client.await_completion(self.client.get_prediction_data_cost(algorithm, costMethod))
        self.assertEqual('OK', response['status'])
        actualCosts = {}
        for cost in response['result']:
            actualCosts[cost['objectName']] = cost['value']
        self.assertEqual(expectedCosts, actualCosts)

    def _getPredictedDataQuality(self, algorithm, costAlgorithm, expectedDataQuality):
        response = self.client.await_completion(self.client.get_prediction_data_quality(algorithm, costAlgorithm))
        self.assertEqual('OK', response['status'])
        actualDataQuality = {}
        for dataQuality in response['result']:
            actualDataQuality[dataQuality['objectName']] = dataQuality['value']
        self.assertEqual(expectedDataQuality, actualDataQuality)

    def _getPredictedWorkerQuality(self, costAlgorithm, expectedWorkerQuality):
        response = self.client.await_completion(self.client.get_prediction_workers_quality(costAlgorithm))
        self.assertEqual('OK', response['status'])
        actualWorkerQuality = {}
        for workerQuality in response['result']:
            actualWorkerQuality[workerQuality['workerName']] = workerQuality['value']
        self.assertEqual(expectedWorkerQuality, actualWorkerQuality)

    def _getEvaluatedDataCost(self, algorithm, labelChoosingMethod):
        response = self.client.await_completion(self.client.get_evaluation_data_cost(algorithm, labelChoosingMethod))
        self.assertEqual('OK', response['status'])
        self.assertEqual([], response['result'])

    def _getEvaluatedDataQuality(self, algorithm, labelChoosingMethod):
        response = self.client.await_completion(self.client.get_evaluation_data_quality(algorithm, labelChoosingMethod))
        self.assertEqual('OK', response['status'])
        self.assertEqual([], response['result'])

    def _getEvaluatedWorkerQuality(self, costAlgorithm):
        response = self.client.await_completion(self.client.get_evaluation_workers_quality(costAlgorithm))
        self.assertEqual('OK', response['status'])
        for workerQuality in response['result']:
            self.assertTrue(math.isnan(workerQuality['value']))

    def testGetPredictionZip(self):
        response = self.client.await_completion(self.client.get_prediction_zip())
        self.assertEqual('OK', response['status'])
        self.assertTrue('/media/downloads/' in response['result'])

    def test_GetPredictedCategories_DS_MaxLikelihood(self):
        expectedCategories = {'url1':'porn', 'url2':'notporn', 'url3':'porn', 'url4':'notporn', 'url5':'porn'}
        self._getPredictedCategories("DS", "MaxLikelihood", expectedCategories)

    def test_GetPredictedCategories_DS_MinCost(self):
        expectedCategories = {'url1':'porn', 'url2':'notporn', 'url3':'porn', 'url4':'notporn', 'url5':'porn'}
        self._getPredictedCategories("DS", "MinCost", expectedCategories)

    def test_GetPredictedCategories_MV_MaxLikelihood(self):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'porn'}
        self._getPredictedCategories("MV", "MaxLikelihood", expectedCategories)

    def test_GetPredictedCategories_MV_MinCost(self):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'porn'}
        self._getPredictedCategories("MV", "MinCost", expectedCategories)

    def test_GetPredictedDataCost_DS_ExpectedCost(self):
        #This is not good at all 
        expectedCosts = {'url1':0.0, 'url2':0.0, 'url3':0.0, 'url4':0.0, 'url5':0.0 }
        self._getPredictedDataCost("DS", "ExpectedCost", expectedCosts)

    def test_GetPredictedDataCost_DS_MinCost(self):
        #This is also not good at all 
        expectedCosts = {'url1':0.0, 'url2':0.0, 'url3':0.0, 'url4':0.0, 'url5':0.0 }
        self._getPredictedDataCost("DS", "MinCost", expectedCosts)

    def test_GetPredictedDataCost_MV_ExpectedCost(self):
        expectedCosts = {'url1':0.4800000000000001, 'url2':0.32000000000000006, 'url3':0.4800000000000001, 'url4':0.32000000000000006, 'url5':0.4800000000000001 }
        self._getPredictedDataCost("MV", "ExpectedCost", expectedCosts)

    def test_GetPredictedDataCost_MV_MinCost(self):
        expectedCosts = {'url1':0.4, 'url2':0.2, 'url3':0.4, 'url4':0.2, 'url5':0.4}
        self._getPredictedDataCost("MV", "MinCost", expectedCosts)

    def test_GetPredictedDataQuality_DS_ExpectedCost(self):
        #Not good
        expectedDataQuality = {'url1':1.0, 'url2':1.0, 'url3':1.0, 'url4':1.0, 'url5':1.0}
        self._getPredictedDataQuality("DS", "ExpectedCost", expectedDataQuality)

    def test_GetPredictedDataQuality_DS_MinCost(self):
        #Not good
        expectedDataQuality = {'url1':1.0, 'url2':1.0, 'url3':1.0, 'url4':1.0, 'url5':1.0}
        self._getPredictedDataQuality("DS", "MinCost", expectedDataQuality)

    def test_GetPredictedDataQuality_MV_ExpectedCost(self):
        expectedDataQuality = {'url1':0.039999999999999813, 'url2':0.3599999999999999, 'url3':0.039999999999999813, 'url4':0.3599999999999999, 'url5':0.039999999999999813}
        self._getPredictedDataQuality("MV", "ExpectedCost", expectedDataQuality)

    def test_GetPredictedDataQuality_MV_MinCost(self):
        expectedDataQuality = {'url1':0.19999999999999996, 'url2':0.6, 'url3':0.19999999999999996, 'url4':0.6, 'url5':0.19999999999999996}
        self._getPredictedDataQuality("MV", "MinCost", expectedDataQuality)

    def test_GetPredictedWorkersQuality_ExpectedCost(self):
        expectedWorkerQuality = {'worker1':0.0, 'worker2':0.4444444444444444, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0}
        self._getPredictedWorkerQuality("ExpectedCost", expectedWorkerQuality)

    def test_GetPredictedWorkersQuality_MaxLikelihood(self):
        expectedWorkerQuality = {'worker1':0.0, 'worker2':0.6666666666666667, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0}
        self._getPredictedWorkerQuality("MaxLikelihood", expectedWorkerQuality)

    def test_GetPredictedWorkersQuality_MinCost(self):
        expectedWorkerQuality = {'worker1':0.0, 'worker2':0.6666666666666667, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0}
        self._getPredictedWorkerQuality("MinCost", expectedWorkerQuality)

    def test_GetEvaluatedDataCosts_NoEvaluationData(self):
        algos = [("DS","MaxLikelihood"), ("DS","MinCost"), ("MV","MaxLikelihood"), ("DS","MinCost")] 
        for algo, labelChoosingMethod in algos:
            self._getEvaluatedDataCost(algo, labelChoosingMethod)

    def test_GetEvaluatedDataQuality_NoEvaluationData(self):
        algos = [("DS","MaxLikelihood"), ("DS","MinCost"), ("MV","MaxLikelihood"), ("DS","MinCost")] 
        for algo, labelChoosingMethod in algos:
            self._getEvaluatedDataCost(algo, labelChoosingMethod)

    def test_GetEvaluatedWorkersQuality_NoEvaluationData(self):
        costAlgorithms = ["ExpectedCost", "MaxLikelihood", "MinCost"] 
        for costAlgorithm in costAlgorithms:
            self._getEvaluatedWorkerQuality(costAlgorithm)