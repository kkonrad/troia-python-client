# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *


class TestWorkers(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def test_AddGetEmptyWorkers(self):
        self.client.create(CATEGORIES)
        self.client.await_completion(self.client.post_compute())
        response = self.client.await_completion(self.client.get_workers())
        self.assertEqual('OK', response['status'])
        self.assertEqual({}, response['result'])

    def test_AddGetWorkers_BeforeCompute(self):
        self.client.create(CATEGORIES)
        self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
        self.client.await_completion(self.client.post_gold_data(GOLD_SAMPLES))
        response = self.client.await_completion(self.client.get_workers())
        defaultConfusionMatrix = [{u'to': u'porn', u'from': u'porn', u'value': u'90.0'}, {u'to': u'notporn', u'from': u'porn', u'value': u'10.0'}, 
                                  {u'to': u'porn', u'from': u'notporn', u'value': u'10.0'}, {u'to': u'notporn', u'from': u'notporn', u'value': u'90.0'}]
        for worker, results in response['result'].iteritems():
            self.assertEqual(defaultConfusionMatrix, results['Confusion matrix'])
            self.assertEqual(5, results['Number of annotations'])
            self.assertEqual(2, results['Gold tests'])

    def test_AddGetWorkers_AfterCompute(self):
        self.client.create(CATEGORIES)
        self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
        self.client.await_completion(self.client.post_compute())
        response = self.client.await_completion(self.client.get_workers())

        expectedResults = {
         u'worker1': [{u'to': u'porn', u'from': u'porn', u'value': u'100.0'}, {u'to': u'notporn', u'from': u'porn', u'value': u'0.0'}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': u'100.0'}, {u'to': u'notporn', u'from': u'notporn', u'value': u'0.0'}], 
         u'worker3': [{u'to': u'porn', u'from': u'porn', u'value': u'0.0'}, {u'to': u'notporn', u'from': u'porn', u'value': u'100.0'}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': u'100.0'}, {u'to': u'notporn', u'from': u'notporn', u'value': u'0.0'}], 
         u'worker2': [{u'to': u'porn', u'from': u'porn', u'value': u'33.333'}, {u'to': u'notporn', u'from': u'porn', u'value': u'66.667'}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': u'100.0'}, {u'to': u'notporn', u'from': u'notporn', u'value': u'0.0'}], 
         u'worker5': [{u'to': u'porn', u'from': u'porn', u'value': u'100.0'}, {u'to': u'notporn', u'from': u'porn', u'value': u'0.0'}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': u'0.0'},{u'to': u'notporn', u'from': u'notporn', u'value': u'100.0'}], 
         u'worker4': [{u'to': u'porn', u'from': u'porn', u'value': u'0.0'}, {u'to': u'notporn', u'from': u'porn', u'value': u'100.0'}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': u'100.0'}, {u'to': u'notporn', u'from': u'notporn', u'value': u'0.0'}]}

        actualResults = {}
        for worker, results in response['result'].iteritems():
            self.assertEqual(5, results['Number of annotations'])
            self.assertEqual(0, results['Gold tests'])
            actualResults[worker] = results['Confusion matrix']
        self.assertEqual(expectedResults, actualResults)

    def test_AddGetWorker(self):
        self.client.create(CATEGORIES)
        self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
        self.client.await_completion(self.client.post_compute())
        response = self.client.await_completion(self.client.get_worker("worker1"))
        expectedConfusionMatrix = [{u'to': u'porn', u'from': u'porn', u'value': u'100.0'}, {u'to': u'notporn', u'from': u'porn', u'value': u'0.0'}, 
                                   {u'to': u'porn', u'from': u'notporn', u'value': u'100.0'}, {u'to': u'notporn', u'from': u'notporn', u'value': u'0.0'}]
        self.assertEqual(5, response['result']['Number of annotations'])
        self.assertEqual(0, response['result']['Gold tests'])
        self.assertEqual(expectedConfusionMatrix, response['result']['Confusion matrix'])
