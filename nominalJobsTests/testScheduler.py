# -*- coding: utf-8 -*-
import unittest
import random
from ddt import ddt, data
from client.gal import TroiaClient
from operator import itemgetter
from testSettings import *
import pprint

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
        self.scheduler = 'CachedScheduler'
        self.utils = TestUtils()

    def tearDown(self):
        self.client.delete()

    def _createTestPrereq(self, algorithm, scheduler, calculator, assigns, categories = CATEGORIES, categoryPriors = CATEGORY_PRIORS, costMatrix = COST_MATRIX):
        response = self.client.create(
            categories,
            categoryPriors=categoryPriors,
            algorithm=algorithm,
            scheduler=scheduler,
            prioritycalculator=calculator,
            costMatrix=costMatrix
            )

        self.assertEqual('OK', response['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns))['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])

    def getObjectCountsList(self, assigns, reverse=False, excludedObjectsList=None):
        #create the dictionary containing the objects and the associated no of assigns
        labelsDict = {}
        for l in assigns:
                if l[1] in labelsDict.keys():
                    labelsDict[l[1]] += 1
                else:
                    labelsDict[l[1]] = 1

        #sort the objects ascending, based on the no of labels 
        sortedList = sorted(labelsDict.items(), key=itemgetter(1), reverse=reverse)
        if (excludedObjectsList):
            for value in sortedList:
                if value[0] in excludedObjectsList:
                    sortedList.remove(value)
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

    def getAssignedLabels(self):
        response = self.client.await_completion(self.client.get_assigned_labels())
        self.assertEqual('OK', response['status'])
        assignedLabels = [(l['worker'], l['object'], l['label']) for l in response['result']]
        return assignedLabels

    def _runScheduler(self, workerId=None):
        if (workerId):
            return self.client.get_next_worker_object(workerId)
        else:
            return self.client.get_next_object()

    def _runTestMethod(self, calculator, expectedObjectList, newAssign, workerId=None, excludedObjectsList=None):
        for (_, objectCost) in expectedObjectList:
            response = self.client.await_completion(self._runScheduler(workerId))
            objectName = response['result']['name']

            #get the objects with equal costs
            equalCostObjects = [item[0] for item in expectedObjectList
                    if item[1] == objectCost]
            self.assertTrue(objectName in equalCostObjects)

        # This one should be null. That means the 'result' key is not present in the response.
        response = self.client.await_completion(self._runScheduler(workerId))
        if response['status'] != 'OK':
            pprint.pprint(response)
        self.assertIsNone(response.get('result', None))

        # Add assign to the object. The object should be returned by subsequent 'nextObject' call.
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssign))['status'])
        if calculator == 'countassigns':
            newObjectsList = self.getObjectCountsList(newAssign, False, excludedObjectsList)
        else:
            self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])
            newObjectsList = self.getObjectCostsList()

        #get the objects having the maximum priority
        maxPriorityObjects = [item[0] for item in newObjectsList
                    if item[1] == newObjectsList[0][1]]

        response = self.client.await_completion(self._runScheduler(workerId))

        self.assertEqual('OK',response['status'])

        if response.get('result') == None:
            self.assertTrue(len(newAssign) == 0)
        else:
            self.assertTrue(response['result']['name'] in maxPriorityObjects)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextObject_DifferentLabelCounts_AddNewAssigns(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'), 
                   ('worker2', 'object1', 'notporn'),
                   ('worker1', 'object2', 'porn'),
                   ('worker2', 'object2', 'notporn'),
                   ('worker3', 'object2', 'porn')]

        expectedObjectsList = self.getObjectCountsList(assigns, False)

        newAssigns = [('worker1', 'object3', 'porn')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssigns)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextObject_DifferentLabelCounts_AddEmptyAssign(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'),
                   ('worker1', 'object2', 'porn'),
                   ('worker2', 'object2', 'porn')]

        expectedObjectsList = self.getObjectCountsList(assigns, False)
        newAssign = []
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextObject_SameLabelCounts_AddNewAssign(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'), 
                   ('worker2', 'object1', 'porn'),
                   ('worker1', 'object2', 'porn'),
                   ('worker2', 'object2', 'porn')]

        expectedObjectsList = self.getObjectCountsList(assigns, False)
        newAssign = [('worker3', 'object0', 'notporn')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextObject_SameLabelCounts_AddEmptyAssign(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'), 
                   ('worker2', 'object1', 'porn'),
                   ('worker1', 'object2', 'porn'),
                   ('worker2', 'object2', 'porn')]
        expectedObjectsList = self.getObjectCountsList(assigns, False)
        newAssign = []
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CostBasedCalculator_GetNextObject_SameObjectCosts(self, algorithm):
        calculator = 'costbased'
        categories = ["cat1", "cat2"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.5}, {"categoryName": "cat2", "value": 0.5}]
        costMatrix =  [{"from": "cat1", "to": "cat2", "value": 1.0}, {"from": "cat1", "to": "cat1", "value": 0.0}, 
                       {"from": "cat2", "to": "cat1", "value": 1.0}, {"from": "cat2", "to": "cat2", "value": 0.0}]
        assigns = [('worker1', 'object1', 'cat1'), 
                   ('worker2', 'object1', 'cat1'),
                   ('worker3', 'object2', 'cat1'),
                   ('worker4', 'object2', 'cat1')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors, costMatrix)
        objectCostList = self.getObjectCostsList()
        newAssign = [('worker3', 'object0', 'cat1')]
        self._runTestMethod(calculator, objectCostList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CostBasedCalculator_GetNextObject_DifferentObjectCosts(self, algorithm):
        calculator = 'costbased'
        categories = ["porn", "notporn"] 
        categoryPriors = [{"categoryName": "porn", "value": 0.1}, {"categoryName": "notporn", "value": 0.9}]
        costMatrix =  [{"from": "porn", "to": "notporn", "value": 1.0}, {"from": "porn", "to": "porn", "value": 0.0}, 
                       {"from": "notporn", "to": "porn", "value": 1.0}, {"from": "notporn", "to": "notporn", "value": 0.0}]
        assigns = [('worker0', 'object0', 'notporn'),
                   ('worker1', 'object1', 'porn'),
                   ('worker2', 'object1', 'porn')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors, costMatrix)
        objectCostList = self.getObjectCostsList()
        newAssign = [('worker3', 'object2', 'porn')]
        self._runTestMethod(calculator, objectCostList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CostBasedCalculator_GetNextObject_DifferentObjectCosts_AddEmptyLabel(self, algorithm):
        calculator = 'costbased'
        categories = ["porn", "notporn"] 
        categoryPriors = [{"categoryName": "porn", "value": 0.1}, {"categoryName": "notporn", "value": 0.9}]
        costMatrix =  [{"from": "porn", "to": "notporn", "value": 1.0}, {"from": "porn", "to": "porn", "value": 0.0}, 
                       {"from": "notporn", "to": "porn", "value": 1.0}, {"from": "notporn", "to": "notporn", "value": 0.0}]
        assigns = [('worker0', 'object0', 'notporn'),
                   ('worker1', 'object1', 'porn'),
                   ('worker2', 'object1', 'porn')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors, costMatrix)
        objectCostList = self.getObjectCostsList()

        newAssign = []
        self._runTestMethod(calculator, objectCostList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextWorkerObject_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'),
                   ('worker2', 'object2', 'notporn'),
                   ('worker2', 'object3', 'notporn'),
                   ('worker3', 'object2', 'notporn'),
                   ('worker3', 'object3', 'notporn')
                   ]

        expectedObjectsList = [('object2', 2), ('object3', 2)]
        newAssign = [('worker4', 'object2', 'notporn')]
        excludedObjectsList = ['object1']

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssign, 'worker1', excludedObjectsList)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextWorkerObject_DifferentLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'),
                   ('worker2', 'object1', 'porn'),
                   ('worker2', 'object2', 'notporn'),
                   ('worker3', 'object2', 'notporn'),
                   ('worker3', 'object3', 'porn')]

        expectedObjectsList = [('object3', 1), ('object2', 2)]
        newAssign = [('worker4', 'object2', CATEGORIES[1])]
        excludedObjectsList = ['object1']

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssign, 'worker1', excludedObjectsList)

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
            prioritycalculator=calculator
        )

        self.assertEqual('OK', response['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns))['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])

    def getObjectCountsList(self, assigns, reverse=False, excludedObjectsList=False):
        #create the dictionary containing the objects and the associated no of assigns
        labelsDict = {}
        for l in assigns:
            if l[1] in labelsDict.keys():
                labelsDict[l[1]] += 1
            else:
                labelsDict[l[1]] = 1

        #sort the objects ascending, based on the no of labels 
        sortedList = sorted(labelsDict.items(), key=itemgetter(1), reverse=reverse)

        if (excludedObjectsList):
            for value in sortedList:
                if value[0] in excludedObjectsList:
                    sortedList.remove(value)
        return sortedList

    def getObjectCostsList(self):
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))
        if response['status'] != 'Ok':
            pprint.pprint(response)
        self.assertEquals("OK", response['status'])
        objectCosts = {}
        for result in response['result']:
            objectCosts[result['objectName']] = result['value']

        #sort the objects descending, based on cost 
        objectCostList = sorted(objectCosts.items(), key=itemgetter(1), reverse=True)
        return objectCostList

    def getAssignedLabels(self):
        response = self.client.await_completion(self.client.get_assigned_labels())
        self.assertEqual('OK', response['status'])
        assignedLabels = [(l['worker'], l['object'], l['label']) for l in response['result']]
        return assignedLabels

    def _runScheduler(self, workerId=None):
        if (workerId):
            return self.client.get_next_worker_object(workerId)
        else:
            return self.client.get_next_object()

    def _runTestMethod(self, calculator, expectedObjectList, newAssign, workerId=None, excludedObjectsList=None):
        for i in xrange(len(expectedObjectList)):
            response = self.client.await_completion(self._runScheduler(workerId))
            self.assertTrue(response['result']['name'] in expectedObjectList)

        # Add assign to the object. The object should be returned by subsequent 'nextObject' call.
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssign))['status'])
        response = self.client.await_completion(self._runScheduler(workerId))
        self.assertEqual('OK',response['status'])

        if calculator == 'countassigns':
            newObjectsList = self.getObjectCountsList(self.getAssignedLabels(), False, excludedObjectsList)
        else:
            newObjectsList = self.getObjectCostsList()

        #get the objects having the maximum priority
        maxPriorityObjects = [item[0] for item in newObjectsList
                    if item[1] == newObjectsList[0][1]]

        response = self.client.await_completion(self._runScheduler(workerId))
        self.assertEqual('OK',response['status'])
        self.assertTrue(response['result']['name'] in maxPriorityObjects)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextObject_DifferentLabelCounts_AddEmptyAssigns(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'),
                   ('worker2', 'object1', 'notporn'),
                   ('worker2', 'object2', 'notporn')]
        sortedList = self.getObjectCountsList(assigns, False)
        minValue = sortedList[0][1]
        expectedObjectsList = [o[0] for o in sortedList if o[1] == minValue]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, [])

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextObject_DifferentLabelCounts_AddNewAssigns(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'),
                   ('worker2', 'object1', 'porn'),
                   ('worker1', 'object2', 'porn'),
                   ('worker2', 'object2', 'notporn'),
                   ('worker3', 'object2', 'porn'),
                   ]

        sortedList = self.getObjectCountsList(assigns, False)
        minValue = sortedList[0][1]
        expectedObjectsList = [o[0] for o in sortedList if o[1] == minValue]

        newAssign = [('worker1', 'object3', 'porn')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextObject_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        categories = ["cat1", "cat2"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.5}, {"categoryName": "cat2", "value": 0.5}]
        assigns = [('worker1', 'object1', 'cat1'), 
                   ('worker1', 'object2', 'cat1'),
                   ('worker2', 'object1', 'cat2'),
                   ('worker2', 'object2', 'cat2')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)

        sortedList = self.getObjectCountsList(assigns, False)
        minValue = sortedList[0][1]
        expectedObjectList = [o[0] for o in sortedList if o[1] == minValue]
        newAssign = [('worker3', 'object3', 'cat1')]
        self._runTestMethod(calculator, expectedObjectList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CostBasedCalculator_GetNextObject_SameCosts(self, algorithm):
        calculator = 'costbased'
        categories = ["cat1", "cat2"] 
        categoryPriors = [{"categoryName": "cat1", "value": 0.5}, {"categoryName": "cat2", "value": 0.5}]
        assigns = [('worker1', 'object1', 'cat1'), 
                   ('worker2', 'object1', 'cat1'),
                   ('worker3', 'object2', 'cat1'),
                   ('worker4', 'object2', 'cat1')]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns, categories, categoryPriors)
        sortedList = self.getObjectCostsList()

        minValue = sortedList[0][1]
        expectedObjectList = [o[0] for o in sortedList if o[1] == minValue]

        newAssign = [('worker5', 'object3', 'cat1')]
        self._runTestMethod(calculator, expectedObjectList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CostBasedCalculator_GetNextObject_DifferentCosts(self, algorithm):
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
        minValue = sortedList[0][1]
        expectedObjectList = [o[0] for o in sortedList if o[1] == minValue]
        newAssign = [('worker4', 'object0', 'cat3')]
        self._runTestMethod(calculator, expectedObjectList, newAssign)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextWorkerObject_DifferentLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'),
                   ('worker2', 'object1', 'porn'),
                   ('worker2', 'object2', 'notporn'),
                   ('worker3', 'object2', 'notporn'),
                   ('worker4', 'object2', 'notporn'),
                   ('worker3', 'object3', 'porn')
                   ]

        expectedObjectsList = ['object3']
        newAssigns = [('worker4', 'object3', CATEGORIES[0])]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssigns, 'worker1')

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CountAssignsCalculator_GetNextWorkerObject_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 'porn'),
                   ('worker2', 'object1', 'porn'),
                   ('worker2', 'object2', 'notporn'),
                   ('worker3', 'object2', 'porn'),
                   ('worker3', 'object3', 'notporn'),
                   ('worker4', 'object3', 'porn')
                   ]

        expectedObjectsList = ['object3', 'object2']
        newAssigns = [('worker4', 'object4', CATEGORIES[0])]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssigns, 'worker1')