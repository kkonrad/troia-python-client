# -*- coding: utf-8 -*-
import unittest
import random
from client.gal import TroiaClient
from testSettings import *


class TestCachedScheduler(unittest.TestCase):

    def test_IMV(self):
        self._test_method('IMV')

    def test_IDS(self):
        # TODO Incremental Dawid Skene
        # self._test_method('IDS')
        pass

    def test_BMV(self):
        self._test_method('BMV')

    def test_BDS(self):
        self._test_method('BDS')

    def _test_method(self, algorithm):
        client = TroiaClient(ADDRESS)
        response = client.create(
            CATEGORIES,
            categoryPriors=CATEGORY_PRIORS,
            costMatrix=COST_MATRIX,
            algorithm=algorithm,
            scheduler="cachedscheduler",
            calculator="countassigns"
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
        print assigns
        self.assertEqual('OK', client.await_completion(client.post_assigned_labels(assigns))['status'])
        self.assertEqual('OK', client.await_completion(client.post_compute())['status'])

        # Get created objects.
        objects = client.await_completion(client.get_objects())['result']

        # Get all objects from the queue.
        for i in xrange(num_objects):
            print objects[i]['name']
            self.assertEqual( objects[i]['name'], client.await_completion(client.get_next_object())['result']['name'])
        # This one should be null. That means the 'result' key is not present
        # in the response.
        self.assertIsNone(client.await_completion(client.get_next_object()).get('result', None))
        # Add assign to the object. The object should be evicted from the
        # cache and returned by subsequent 'nextObject' call.
        self.assertEqual('OK', client.await_completion(client.post_assigned_labels(assigns[-1:]))['status'])
        self.assertEqual(objects[-1]['name'], client.await_completion(client.get_next_object())['result']['name'])
        client.delete()
