# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *
import math
from nominalJobsTests.testSettings import EVALUATION_DATA
from ddt import ddt, data


class TestPrediction(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        self.client.create(CATEGORIES, costMatrix=COST_MATRIX, categoryPriors=CATEGORY_PRIORS, algorithm=self.algorithm)
        self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
        self.client.await_completion(self.client.post_evaluation_objects(EVALUATION_DATA))
        self.client.await_completion(self.client.post_compute())

    def tearDown(self):
        self.client.delete()

    def _getObjectsPrediction(self, method, expectedResults):
        response = self.client.await_completion(self.client.get_objects_prediction(method))
        self.assertEqual('OK', response['status'])
        for categories in response['result']:
            self.assertAlmostEqual(expectedResults[categories['objectName']], categories['categoryName'])

    def _getEstimatedObjectsCost(self, costMethod, expectedCosts):
        response = self.client.await_completion(self.client.get_estimated_objects_cost(costMethod))
        self.assertEqual('OK', response['status'])
        for cost in response['result']:
            self.assertAlmostEqual(expectedCosts[cost['objectName']], cost['value'])

    def _getEvaluatedObjectsCost(self, labelChoosingMethod, expectedResults):
        response = self.client.await_completion(self.client.get_evaluated_objects_cost(labelChoosingMethod))
        self.assertEqual('OK', response['status'])
        for item in response['result']:
            self.assertEqual(expectedResults[item['objectName']], item['value'])

    def _getEstimatedObjectsQuality(self, costAlgorithm, expectedDataQuality):
        response = self.client.await_completion(self.client.get_estimated_objects_quality(costAlgorithm))
        self.assertEqual('OK', response['status'])
        for dataQuality in response['result']:
            self.assertEqual(expectedDataQuality[dataQuality['objectName']], dataQuality['value'])

    def _getEvaluatedObjectsQuality(self, labelChoosingMethod, expectedResults):
        response = self.client.await_completion(self.client.get_evaluated_objects_quality(labelChoosingMethod))
        self.assertEqual('OK', response['status'])
        for item in response['result']:
            self.assertEqual(expectedResults[item['objectName']], item['value'])

    def _getEstimatedObjectsCostSummary (self, expectedObjectsCosts):
        response = self.client.await_completion(self.client.get_objects_cost_estimated_summary())
        self.assertEqual('OK', response['status'])
        for k, v in expectedObjectsCosts.items():
            self.assertAlmostEqual(expectedObjectsCosts[k], response['result'][k])

    def _getEvaluatedObjectsCostSummary (self, expectedObjectsCosts):
        response = self.client.await_completion(self.client.get_objects_cost_evaluated_summary())
        self.assertEqual('OK', response['status'])
        for k, v in expectedObjectsCosts.items():
            self.assertEqual(expectedObjectsCosts[k], response['result'][k])

    def _getEstimatedObjectsQualitySummary(self, expectedDataQuality):
        response = self.client.await_completion(self.client.get_objects_quality_estimated_summary())
        self.assertEqual('OK', response['status'])
        for k, v in expectedDataQuality.items():
            self.assertAlmostEqual(expectedDataQuality[k], response['result'][k])

    def _getEvaluatedObjectsQualitySummary(self, expectedDataQuality):
        response = self.client.await_completion(self.client.get_objects_quality_evaluated_summary())
        self.assertEqual('OK', response['status'])
        for k, v in expectedDataQuality.items():
            self.assertAlmostEqual(expectedDataQuality[k], response['result'][k])

    def _getEstimatedWorkerCost(self, costAlgorithm, expectedWorkerCost):
        response = self.client.await_completion(self.client.get_estimated_workers_cost(costAlgorithm))
        self.assertEqual('OK', response['status'])
        for workerCost in response['result']:
            self.assertAlmostEqual(expectedWorkerCost[workerCost['workerName']], workerCost['value'])

    def _getEstimatedWorkerQuality(self, costAlgorithm, expectedWorkerQuality):
        response = self.client.await_completion(self.client.get_estimated_workers_quality(costAlgorithm))
        self.assertEqual('OK', response['status'])
        for workerQuality in response['result']:
            self.assertAlmostEqual(expectedWorkerQuality[workerQuality['workerName']], workerQuality['value'])

    def _getEvaluatedWorkerQuality(self, costAlgorithm, expectedResults):
        response = self.client.await_completion(self.client.get_evaluated_workers_quality(costAlgorithm))
        self.assertEqual('OK', response['status'])
        for item in response['result']:
            self.assertEqual(expectedResults[item['workerName']], item['value'])

    def _getWorkersQualityEstimatedSummary(self, expectedWorkerQuality):
        response = self.client.await_completion(self.client.get_workers_quality_estimated_summary())
        self.assertEqual('OK', response['status'])
        for k, v in expectedWorkerQuality.items():
            self.assertEqual(expectedWorkerQuality[k], response['result'][k])

    def _getWorkersQualityEvaluatedSummary(self, expectedWorkerQuality):
        response = self.client.await_completion(self.client.get_workers_quality_evaluated_summary())
        self.assertEqual('OK', response['status'])
        for k, v in expectedWorkerQuality.items():
            self.assertEqual(expectedWorkerQuality[k], response['result'][k])

    def _getCategoryProbability(self, expectedProbabilities):
        for object in set((x[1] for x in ASSIGNED_LABELS)):
            response = self.client.await_completion(self.client.get_probability_distribution(object))
            self.assertEqual('OK', response['status'])
            self.assertEqual(expectedProbabilities[object], response['result'])

@ddt
class TestPredictionMV(TestPrediction):

    algorithm = "BMV"

    def test_GetCategoryProbability(self):
        expectedProbabilities = {'url1': [{u'categoryName': u'porn', u'value': 0.4}, {u'categoryName': u'notporn', u'value': 0.6000000000000001}],
                                 'url2': [{u'categoryName': u'porn', u'value': 0.8}, {u'categoryName': u'notporn', u'value': 0.2}],
                                 'url3': [{u'categoryName': u'porn', u'value': 0.4}, {u'categoryName': u'notporn', u'value': 0.6000000000000001}],
                                 'url4': [{u'categoryName': u'porn', u'value': 0.8}, {u'categoryName': u'notporn', u'value': 0.2}],
                                 'url5': [{u'categoryName': u'porn', u'value': 0.6000000000000001}, {u'categoryName': u'notporn', u'value': 0.4}]} 
        self._getCategoryProbability(expectedProbabilities)

    @data('ExpectedCost', 'MinCost')
    def test_GetEstimatedObjectsCost(self, costAlgorithm):
        expectedCosts = {'ExpectedCost':  {'url1':0.4800000000000001, 'url2':0.32000000000000006, 'url3':0.4800000000000001, 'url4':0.32000000000000006, 'url5':0.4800000000000001 },
                         'MinCost': {'url1':0.4, 'url2':0.2, 'url3':0.4, 'url4':0.2, 'url5':0.4}}
        self._getEstimatedObjectsCost(costAlgorithm, expectedCosts[costAlgorithm])

    @data('ExpectedCost', 'MinCost')
    def test_GetEstimatedObjectsQuality(self, costAlgorithm):
        expectedDataQuality = {'ExpectedCost': {'url1':0.039999999999999813, 'url2':0.3599999999999999, 'url3':0.039999999999999813, 'url4':0.3599999999999999, 'url5':0.039999999999999813},
                               'MinCost': {'url1':0.19999999999999996, 'url2':0.6, 'url3':0.19999999999999996, 'url4':0.6, 'url5':0.19999999999999996}}
        self._getEstimatedObjectsQuality(costAlgorithm, expectedDataQuality[costAlgorithm])

    @data('MaxLikelihood', 'MinCost')
    def test_GetObjectsPrediction(self, costAlgorithm):
        expectedCategories = {'MaxLikelihood': {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'porn'},
                              'MinCost':{'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'porn'}}
        self._getObjectsPrediction(costAlgorithm, expectedCategories[costAlgorithm])

@ddt
class TestPredictionIDS(TestPrediction):

    algorithm = "IDS"

    @data('MaxLikelihood', 'MinCost')
    def test_GetObjectsPrediction(self, costAlgorithm):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'notporn'}
        self._getObjectsPrediction(costAlgorithm, expectedCategories)

    def test_GetEstimatedObjectsCostSummary(self):
        expectedObjectsCosts = {'MaxLikelihood':0.13045135272274802, 'ExpectedCost':0.18053434133112525, 'MinCost':0.13045135272274802, 'Spammer':0.5 }
        self._getEstimatedObjectsCostSummary(expectedObjectsCosts)

    def test_GetEvaluatedObjectsCostSummary(self):
        expectedObjectsCosts = {'MaxLikelihood':0.0, 'MinCost':0.0}
        self._getEvaluatedObjectsCostSummary(expectedObjectsCosts)

    def test_GetEstimatedObjectsQualitySummary(self):
        expectedObjectsQuality = {'MaxLikelihood':0.739097294554504, 'ExpectedCost':0.6389313173377495, 'MinCost':0.739097294554504 }
        self._getEstimatedObjectsQualitySummary(expectedObjectsQuality)

    def test_GetEvaluatedObjectsQualitySummary(self):
        expectedObjectsQuality = {'MaxLikelihood':1.0, 'MinCost':1.0 }
        self._getEvaluatedObjectsQualitySummary(expectedObjectsQuality)

    @data('ExpectedCost', 'MaxLikelihood', 'MinCost')
    def test_GetEstimatedWorkersCost(self, costAlgorithm):
        expectedWorkersCost = {'ExpectedCost':  {'worker1':0.4623062156843241, 'worker2':0.4293514558166182, 'worker3':0.34760515356531635, 'worker4':0.24473477143048578, 'worker5':0.42542373936210476},
                               'MaxLikelihood': {'worker1':0.46565701665845577, 'worker2':0.3151766751397192, 'worker3':0.2294316591298916, 'worker4':0.14920267770148643, 'worker5':0.3061659701843492},
                               'MinCost':       {'worker1':0.46565701665845577, 'worker2':0.3151766751397192, 'worker3':0.2294316591298916, 'worker4':0.14920267770148643, 'worker5':0.3061659701843492}}
        self._getEstimatedWorkerCost(costAlgorithm, expectedWorkersCost[costAlgorithm])

    def test_GetEstimatedWorkersQualitySummary(self):
        expectedWorkerQuality = {'MaxLikelihood':0.4137464004744391, 'ExpectedCost':0.23623146565646036, 'MinCost':0.4137464004744391}
        self._getWorkersQualityEstimatedSummary(expectedWorkerQuality)

    def test_GetEvaluatedWorkersQualitySummary(self):
        expectedWorkerQuality = {'MaxLikelihood':0.7333333333333334, 'MinCost':0.7333333333333334}
        self._getWorkersQualityEvaluatedSummary(expectedWorkerQuality)

@ddt
class TestPredictionBDS(TestPrediction):

    algorithm = "BDS"

    def test_GetCategoryProbability(self):
        expectedProbabilities = {'url1': [{u'categoryName': u'porn', u'value': 0.0}, {u'categoryName': u'notporn', u'value': 1.0}],
                                 'url2': [{u'categoryName': u'porn', u'value': 1.0}, {u'categoryName': u'notporn', u'value': 0.0}],
                                 'url3': [{u'categoryName': u'porn', u'value': 0.0}, {u'categoryName': u'notporn', u'value': 1.0}],
                                 'url4': [{u'categoryName': u'porn', u'value': 1.0}, {u'categoryName': u'notporn', u'value': 0.0}],
                                 'url5': [{u'categoryName': u'porn', u'value': 0.0}, {u'categoryName': u'notporn', u'value': 1.0}]}
        self._getCategoryProbability(expectedProbabilities)

    @data('MaxLikelihood', 'MinCost')
    def test_GetObjectsPrediction(self, costAlgorithm):
        expectedCategories = {'url1':'notporn', 'url2':'porn', 'url3':'notporn', 'url4':'porn', 'url5':'notporn'}
        self._getObjectsPrediction(costAlgorithm, expectedCategories)

    @data('ExpectedCost', 'MinCost')
    def test_GetEstimatedObjectsCost(self, costAlgorithm):
        expectedCosts = {'url1':0.0, 'url2':0.0, 'url3':0.0, 'url4':0.0, 'url5':0.0 }
        self._getEstimatedObjectsCost(costAlgorithm, expectedCosts)

    @data('MaxLikelihood', 'MinCost')
    def test_GetEvaluatedObjectsCosts(self, costAlgorithm):
        expectedCosts = {'url1':0.0, 'url2':0.0, 'url3':0.0, 'url4':0.0, 'url5':0.0 }
        self._getEvaluatedObjectsCost(costAlgorithm, expectedCosts)

    @data('ExpectedCost', 'MinCost')
    def test_GetEstimatedObjectsQuality(self, costAlgorithm):
        expectedDataQuality = {'url1':1.0, 'url2':1.0, 'url3':1.0, 'url4':1.0, 'url5':1.0}
        self._getEstimatedObjectsQuality(costAlgorithm, expectedDataQuality)

    @data('MaxLikelihood', 'MinCost')
    def test_GetEvaluatedObjectsQuality(self, costAlgorithm):
        expectedDataQuality = {'url1':1.0, 'url2':1.0, 'url3':1.0, 'url4':1.0, 'url5':1.0 }
        self._getEvaluatedObjectsQuality(costAlgorithm, expectedDataQuality)

    @data('ExpectedCost', 'MaxLikelihood', 'MinCost')
    def test_GetEstimatedWorkersCost(self, costAlgorithm):
        expectedWorkersCost = {'ExpectedCost':  {'worker1':0.5, 'worker2': 0.2777777777777778, 'worker3':0.0, 'worker4':0.0, 'worker5':0.0},
                               'MaxLikelihood': {'worker1':0.5, 'worker2':0.16666666666666666, 'worker3':0.0, 'worker4':0.0, 'worker5':0.0},
                               'MinCost':       {'worker1':0.5, 'worker2':0.16666666666666666, 'worker3':0.0, 'worker4':0.0, 'worker5':0.0}}
        self._getEstimatedWorkerCost(costAlgorithm, expectedWorkersCost[costAlgorithm])

    @data('ExpectedCost', 'MaxLikelihood', 'MinCost')
    def test_GetEstimatedWorkersQuality(self, costAlgorithm):
        expectedWorkerQuality = {'ExpectedCost':  {'worker1':0.0, 'worker2':0.4444444444444444, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0},
                                 'MaxLikelihood': {'worker1':0.0, 'worker2':0.6666666666666667, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0},
                                 'MinCost':       {'worker1':0.0, 'worker2':0.6666666666666667, 'worker3':1.0, 'worker4':1.0, 'worker5':1.0}}

        self._getEstimatedWorkerQuality(costAlgorithm, expectedWorkerQuality[costAlgorithm])

    @data('MaxLikelihood', 'MaxLikelihood', 'MinCost')
    def test_GetEvaluatedWorkersQuality(self, costAlgorithm):
        expectedResults = {'ExpectedCost': {'worker2': 0.4444444444444444, 'worker1': 0.0, 'worker5': 1.0, 'worker4': 1.0, 'worker3': 1.0},
                           'MaxLikelihood': {'worker2': 0.6666666666666667, 'worker1': 0, 'worker5': 1.0, 'worker4': 1.0, 'worker3': 1.0},
                           'MinCost':{'worker2': 0.6666666666666667, 'worker1': 0, 'worker5': 1.0, 'worker4': 1.0, 'worker3': 1.0}}
        self._getEvaluatedWorkerQuality(costAlgorithm, expectedResults[costAlgorithm])

    def test_GetEstimatedObjectsCostSummary(self):
        expectedObjectsCosts = {'MaxLikelihood':0.0, 'ExpectedCost':0.0, 'MinCost':0.0, 'Spammer':0.5 }
        self._getEstimatedObjectsCostSummary(expectedObjectsCosts)

    def test_GetEvaluatedObjectsCostSummary(self):
        expectedObjectsCosts = {'MaxLikelihood':0.0, 'MinCost':0.0}
        self._getEvaluatedObjectsCostSummary(expectedObjectsCosts)

    def test_GetEstimatedObjectsQualitySummary(self):
        expectedObjectsQuality = {'MaxLikelihood':1.0, 'ExpectedCost':1.0, 'MinCost':1.0 }
        self._getEstimatedObjectsQualitySummary(expectedObjectsQuality)

    def test_GetEvaluatedObjectsQualitySummary(self):
        expectedObjectsQuality = {'MaxLikelihood':1.0, 'MinCost':1.0 }
        self._getEvaluatedObjectsQualitySummary(expectedObjectsQuality)

    def test_GetEstimatedWorkersQualitySummary(self):
        expectedWorkerQuality = {'MaxLikelihood':0.7333333333333334, 'ExpectedCost':0.6888888888888889, 'MinCost':0.7333333333333334}
        self._getWorkersQualityEstimatedSummary(expectedWorkerQuality)

    def test_GetEvaluatedWorkersQualitySummary(self):
        expectedWorkerQuality = {'MaxLikelihood':0.7333333333333334, 'MinCost':0.7333333333333334}
        self._getWorkersQualityEvaluatedSummary(expectedWorkerQuality)

    def test_GetPredictionZip(self):
        response = self.client.await_completion(self.client.get_prediction_zip())
        self.assertEqual('OK', response['status'])
        self.assertTrue('/media/downloads/' in response['result'])
