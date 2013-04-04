# -*- coding: utf-8 -*-
import unittest
import random
from ddt import ddt, data
from client.gal import TroiaClient
from testSettings import *

@ddt
class TestCachedScheduler(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        self.scheduler = 'cachedscheduler'

    def tearDown(self):
        self.client.delete()

    def _generateAssigns(self, assignsGenModel, num_objects):
        assigns = []
        if assignsGenModel == 'differentCounts':
            for i in xrange(num_objects):
                for j in xrange(i + 1):
                    assigns.append((
                        'worker{}'.format(j),
                        'object{}'.format(i),
                         CATEGORIES[random.randint(0, len(CATEGORIES) - 1)]
                    ))
        if assignsGenModel == 'sameCounts':
            for i in xrange(num_objects):
                for j in xrange(num_objects):
                    assigns.append((
                        'worker{}'.format(j),
                        'object{}'.format(i),
                         CATEGORIES[random.randint(0, len(CATEGORIES) - 1)]
                    ))
        if assignsGenModel == 'sameCosts':
            for i in xrange(num_objects):
                for j in xrange(num_objects):
                    assigns.append((
                        'worker{}'.format(j),
                        'object{}'.format(i),
                         CATEGORIES[1]
                    ))
        if assignsGenModel == 'differentCosts':
            for i in xrange(num_objects):
                for j in xrange( i + 1):
                    assigns.append((
                        'worker{}'.format(j),
                        'object{}'.format(i),
                         CATEGORIES[i]
                    ))
        print assigns
        return assigns

    def _createTestPrereq(self, algorithm, scheduler, calculator, assigns,  categoryPriors):
        response = self.client.create(
            CATEGORIES,
            categoryPriors=categoryPriors,
            costMatrix=COST_MATRIX,
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
        assignsGenerationModel = 'differentCounts'
        noObjects = 3
        expectedObjectsQueue = ['object0', 'object1', 'object2']
        newAssign = [('worker0', 'object1', CATEGORIES[1])]
        expectedObject = 'object1'
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_DifferentLabelCounts_AddEmptyAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'differentCounts'
        noObjects = 3
        expectedObjectsQueue = ['object0', 'object1', 'object2']
        newAssign = []
        expectedObject = None
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_SameLabelCounts_AddNewAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'sameCounts'
        noObjects = 2
        expectedObjectsQueue = ['object0', 'object1']
        newAssign = [('worker3', 'object0', CATEGORIES[1])]
        expectedObject = 'object0'
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CountAssignsCalculator_SameLabelCounts_AddEmptyAssign(self, algorithm):
        calculator = 'countassigns'
        assignsGenerationModel = 'sameCounts'
        noObjects = 2
        expectedObjectsQueue = ['object0', 'object1']
        newAssign = []
        expectedObject = None
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    def _test_method(self, algorithm, scheduler, calculator, assignsGenModel, noObjects, categoryPriors=CATEGORY_PRIORS):
        assigns = self._generateAssigns(assignsGenModel, noObjects)
        self._createTestPrereq(algorithm, scheduler, calculator, assigns, categoryPriors)

    def _check_results(self, expectedObjectsQueue, newAssign, expectedObject):
        for i in xrange(len(expectedObjectsQueue)):
            response = self.client.await_completion(self.client.get_next_object())
            self.assertEqual(expectedObjectsQueue[i], response['result']['name'])

        # This one should be null. That means the 'result' key is not present in the response.
        self.assertIsNone(self.client.await_completion(self.client.get_next_object()).get('result', None))

        # Add assign to the object. The object should be returned by subsequent 'nextObject' call.
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(newAssign))['status'])
        response = self.client.await_completion(self.client.get_next_object())
        if response.get('result') == None:
            self.assertIsNone(expectedObject)
        else:
            self.assertEqual(expectedObject, response['result']['name'])

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def est_CachedScheduler_CostBasedCalculator_SameCosts(self, algorithm):
        calculator = 'costbased'
        assignsGenerationModel = 'sameCosts'
        noObjects = 3
        categoryPriors = [{"categoryName": "porn", "value": 0.1}, {"categoryName": "notporn", "value": 0.9}]
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects)
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))
        self.assertEquals("OK", response['status'])
        resDict = {}
        for result in response['result']:
            resDict[result['objectName']] = result['value']
        #sort the objects descending, based on cost 
        expectedObjectsQueue = [] 
        for key, value in sorted(resDict.iteritems(), key=lambda (k,v): (k, v)):
            expectedObjectsQueue.append(key)
        newAssign = []
        expectedObject = None
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)

    @data('BDS', 'IDS', 'BMV', 'IMV')
    def test_CachedScheduler_CostBasedCalculator_DifferentCosts(self, algorithm):
        print algorithm
        calculator = 'costbased'
        assignsGenerationModel = 'differentCosts'
        noObjects = 2
        categoryPriors = [{"categoryName": "porn", "value": 0.1}, {"categoryName": "notporn", "value": 0.9}]
        self._test_method(algorithm, self.scheduler, calculator, assignsGenerationModel, noObjects, categoryPriors)
        response = self.client.await_completion(self.client.get_estimated_objects_cost("ExpectedCost"))
        self.assertEquals("OK", response['status'])
        print response
        resDict = {}
        for result in response['result']:
            resDict[result['objectName']] = result['value']
        #sort the objects descending, based on cost 
        expectedObjectsQueue = [] 
        for key, value in sorted(resDict.iteritems(), key=lambda (k,v): (k,v)):
            print "%s: %s" % (key, value)
            expectedObjectsQueue.append(key)
        newAssign = []
        expectedObject = None
        self._check_results(expectedObjectsQueue, newAssign, expectedObject)


class TestNormalScheduler(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def est_IMV_CachedScheduler_CountAssignsCalculator(self):
        self._test_method('IMV')

    def est_IDS_CachedScheduler_CountAssignsCalculator(self):
        self._test_method('IDS')

    def est_BMV_CachedScheduler_CountAssignsCalculator(self):
        self._test_method('BMV')

    def est_BDS_CachedScheduler_CountAssignsCalculator(self):
        self._test_method('BDS')

    def _test_method(self, algorithm):
        response = self.client.create(
            CATEGORIES,
            categoryPriors=CATEGORY_PRIORS,
            costMatrix=COST_MATRIX,
            algorithm=algorithm,
            scheduler='normalscheduler',
            calculator='countassigns'
        )
        self.assertEqual('OK', response['status'])
        num_objects = 3
        assigns = []
        for i in xrange(num_objects):
            for j in xrange(i + 1):
                assigns.append((
                    'worker{}'.format(j),
                    'object{}'.format(i),
                    CATEGORIES[random.randint(0, len(CATEGORIES) - 1)]
                ))
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns))['status'])
        self.assertEqual('OK', self.client.await_completion(self.client.post_compute())['status'])

        # Get created objects.
        objects = self.client.await_completion(self.client.get_objects())['result']
        self.assertEquals(num_objects, len(objects))
        #we have object0 = 3 assigns, object1 = 6 assigns, object2 = 9 assigns

        #retrieve the objects from the queue:
        expectedObject = 'object2'
        for i in xrange(num_objects):
            response = self.client.await_completion(self.client.get_next_object())
            self.assertEqual(expectedObject, self.client.await_completion(self.client.get_next_object())['result']['name'])

        # Add assign to the object
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns[-1:]))['status'])
        self.assertEqual(expectedObject, self.client.await_completion(self.client.get_next_object())['result']['name'])