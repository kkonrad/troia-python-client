# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *


class TestCategories(unittest.TestCase):

        def setUp(self):
            self.client = TroiaClient(ADDRESS)

        def tearDown(self):
            self.client.delete()

        def _test_method(self, categories):
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])
            for category in categories:
                self.assertTrue(category in response['result'])

        def _create_priors(self, categories, priors):
            return [{'categoryName': c, "value": p} for c, p in zip(categories, priors)]

        def test_AddGetCategories_LongCategoryNames(self):
            categories = [u'hjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdh', u'hjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhsdsd']
            self._test_method(categories)

        def test_AddGetCategories_PrintableASCII_SpecialChars(self):
            categories = [u'!@#$:;,.{}[]', u'2ndCategory']
            self._test_method(categories)

        def test_AddGetCategories_ExtendedASCIIChars(self):
            categories = [u'œŒ', u'ÀÆË™ž¤©']
            self._test_method(categories)

        def test_AddGetCategories_UnicodeChars(self):
            categories = [u'ૉେஇΨҖӖմ؂څ', u'ూഹܬआਖ਼']
            self._test_method(categories)

        def test_CreateJobWithoutCategoryPriors_GetPriors(self):
            categories = [u'category1', u'category2']
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])
            for category in categories:
                self.assertTrue(category in response['result'])

        def test_CreateJobWithCategoryPriors_GetPriors(self):
            categories = [u'category1', u'category2']
            priors = [0.3, 0.7]
            response = self.client.create(categories, categoryPriors=self._create_priors(categories, priors))
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])
            for category in categories:
                self.assertTrue(category in response['result'])

        def test_CreateJobWithoutCostMatrix_2Categories_GetCostMatrix(self):
            categories = [u'category1', u'category2']
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_cost_matrix())
            self.assertEqual('OK', response['status'])

            #check that the default 0-1 cost matrix is created
            for matrix_value in response['result']:
                self.assertEqual(0.0 if matrix_value['from'] == matrix_value['to'] else 1.0, matrix_value['value'])

        def test_CreateJobWithoutCostMatrix_3Categories_GetCostMatrix(self):
            categories = [u'category1', u'category2', u'category3']
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_cost_matrix())
            self.assertEqual('OK', response['status'])

            #check that the default 0-1 cost matrix is created
            for matrix_value in response['result']:
                self.assertEqual(0.0 if matrix_value['from'] == matrix_value['to'] else 1.0, matrix_value['value'])

        def test_CreateJobWithCostMatrix_GetCostMatrix(self):
            categories = [u'category1', u'category2', u'category3']
            cMatrix = [{"from": "category1", "to": "category1", "value": 0.0}, {"from": "category1", "to": "category2", "value": 0.5}, {"from": "category1", "to": "category3", "value": 0.5},
                       {"from": "category2", "to": "category1", "value": 0.5}, {"from": "category2", "to": "category2", "value": 0.0}, {"from": "category2", "to": "category3", "value": 0.5},
                       {"from": "category3", "to": "category1", "value": 0.5}, {"from": "category3", "to": "category2", "value": 0.5}, {"from": "category3", "to": "category3", "value": 0.0}]
            response = self.client.create(categories, costMatrix=cMatrix)
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            for matrix_value in response['result']:
                self.assertEqual(0.0 if matrix_value['from'] == matrix_value['to'] else 0.5, matrix_value['value'])
