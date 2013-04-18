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

    def _check_results(self, expectedObjectList, newAssign, expectedObject):
        for i in xrange(len(expectedObjectList)):
            response = self.client.await_completion(self.client.get_next_object())
            objectName = response['result']['name']
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
    def test_CachedScheduler_CountAssignsCalculator_DifferentLabelCounts_AddNewAssigns(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'), 
                   ('worker2', 'object1', 'porn'),
                   ('worker3', 'object1', 'notporn'),
                   ('worker4', 'object1', 'notporn'),
                   ('worker1', 'object2', 'porn'),
                   ('worker2', 'object2', 'porn'),
                   ('worker3', 'object2', 'porn'),
                   ('worker3', 'object3', 'notporn'),
                   ]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('object3', response['result']['name'])

        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('object2', response['result']['name'])

        newAssigns = [('worker4', 'object3', 'porn')]
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssigns))['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])
        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('object3', response['result']['name'])

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

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CostBasedCalculator_SameCosts(self, algorithm):
        calculator = 'costbased'
        categories = ["cat1", "cat2"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.5}, {"categoryName": "cat2", "value": 0.5}]
        assigns = [('worker1', 'object1', 'cat1'), 
                   ('worker2', 'object1', 'cat1'),
                   ('worker3', 'object2', 'cat1'),
                   ('worker4', 'object2', 'cat1')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)
        objectCostList = self.getObjectCostsList()
        newAssign = [('worker3', 'object0', categories[0])]
        expectedObject = 'object0'
        self._check_results(objectCostList, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CostBasedCalculator_DifferentObjectCosts_AssignsInOneCategory(self, algorithm):
        calculator = 'costbased'
        assigns = [('worker0', 'object0', 'notporn'), 
                   ('worker1', 'object0', 'notporn'), 
                   ('worker2', 'object0', 'notporn'),
                   ('worker0', 'object1', 'notporn'), 
                   ('worker1', 'object1', 'notporn'),
                   ('worker2', 'object1', 'notporn'),
                   ('worker0', 'object2', 'notporn'), 
                   ('worker1', 'object2', 'notporn'), 
                   ('worker2', 'object2', 'notporn')]
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
        for i in xrange(len(expectedObjectList) + 1):
            response = self.client.await_completion(self.client.get_next_object())
            self.assertTrue(response['result']['name'] in expectedObjectList)

        # Add assign to the object. The object should be returned by subsequent 'nextObject' call.
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssign))['status'])
        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('OK',response['status'])
        self.assertEquals(newAssign[0][1], response['result']['name'])

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
    def test_NormalScheduler_CountAssignsCalculator_DifferentLabelCounts_AddNewAssigns(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'), 
                   ('worker2', 'object1', 'porn'),
                   ('worker1', 'object2', 'porn'),
                   ('worker2', 'object2', 'notporn'),
                   ('worker3', 'object2', 'porn'),
                   ]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('object1', response['result']['name'])

        newAssigns = [('worker1', 'object3', 'porn')]
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssigns))['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])
        response = self.client.await_completion(self.client.get_next_object())
        self.assertEqual('object3', response['result']['name'])

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_NormalScheduler_CountAssignsCalculator_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        categories = ["cat1", "cat2"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.5}, {"categoryName": "cat2", "value": 0.5}]
        assigns = [('worker1', 'object1', 'cat1'), 
                   ('worker1', 'object2', 'cat1'),
                   ('worker2', 'object1', 'cat2'),
                   ('worker2', 'object2', 'cat2')]
        objectsList = self.sortedObjectsByLabels(assigns, False)
        expectedObjectsList = []
        for o in objectsList:
            expectedObjectsList.append(o[0])

        newAssign = [('worker3', 'object3', 'cat1')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)
        self._check_results(expectedObjectsList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_NormalScheduler_CostBasedCalculator_SameCosts(self, algorithm):
        calculator = 'costbased'
        categories = ["cat1", "cat2"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.5}, {"categoryName": "cat2", "value": 0.5}]
        assigns = [('worker1', 'object1', 'cat1'), 
                   ('worker2', 'object1', 'cat1'),
                   ('worker3', 'object2', 'cat1'),
                   ('worker4', 'object2', 'cat1')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)
        sortedList = self.getObjectCostsList()

        expectedObjectList = []
        minValue = sortedList[0][1]
        for o in sortedList:
            if o[1] == minValue:
                expectedObjectList.append(o[0])

        newAssign = [('worker5', 'object3', 'cat1')]
        self._check_results(expectedObjectList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_NormalScheduler_CostBasedCalculator_DifferentCosts(self, algorithm):
        calculator = 'costbased'
        categories = ["cat1", "cat2", "cat3"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.1}, {"categoryName": "cat2", "value": 0.3},  {"categoryName": "cat3", "value": 0.6}]
        assigns = [('worker1', 'object1', 'cat1'), 
                   ('worker2', 'object1', 'cat2'),
                   ('worker2', 'object2', 'cat1'),
                   ('worker3', 'object1', 'cat1'),
                   ('worker3', 'object2', 'cat2')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)
        sortedList = self.getObjectCostsList()

        expectedObjectList = []
        minValue = sortedList[0][1]
        for o in sortedList:
            if o[1] == minValue:
                expectedObjectList.append(o[0])

        newAssign = [('worker4', 'object0', 'cat3')]
        self._check_results(expectedObjectList, newAssign)