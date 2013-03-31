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

        def test_AddGetCategories_SameCategoryNames(self):
            categories = [u'category1', u'category1']
            response = self.client.create(categories)
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('There should be at least two categories', response['result'])

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

        def test_CreateJobWithCategoryPriors_GetPriors(self):
            categories = [u'category1', u'category2']
            priors = [0.3, 0.7]
            response = self.client.create(categories, categoryPriors=self._create_priors(categories, priors))
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])

        def test_CreateJobWithoutCostMatrix_GetCostMatrix(self):
            categories = [u'category1', u'category2']
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            print response

        def test_CreateJobWithCostMatrix_GetCostMatrix(self):
            categories = [u'category1', u'category2']
            response = self.client.create(categories, costMatrix=COST_MATRIX)
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            print response

