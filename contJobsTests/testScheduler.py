'''
Created on May 22, 2013

@author: dana
'''
# -*- coding: utf-8 -*-
import unittest
import random
from ddt import ddt, data
from operator import itemgetter
from testSettings import *
import pprint
from client.galc import TroiaContClient

@ddt
class TestCachedScheduler(unittest.TestCase):

    def setUp(self):
        self.client = TroiaContClient(ADDRESS)
        self.scheduler = 'CachedScheduler'

    def tearDown(self):
        self.client.delete()

    def _createTestPrereq(self, algorithm, scheduler, calculator, assigns=ASSIGNED_LABELS_CONT):
        response = self.client.create(
            algorithm=algorithm,
            scheduler=scheduler,
            prioritycalculator=calculator
            )

        if calculator == 'countassigns':
            self.assertEqual('OK', response['status'])
            self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns))['status'])
            self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])
        else:
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('class com.datascience.scheduler.CostBasedPriorityCalculator supports only NominalProjects, not class com.datascience.galc.ContinuousProject', response['result'])

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
        return None

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

    @data('GALC')
    def test_CountAssignsCalculator_GetNextObject_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 4.399898705211159),
                   ('worker2', 'object1', 2.399898705211159),
                   ('worker1', 'object2', -4.399898705211159),
                   ('worker2', 'object2', -0.700100702612725),
                   ('worker3', 'object3', 2.645722067195676)]

        expectedObjectsList = self.getObjectCountsList(assigns, False)

        newAssigns = [('worker1', 'object3', -2.0491697316789894)]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssigns)

    @data('GALC')
    def test_CountAssignsCalculator_GetNextObject_DifferentLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 4.399898705211159),
                   ('worker2', 'object1', 2.399898705211159),
                   ('worker1', 'object2', -4.399898705211159),
                   ('worker2', 'object2', -0.700100702612725),
                   ('worker3', 'object2', 2.645722067195676)]

        expectedObjectsList = self.getObjectCountsList(assigns, False)

        newAssigns = [('worker1', 'object3', -2.0491697316789894)]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssigns)

    @data('GALC')
    def test_CountAssignsCalculator_GetNextWorkerObject_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 4.399898705211159),
                   ('worker2', 'object2', 2.399898705211159),
                   ('worker3', 'object2', -4.399898705211159),
                   ('worker2', 'object3', -0.700100702612725),
                   ('worker3', 'object3', 2.645722067195676)
                   ]

        expectedObjectsList = [('object2', 2), ('object3', 2)]
        newAssign = [('worker4', 'object2', 2.63272206719567)]
        excludedObjectsList = ['object1']

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssign, 'worker1', excludedObjectsList)

    @data('GALC')
    def test_CountAssignsCalculator_GetNextWorkerObject_DifferentLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 4.399898705211159),
                   ('worker2', 'object1', 2.399898705211159),
                   ('worker2', 'object2', -4.399898705211159),
                   ('worker3', 'object2', -0.700100702612725),
                   ('worker3', 'object3',  2.645722067195676)]

        expectedObjectsList = [('object3', 1), ('object2', 2)]
        newAssign = [('worker4', 'object2', 3.54674687574)]
        excludedObjectsList = ['object1']

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssign, 'worker1', excludedObjectsList)

    @data('GALC')
    def test_CostBasedCalculator_GetNextObject_SameLabelCounts(self, algorithm):
        calculator = 'costbased'
        assigns = [('worker1', 'object1', 10.000000434),
                   ('worker2', 'object1', 20.00000121),
                   ('worker2', 'object2', 30.00001133),
                   ('worker3', 'object2', 140.0405070807049)
                   ]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)

@ddt
class TestNormalScheduler(unittest.TestCase):

    def setUp(self):
        self.client = TroiaContClient(ADDRESS)
        self.scheduler = 'normalscheduler'

    def tearDown(self):
        self.client.delete()

    def _createTestPrereq(self, algorithm, scheduler, calculator, assigns=ASSIGNED_LABELS_CONT):
        response = self.client.create(
            algorithm=algorithm,
            scheduler=scheduler,
            prioritycalculator=calculator
        )

        if calculator == 'countassigns':
            self.assertEqual('OK', response['status'])
            self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns))['status'])
            self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])
        else:
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('class com.datascience.scheduler.CostBasedPriorityCalculator supports only NominalProjects, not class com.datascience.galc.ContinuousProject', response['result'])

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
        pass

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

    @data('GALC')
    def test_CountAssignsCalculator_GetNextObject_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 4.399898705211159),
                   ('worker1', 'object2', 1.455345344678543),
                   ('worker2', 'object1', -2.232434324324),
                   ('worker2', 'object2', 3.21413241341)]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        sortedList = self.getObjectCountsList(assigns, False)
        minValue = sortedList[0][1]
        expectedObjectList = [o[0] for o in sortedList if o[1] == minValue]

        newAssign = [('worker3', 'object3', 2.343432532534)]
        self._runTestMethod(calculator, expectedObjectList, newAssign)

    @data('GALC')
    def test_CountAssignsCalculator_GetNextObject_DifferentLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 4.399898705211159),
                   ('worker2', 'object1', 1.455345344678543),
                   ('worker1', 'object2', -2.232434324324),
                   ('worker2', 'object2', 3.21413241341),
                   ('worker3', 'object2', 2.343432532534),
                   ]
        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        sortedList = self.getObjectCountsList(assigns, False)
        minValue = sortedList[0][1]
        expectedObjectsList = [o[0] for o in sortedList if o[1] == minValue]

        newAssign = [('worker1', 'object3', 1.12343432532534)]
        self._runTestMethod(calculator, expectedObjectsList, newAssign)

    @data('GALC')
    def test_CountAssignsCalculator_GetNextWorkerObject_SameLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 10.000000434),
                   ('worker2', 'object1', 20.00000121),
                   ('worker2', 'object2', 30.00001133),
                   ('worker3', 'object2', 140.0405070807049),
                   ('worker3', 'object3', 1018375.248483994),
                   ('worker4', 'object3', 10384746.364646522)
                   ]

        expectedObjectsList = ['object3', 'object2']
        newAssigns = [('worker4', 'object4', 343573.434353452)]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssigns, 'worker1')

    @data('GALC')
    def test_CountAssignsCalculator_GetNextWorkerObject_DifferentLabelCounts(self, algorithm):
        calculator = 'countassigns'
        assigns = [('worker1', 'object1', 1.423432433248882),
                   ('worker2', 'object1', 23.325325325345345),
                   ('worker2', 'object2', 0.897868767634443),
                   ('worker3', 'object2', -264.43284327432453),
                   ('worker4', 'object2', -123.45734957347543),
                   ('worker3', 'object3', 768.43439743643328)
                   ]

        expectedObjectsList = ['object3']
        newAssigns = [('worker4', 'object3', 100.3733435)]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
        self._runTestMethod(calculator, expectedObjectsList, newAssigns, 'worker1')

    @data('GALC')
    def test_CostBasedCalculator_GetNextObject_SameLabelCounts(self, algorithm):
        calculator = 'costbased'
        assigns = [('worker1', 'object1', 10.000000434),
                   ('worker2', 'object1', 20.00000121),
                   ('worker2', 'object2', 30.00001133),
                   ('worker3', 'object2', 140.0405070807049)
                   ]

        self._createTestPrereq(algorithm, self.scheduler, calculator, assigns)
