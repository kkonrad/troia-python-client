# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *


class TestUnassignedLabels(unittest.TestCase):
    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def _test_method(self, categories, unassignedLabels, expectedProbabilities):
        response = self.client.create(categories, algorithm="BMV")
        self.assertEqual('OK', response['status'])

        #post the assigned labels
        response = self.client.await_completion(self.client.post_objects(unassignedLabels))
        self.assertEqual('OK', response['status'])

        #get the unassigned labels
        response = self.client.await_completion(self.client.get_objects())
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(unassignedLabels), len(response['result']))
        if (unassignedLabels):
            result = response['result'][0]
            self.assertEqual(unassignedLabels[0], result['name'])

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
        response = self.client.await_completion(self.client.post_objects(unassignedLabel))
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.get_objects())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(6, len(result))
        results = []
        for object in result:
            if object['name'] not in unassignedLabel:
                assigns = self.client.await_completion(self.client.get_object_assigns(object['name']))['result']
                for a in assigns:
                    results.append((a['worker'], a['object'], a['label']))
        for label in ASSIGNED_LABELS:
            self.assertTrue(label in results)

    def test_AddGetData_AllLabels(self):
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.post_assigned_labels([('worker1', 'url1', 'porn'), ('worker1', 'url2', 'porn')]))
        self.assertEqual('OK', response['status'])

        #post the unassigned label
        objects_without_assigns = ["newUnassignedLabel"]
        response = self.client.await_completion(self.client.post_objects(objects_without_assigns))
        self.assertEqual('OK', response['status'])

        #get labels
        response = self.client.await_completion(self.client.get_objects())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(3, len(result))
        self.client.await_completion(self.client.post_compute())
        for label in result:
            response = self.client.await_completion(self.client.get_probability_distribution(label['name']))
            dist = response['result'][0]
            self.assertEqual(dist['value'], 0.5 if label['name'] in objects_without_assigns else 1.0 if dist['categoryName'] == 'porn' else 0.0)

if __name__ == '__main__':
    unittest.main()
