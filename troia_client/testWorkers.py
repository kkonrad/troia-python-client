# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
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
        self.assertEqual([], response['result'])

#    def test_AddGetWorkers_BeforeCompute(self):
#        self.client.create(CATEGORIES)
#        self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
#        self.client.await_completion(self.client.post_gold_data(GOLD_SAMPLES))
#        response = self.client.await_completion(self.client.get_workers())
#        defaultConfusionMatrix = [{u'to': u'porn', u'from': u'porn', u'value': u'90.0'}, {u'to': u'notporn', u'from': u'porn', u'value': u'10.0'}, 
#                                  {u'to': u'porn', u'from': u'notporn', u'value': u'10.0'}, {u'to': u'notporn', u'from': u'notporn', u'value': u'90.0'}]
#        for worker, results in response['result'].iteritems():
#            self.assertEqual(defaultConfusionMatrix, results['Confusion matrix'])
#            self.assertEqual(5, results['Number of annotations'])
#            self.assertEqual(2, results['Gold tests'])

    def test_AddGetWorkers_AfterCompute(self):
        self.client.create(CATEGORIES)
        self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
        self.client.await_completion(self.client.post_compute())

        #assigns check
        response = self.client.await_completion(self.client.get_workers())
        for w in response['result']:
            for a in w['assigns']:
                self.assertTrue((a['worker'], a['lobject']['name'], a['label']) in ASSIGNED_LABELS)
        
        #confusion matrices check
        response = self.client.await_completion(self.client.get_workers_confusion_matrix())
        exp = {
         u'worker1': [{u'to': u'porn', u'from': u'porn', u'value': 100.0}, {u'to': u'notporn', u'from': u'porn', u'value': 0.0}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': 100.0}, {u'to': u'notporn', u'from': u'notporn', u'value': 0.0}], 
         u'worker3': [{u'to': u'porn', u'from': u'porn', u'value': 0.0}, {u'to': u'notporn', u'from': u'porn', u'value': 100.0}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': 100.0}, {u'to': u'notporn', u'from': u'notporn', u'value': 0.0}], 
         u'worker2': [{u'to': u'porn', u'from': u'porn', u'value': 33.333}, {u'to': u'notporn', u'from': u'porn', u'value': 66.667}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': 100.0}, {u'to': u'notporn', u'from': u'notporn', u'value': 0.0}], 
         u'worker5': [{u'to': u'porn', u'from': u'porn', u'value': 100.0}, {u'to': u'notporn', u'from': u'porn', u'value': 0.0}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': 0.0}, {u'to': u'notporn', u'from': u'notporn', u'value': 100.0}], 
         u'worker4': [{u'to': u'porn', u'from': u'porn', u'value': 0.0}, {u'to': u'notporn', u'from': u'porn', u'value': 100.0}, 
                      {u'to': u'porn', u'from': u'notporn', u'value': 100.0}, {u'to': u'notporn', u'from': u'notporn', u'value': 0.0}]}

        for w in response['result']:
            worker_name = w['workerName']
            for e1 in w['value']['matrix']:
                exists = False
                for e2 in exp[worker_name]:
                    if e2['to'] == e1['to'] and e2['from'] == e1['from']:
                        exists = True
                        self.assertAlmostEqual(
                           e2['value'], 
                           e1['value'], 
                           2, 
                           "{}, from: {}, to: {}. expected:{}, was: {}".format(worker_name, e1['from'], e1['to'], e2['value'], e1['value']))
                self.assertTrue(exists)
