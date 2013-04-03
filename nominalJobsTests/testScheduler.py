# -*- coding: utf-8 -*-
import unittest
import random
from client.gal import TroiaClient
from testSettings import *


class TestCachedScheduler(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def test_IMV_CachedScheduler_CountAssignsCalculator(self):
        self._test_method('IMV')

    def test_IDS_CachedScheduler_CountAssignsCalculator(self):
        self._test_method('IDS')

    def test_BMV_CachedScheduler_CountAssignsCalculator(self):
        self._test_method('BMV')

    def test_BDS_CachedScheduler_CountAssignsCalculator(self):
        self._test_method('BDS')

    def _test_method(self, algorithm):
        response = self.client.create(
            CATEGORIES,
            categoryPriors=CATEGORY_PRIORS,
            costMatrix=COST_MATRIX,
            algorithm=algorithm,
            scheduler='cachedscheduler',
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
        expectedObjectsQueue = ['object2', 'object1', 'object0']
        for i in xrange(num_objects):
            response = self.client.await_completion(self.client.get_next_object())
            self.assertEqual(expectedObjectsQueue[i], self.client.await_completion(self.client.get_next_object())['result']['name'])

        # This one should be null. That means the 'result' key is not present in the response.
        self.assertIsNone(self.client.await_completion(self.client.get_next_object()).get('result', None))

        # Add assign to the object. The object should be evicted from the
        # cache and returned by subsequent 'nextObject' call.
        self.assertEqual('OK', self.client.await_completion(self.client.post_assigned_labels(assigns[-1:]))['status'])
        self.assertEqual(objects[-1]['name'], self.client.await_completion(self.client.get_next_object())['result']['name'])