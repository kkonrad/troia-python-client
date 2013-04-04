# -*- coding: utf-8 -*-
import unittest
import random
from ddt import ddt, data
from client.gal import TroiaClient
from testSettings import *

class TestUtils:

    def generateAssigns(self, assignsGenModel, num_objects, categories=CATEGORIES):
        assigns = []
        if assignsGenModel == 'differentObjectCounts':
            for i in xrange(num_objects):
                for j in xrange(i + 1):
                    assigns.append((
                        'worker{}'.format(j),
                        'object{}'.format(i),
                         categories[random.randint(0, len(categories) - 1)]
                    ))
        if assignsGenModel == 'sameObjectCounts':
            for i in xrange(num_objects):
                for j in xrange(num_objects):
                    assigns.append((
                        'worker{}'.format(j),
                        'object{}'.format(i),
                         categories[random.randint(0, len(categories) - 1)]
                    ))
        if assignsGenModel == 'sameObjectCosts':
            for i in xrange(num_objects):
                for j in xrange(num_objects):
                    assigns.append((
                        'worker{}'.format(j),
                        'object{}'.format(i),
                         categories[1]
                    ))
        if assignsGenModel == 'differentObjectCosts':
            for i in xrange(num_objects):
                for j in xrange( i + 1):
                    assigns.append((
                        'worker{}'.format(j),
                        'object{}'.format(i),
                         categories[i]
                    ))
        return assigns

@ddt
class TestCachedScheduler(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        self.scheduler = 'cachedscheduler'
        self.utils = TestUtils()

    def tearDown(self):
        self.client.delete()

    def _createTestPrereq(self, algorithm, scheduler, calculator, assigns, categories = CATEGORIES, categoryPriors = CATEGORY_PRIORS):
        response = self.client.create(
            categories,
            categoryPriors=categoryPriors,
            algorithm=algorithm,
            scheduler=scheduler,
            calculator=calculator
        )

        self.assertEqual('OK', response['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns))['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_DifferentLabelCounts_AddNewAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'differentObjectCounts'
        noObjects = 3
        expectedObjectsQueue = ['object0', 'object1', 'object2']
        newAssign = [('worker0', 'object1', CATEGORIES[1])]
        expectedObject = 'object1'
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_DifferentLabelCounts_AddEmptyAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'differentObjectCounts'
        noObjects = 3
        expectedObjectsQueue = ['object0', 'object1', 'object2']
        newAssign = []
        expectedObject = None
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_SameLabelCounts_AddNewAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'sameObjectCounts'
        noObjects = 2
        expectedObjectsQueue = ['object0', 'object1']
        newAssign = [('worker3', 'object0', CATEGORIES[1])]
        expectedObject = 'object0'
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_SameLabelCounts_AddEmptyAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'sameObjectCounts'
        noObjects = 2
        expectedObjectsQueue = ['object0', 'object1']
        newAssign = []
        expectedObject = None
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    def _test_method(self, algorithm, scheduler, calculator, assignsGenModel, noObjects, categories = CATEGORIES, categoryPriors=CATEGORY_PRIORS):
        assigns = self.utils.generateAssigns(assignsGenModel, noObjects, categories)
        self._createTestPrereq(algorithm, scheduler, calculator, assigns, categories, categoryPriors)

    def _check_results(self, expectedObjectsQueue, newAssign, expectedObject):
        for i in xrange(len(expectedObjectsQueue)):
            response = self.client.await_completion(self.client.get_next_object())
            self.assertEqual(expectedObjectsQueue[i], response['result']['name'])

        # This one should be null. That means the 'result' key is not present in the response.
        self.assertIsNone(self.client.await_completion(self.client.get_next_object()).get('result', None))

        # Add assign to the object. The object should be returned by subsequent 'nextObject' call.
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssign))['status'])
        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('OK',response['status'])

        if response.get('result') == None:
            self.assertIsNone(expectedObject)
        else:
            self.assertEqual(expectedObject, response['result']['name'])

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CostBasedCalculator_SameCosts(self, algorithm):
        calculator = 'costbased'
        assignsGenerationModel = 'sameObjectCosts'
        noObjects = 3
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))
        self.assertEquals("OK", response['status'])
        resDict = {}
        for result in response['result']:
            resDict[result['objectName']] = result['value']

        #sort the objects descending, based on cost 
        expectedObjectsQueue = [] 
        for key, value in sorted(resDict.iteritems(), reverse=True):
            expectedObjectsQueue.append(key)
        newAssign = []
        expectedObject = None
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CostBasedCalculator_DifferentCosts(self, algorithm):
        calculator = 'costbased'
        assignsGenerationModel = 'differentObjectCosts'
        noObjects = 3
        categories = ["cat1", "cat2", "cat3"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.1}, {"categoryName": "cat2", "value": 0.3}, {"categoryName": "cat3", "value": 0.6}]
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects, categories, categoryPriors)
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))
        self.assertEquals("OK", response['status'])
        resDict = {}
        for result in response['result']:
            resDict[result['objectName']] = result['value']
        #sort the objects descending, based on cost 
        expectedObjectsQueue = [] 
        for key, value in sorted(resDict.iteritems(), reverse=True):
            #print "%s: %s" % (key, value)
            expectedObjectsQueue.append(key)
        newAssign = []
        expectedObject = None
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

@ddt
class TestNormalScheduler(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        self.scheduler = 'normalscheduler'
        self.utils = TestUtils()

    def tearDown(self):
        self.client.delete()

    def _createTestPrereq(self, algorithm, scheduler, calculator, assigns, categories = CATEGORIES, categoryPriors = CATEGORY_PRIORS):
        response = self.client.create(
            categories,
            categoryPriors=categoryPriors,
            algorithm=algorithm,
            scheduler=scheduler,
            calculator=calculator
        )

        self.assertEqual('OK', response['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns))['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])

    def _test_method(self, algorithm, scheduler, calculator, assignsGenModel, noObjects, categories = CATEGORIES, categoryPriors=CATEGORY_PRIORS):
        assigns = self.utils.generateAssigns(assignsGenModel, noObjects, categories)
        self._createTestPrereq(algorithm, scheduler, calculator, assigns, categories, categoryPriors)

    def _check_results(self, noObjects, expectedObjectList, newAssign):
        print "***_check_results"
        print expectedObjectList
        for i in xrange(noObjects + 1):
            response = self.client.await_completion(self.client.get_next_object())
            print response
            self.assertTrue(response['result']['name'] in expectedObjectList)

        # Add assign to the object. The object should be returned by subsequent 'nextObject' call.
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssign))['status'])
        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('OK',response['status'])
        self.assertTrue(response['result']['name'] in expectedObjectList)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_NormalScheduler_CountAssignsCalculator_DifferentLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'differentObjectCounts'
        noObjects = 3
        expectedObjectList = ['object0']
        newAssign = [('worker3', 'object0', CATEGORIES[0])]
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(noObjects, expectedObjectList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_NormalScheduler_CountAssignsCalculator_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'sameObjectCounts'
        noObjects = 3
        expectedObjectList = ['object0', 'object1', 'object2'];
        newAssign = [('worker3', 'object0', CATEGORIES[1])]
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(noObjects, expectedObjectList, newAssign)

    @data('BDS', 'IDS','BMV', 'IMV')
    def test_NormalScheduler_CostBasedCalculator_SameCosts(self, algorithm):
        calculator = 'costbased'
        assignsGenerationModel = 'sameObjectCosts'
        noObjects = 3
        categories = ["category1", "category2", "category3"]
        categoryPriors = [{"categoryName": "category1", "value": 0.1}, {"categoryName": "category2", "value": 0.3}, {"categoryName": "category2", "value": 0.6}]
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects, categories, categoryPriors)
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))

        self.assertEquals("OK", response['status'])
        resDict = {}
        for result in response['result']:
            resDict[result['objectName']] = result['value']

        #sort the objects descending, based on cost 
        sortedList = [] 
        for key, value in sorted(resDict.iteritems(), reverse=True):
            print key, value
            sortedList.append(key)

        newAssign = [('worker3', 'object0', categories[1])]
        self._check_results(noObjects, [sortedList[0]], newAssign)


    @data('BDS', 'IDS','BMV', 'IMV')
    def test_NormalScheduler_CostBasedCalculator_DifferentCosts(self, algorithm):
        calculator = 'costbased'
        assignsGenerationModel = 'differentObjectCosts'
        noObjects = 3
        categories = ["category1", "category2", "category3"]
        categoryPriors = [{"categoryName": "category1", "value": 0.1}, {"categoryName": "category2", "value": 0.3}, {"categoryName": "category2", "value": 0.6}]
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects, categories, categoryPriors)
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))
        self.assertEquals("OK", response['status'])

        resDict = {}
        for result in response['result']:
            resDict[result['objectName']] = result['value']
        #sort the objects descending, based on cost 
        sortedList = [] 
        for key, value in sorted(resDict.iteritems(), reverse=True):
            print key, value
            sortedList.append(key)

        newAssign = [('worker3', 'object0', categories[1])]
        self._check_results(noObjects,  [sortedList[0]], newAssign)


   