# -*- coding: utf-8 -*-
import unittest
import random
from ddt import ddt, data
from client.gal import TroiaClient
from operator import itemgetter
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

    def createSortedObjectsList(self, assigns, reverse=False):
        #create the dictionary containing the objects and the associated no of assigns
        labelsDict = {}
        for l in assigns:
            if l[1] in labelsDict.keys():
                labelsDict[l[1]] += 1
            else:
                labelsDict[l[1]] = 1

        #sort the objects ascending, based on the no of labels 
        sortedList = sorted(labelsDict.items(), key=itemgetter(1), reverse=reverse)
        return sortedList

    def getObjectCostsList(self):
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))
        self.assertEquals("OK", response['status'])
        objectCosts = {}
        for result in response['result']:
            objectCosts[result['objectName']] = result['value']

        #sort the objects descending, based on cost 
        objectCostList = sorted(objectCosts.items(), key=itemgetter(1), reverse=True)
        return objectCostList

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_DifferentLabelCounts_AddNewAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'differentObjectCounts'
        noObjects = 3
        assigns = self.utils.generateAssigns(assignsGenerationModel, noObjects)
        expectedObjectsList = self.createSortedObjectsList(assigns, False)

        newAssign = [('worker0', 'object1', CATEGORIES[1])]
        expectedObject = 'object1'
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._check_results(expectedObjectsList, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_DifferentLabelCounts_AddEmptyAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'differentObjectCounts'
        noObjects = 3
        assigns = self.utils.generateAssigns(assignsGenerationModel, noObjects)
        expectedObjectsList = self.createSortedObjectsList(assigns, False)

        newAssign = []
        expectedObject = None
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._check_results(expectedObjectsList, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_SameLabelCounts_AddNewAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'sameObjectCounts'
        noObjects = 2
        assigns = self.utils.generateAssigns(assignsGenerationModel, noObjects)
        expectedObjectsList = self.createSortedObjectsList(assigns, False)

        newAssign = [('worker3', 'object0', CATEGORIES[1])]
        expectedObject = 'object0'
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._check_results(expectedObjectsList, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_SameLabelCounts_AddEmptyAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'sameObjectCounts'
        noObjects = 2
        assigns = self.utils.generateAssigns(assignsGenerationModel, noObjects)
        expectedObjectsList = self.createSortedObjectsList(assigns, False)
        newAssign = []
        expectedObject = None
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._check_results(expectedObjectsList, newAssign, expectedObject)

    def _check_results(self, expectedObjectList, newAssign, expectedObject):
        for i in xrange(len(expectedObjectList)):
            objectName = self.client.await_completion(self.client.get_next_object())['result']['name']
            objectCost = expectedObjectList[i][1]

            #get the objects with equal costs
            equalCostObjects = []
            for item in expectedObjectList:
                if item[1] == objectCost:
                    equalCostObjects.append(item[0])
            self.assertTrue(objectName in equalCostObjects)

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
        assigns = self.utils.generateAssigns(assignsGenerationModel, noObjects)
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        objectCostList = self.getObjectCostsList()
        newAssign = [('worker3', 'object0', CATEGORIES[0])]
        expectedObject = 'object0'
        self._check_results(objectCostList, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CostBasedCalculator_DifferentCosts(self, algorithm):
        calculator = 'costbased'
        assignsGenerationModel = 'differentObjectCosts'
        noObjects = 3
        categories = ["cat1", "cat2", "cat3"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.1}, {"categoryName": "cat2", "value": 0.3}, {"categoryName": "cat3", "value": 0.6}]

        assigns = self.utils.generateAssigns(assignsGenerationModel, noObjects, categories)
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)
        objectCostList = self.getObjectCostsList()

        newAssign = []
        expectedObject = None
        self._check_results(objectCostList, newAssign, expectedObject)

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

    def sortedObjectsByLabels(self, assigns, reverse=False):
        #create the dictionary containing the objects and the associated no of assigns
        labelsDict = {}
        for l in assigns:
            if l[1] in labelsDict.keys():
                labelsDict[l[1]] += 1
            else:
                labelsDict[l[1]] = 1

        #sort the objects ascending, based on the no of labels 
        sortedList = sorted(labelsDict.items(), key=itemgetter(1), reverse=reverse)
        return sortedList

    def getObjectCostsList(self):
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))
        self.assertEquals("OK", response['status'])
        objectCosts = {}
        for result in response['result']:
            objectCosts[result['objectName']] = result['value']

        #sort the objects descending, based on cost 
        objectCostList = sorted(objectCosts.items(), key=itemgetter(1), reverse=True)
        return objectCostList

    def _check_results(self, expectedObjectList, newAssign):
        for i in xrange(len (expectedObjectList) + 1):
            response = self.client.await_completion(self.client.get_next_object())
            self.assertTrue(response['result']['name'] in expectedObjectList)

        # Add assign to the object. The object should be returned by subsequent 'nextObject' call.
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssign))['status'])
        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('OK',response['status'])
        self.assertTrue(response['result']['name'] in expectedObjectList)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_NormalScheduler_CountAssignsCalculator_DifferentLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assignsGenModel = 'differentObjectCounts'
        noObjects = 3
        assigns = self.utils.generateAssigns(assignsGenModel, noObjects)
        expectedObjectsList = self.sortedObjectsByLabels(assigns, False)

        newAssign = [('worker3', 'object0', CATEGORIES[0])]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._check_results(expectedObjectsList[0][0], newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_NormalScheduler_CountAssignsCalculator_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assignsGenModel = 'sameObjectCounts'
        noObjects = 3
        assigns = self.utils.generateAssigns(assignsGenModel, noObjects)
        objectsList = self.sortedObjectsByLabels(assigns, False)
        expectedObjectsList = []
        for o in objectsList:
            expectedObjectsList.append(o[0])
        newAssign = [('worker3', 'object0', CATEGORIES[1])]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._check_results(expectedObjectsList, newAssign)

    @data('BDS', 'IDS','BMV', 'IMV')
    def test_NormalScheduler_CostBasedCalculator_SameCosts(self, algorithm):
        calculator = 'costbased'
        assignsGenModel = 'sameObjectCosts'
        noObjects = 3
        categories = ["category1", "category2", "category3"]
        categoryPriors = [{"categoryName": "category1", "value": 0.1}, {"categoryName": "category2", "value": 0.3}, {"categoryName": "category2", "value": 0.6}]
        assigns = self.utils.generateAssigns(assignsGenModel, noObjects, categories)
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)
        sortedList = self.getObjectCostsList()

        expectedObjectList = []
        minValue = sortedList[0][1]
        for o in sortedList:
            if o[1] == minValue:
                expectedObjectList.append(o[0])

        newAssign = [('worker3', 'object0', categories[1])]
        self._check_results(expectedObjectList, newAssign)


    @data('BDS', 'IDS','BMV', 'IMV')
    def test_NormalScheduler_CostBasedCalculator_DifferentCosts(self, algorithm):
        calculator = 'costbased'
        assignsGenModel = 'differentObjectCosts'
        noObjects = 3
        categories = ["category1", "category2", "category3"]
        categoryPriors = [{"categoryName": "category1", "value": 0.1}, {"categoryName": "category2", "value": 0.3}, {"categoryName": "category2", "value": 0.6}]
        assigns = self.utils.generateAssigns(assignsGenModel, noObjects, categories)
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)
        sortedList = self.getObjectCostsList()

        expectedObjectList = []
        minValue = sortedList[0][1]
        for o in sortedList:
            if o[1] == minValue:
                expectedObjectList.append(o[0])

        newAssign = [('worker3', 'object0', categories[1])]
        self._check_results(expectedObjectList, newAssign)