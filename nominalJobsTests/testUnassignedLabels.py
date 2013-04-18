# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *


class TestUnassignedLabels(unittest.TestCase):
    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def get_priors(self, categories):
        return [{'categoryName': c, "value": 1. / len(categories)} for c in categories]

    def tearDown(self):
        self.client.delete()

    def _test_method(self, categories, priors, unassignedLabels, expectedProbabilities):
        response = self.client.create(categories, categoryPriors=priors, algorithm="BMV")
        self.assertEqual('OK', response['status'])

        #post the unassigned labels
        response = self.client.await_completion(self.client.post_objects(unassignedLabels))
        self.assertEqual('OK', response['status'])

        #get the unassigned labels
        response = self.client.await_completion(self.client.get_objects())
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(unassignedLabels), len(response['result']))
        if (unassignedLabels):
            result = response['result'][0]
            self.assertEqual(unassignedLabels[0], result['name'])

    def test_AddGetObjects_EmptyLabels(self):
        self._test_method(CATEGORIES, CATEGORY_PRIORS, [], [])

    def test_AddGetUnassignedLabels_LongLabelNames(self):
        categories = ["category1", "category2"]
        priors = [{"categoryName": "category1", "value": 0.0000000001}, {"categoryName": "category2", "value": 0.9999999999}]
        unassignedLabels = ["hjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdh"]
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        self._test_method(categories, priors, unassignedLabels, expectedProbabilities)

    def test_AddGetUnassignedLabels_PrintableASCII_RegularChars(self):
        categories = ["category1", "category2", "category3", "category4"]
        unassignedLabels = ["testObject1"]
        expectedProbabilities = [('category1', 0.25),
                                 ('category2', 0.25),
                                 ('category3', 0.25),
                                 ('category4', 0.25)]
        self._test_method(categories, self.get_priors(categories), unassignedLabels, expectedProbabilities)

    def test_AddGetUnassignedLabels_PrintableASCII_SpecialChars(self):
        categories = ["category1", "category2", "category3"]
        unassignedLabels = ["~!@#$%^&*()_+=-[]{}|:;<> ,./"]
        expectedProbabilities = [('category1', 0.3333333333333333),
                                 ('category2', 0.3333333333333333),
                                 ('category3', 0.3333333333333333)]
        self._test_method(categories, self.get_priors(categories), unassignedLabels, expectedProbabilities)

    def test_AddGetUnassignedLabels_ExtendedASCIIChars(self):
        categories = ["category1", "category2"]
        unassignedLabels = [u"ëñµ¼Úæ"]
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        self._test_method(categories, self.get_priors(categories), unassignedLabels, expectedProbabilities)

    def test_AddGetUnassignedLabels_UnicodeChars(self):
        categories = ["category1", "category2"]
        unassignedLabels = [u"ూഹܬआਖ਼"]
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        self._test_method(categories, self.get_priors(categories), unassignedLabels, expectedProbabilities)

    def test_GetObjectAssigns(self):
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

    def test_GetObjectInfo(self):
        response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS)
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
            self.assertEqual(dist['value'], 0.5 if label['name'] in objects_without_assigns else 0.9 if dist['categoryName'] == 'porn' else 0.1)

if __name__ == '__main__':
    unittest.main()
