# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *


class TestUnassignedLabels(unittest.TestCase):
    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def _test_method(self, categories, unassignedLabels, expectedProbabilities):
        response = self.client.create(categories)
        self.assertEqual('OK', response['status'])

        #post the assigned labels
        response = self.client.await_completion(self.client.post_data(unassignedLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])

        #get the unassigned labels
        response = self.client.await_completion(self.client.get_data("unassigned"))
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(unassignedLabels), len(response['result']))
        if (unassignedLabels):
            result = response['result'][0]
            self.assertFalse(result['labels'])
            self.assertFalse(result['isGold'])
            self.assertEqual(unassignedLabels[0], result['name'])
            categoryProbabilies = [tuple(categoryProb.values()) for categoryProb in result['categoryProbability']]
            for categoryProb in categoryProbabilies:
                self.assertTrue(categoryProb in expectedProbabilities)

    def test_AddGetData_UnassignedLabels_EmptyLabels(self):
        self._test_method(CATEGORIES, [], [])

    def test_AddGetData_UnassignedLabel_LongLabelName(self):
        categories = [{"prior":"0.0000000001", "name":"category1"},
                      {"prior":"0.9999999999", "name":"category2"}]
        unassignedLabels = ["hjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdh"]
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        self._test_method(categories, unassignedLabels, expectedProbabilities)

    def test_AddGetData_UnassignedLabels_PrintableASCII_RegularChars(self):
        categories = [
                      {"prior":"0.1", "name":"category1"},
                      {"prior":"0.3", "name":"category2"},
                      {"prior":"0.5", "name":"category3"},
                      {"prior":"0.1", "name":"category4"}]
        unassignedLabels = ["testObject1"]
        expectedProbabilities = [('category1', 0.25),
                                 ('category2', 0.25),
                                 ('category3', 0.25),
                                 ('category4', 0.25)]
        self._test_method(categories, unassignedLabels, expectedProbabilities)

    def test_AddGetData_UnassignedLabels_PrintableASCII_SpecialChars(self):
        categories = [
                      {"prior":"0.2", "name":"category1"},
                      {"prior":"0.3", "name":"category2"},
                      {"prior":"0.5", "name":"category3"}]
        unassignedLabels = ["~!@#$%^&*()_+=-[]{}|:;<> ,./"]
        expectedProbabilities = [('category1', 0.3333333333333333),
                                 ('category2', 0.3333333333333333),
                                 ('category3', 0.3333333333333333)]
        self._test_method(categories, unassignedLabels, expectedProbabilities)

    def test_AddGetData_UnassignedLabels_ExtendedASCIIChars(self):
        categories = [{"prior":"0.2", "name":"category1"}, 
                      {"prior":"0.8", "name":"category2"}]
        unassignedLabels = [u"ëñµ¼Úæ"]
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        self._test_method(categories, unassignedLabels, expectedProbabilities)

    def test_AddGetData_UnassignedLabels_UnicodeChars(self):
        categories = [{"prior":0.2, "name":"category1"}, {"prior":0.8, "name":"category2"}]
        unassignedLabels = [u"ూഹܬआਖ਼"]
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        self._test_method(categories, unassignedLabels, expectedProbabilities)

    def test_AddGetData_AssignedLabels(self):
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS))
        self.assertEqual('OK', response['status'])

        #post the unassigned label
        unassignedLabel = [u"ూഹܬआਖ਼"]
        response = self.client.await_completion(self.client.post_data(unassignedLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])

        #get the unassigned labels
        response = self.client.await_completion(self.client.get_data("assigned"))
        self.assertEqual('OK', response['status'])
        result = response['result']
        results = []
        self.assertEqual(5, len(result))
        for object in result:
            labels = object['labels']
            for receivedLabel in labels:
                labelTouple = (receivedLabel['workerName'], receivedLabel['objectName'], receivedLabel['categoryName'])
                results.append(labelTouple)
        for label in ASSIGNED_LABELS:
            self.assertTrue(label in results)

    def test_AddGetData_AllLabels(self):
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

        assignedLabels = [('worker1', 'url1', 'porn'), ('worker1', 'url2', 'porn')]
        response = self.client.await_completion(self.client.post_assigned_labels(assignedLabels))
        self.assertEqual('OK', response['status'])

        #post the unassigned label
        unassignedLabel = ["newUnassignedLabel"]
        response = self.client.await_completion(self.client.post_data(unassignedLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])

        #get the unassigned labels
        response = self.client.await_completion(self.client.get_data("all"))
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(3, len(result))
        labels = {}
        for label in result:
            labels[label['name']] = label['labels']
            self.assertTrue({u'categoryName': u'porn', u'value': 0.5} in label['categoryProbability'])
            self.assertTrue({u'categoryName': u'notporn', u'value': 0.5} in label['categoryProbability'])
        self.assertEqual([{u'workerName': u'worker1', u'objectName': u'url1', u'categoryName': u'porn'}], labels['url1'])
        self.assertEqual([{u'workerName': u'worker1', u'objectName': u'url2', u'categoryName': u'porn'}], labels['url2'])
        self.assertEqual([], labels['newUnassignedLabel'])

if __name__ == '__main__':
    unittest.main()
