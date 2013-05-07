# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *


class TestAssignedLabels(unittest.TestCase):
        def setUp(self):
            self.client = TroiaClient(ADDRESS)

        def tearDown(self):
            self.client.delete()

        def _test_method(self, assigned_labels):
            #post the assigned labels
            response = self.client.await_completion(self.client.post_assigned_labels(assigned_labels))
            self.assertEqual('OK', response['status'])

            #get the assigned labels
            response = self.client.await_completion(self.client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            self.assertEqual(len(response['result']), len(assigned_labels))
            results = [(l['worker'], l['object'], l['label']) for l in response['result']]
            for label in assigned_labels:
                self.assertTrue(label in results)

        def test_AddGetEmptyAssignedLabels(self):
            response = self.client.create(CATEGORIES, categoryPriors=CATEGORY_PRIORS, costMatrix=COST_MATRIX)
            self.assertEqual('OK', response['status'])
            self._test_method([])

        def test_AddAssignedLabelsWithInvalidCategory(self):
            categories = ["category1", "category2"]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            #post the assigned labels
            assignedLabels = [('worker1', 'url1', 'category3')]
            response = self.client.await_completion(self.client.post_assigned_labels(assignedLabels))
            self.assertEqual('ERROR', response['status'])

            #get the assigned labels
            response = self.client.await_completion(self.client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertFalse(result)

        def test_AddGetAssignedLabels_LongLabelNames(self):
            categories = ['category1', "category2"]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            response = self.client.await_completion(self.client.post_assigned_labels([('hjkdhfhdfgjkshfghdsgffgfhfghgjhghjgjgjgjgjgjgjldkgj', 'object_dsjgfhgfhgfhhjdfhgjghghkgkhjkfklsdjfkljsdfj', 'category1')]))
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Internal error: Worker name should be shorter than 50 chars', response['result'])

        def test_AddGetAssignedLabels_PrintableASCII_RegularChars(self):
            response = self.client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
            self._test_method(ASSIGNED_LABELS)

        def test_AddGetAssignedLabels_PrintableASCII_SpecialChars(self):
            categories = ['category1', "category2", "category3"]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            self._test_method([('a%a', '~!@#$%^&*()_+=-[]{}|:;<> ,./', 'category1'),
                ('b%%b', '%%%', 'category2'),
                ('c%%!<>c', '~!@#$^&*[](){}-_+=<>?/.,;:', 'category3')])

        def test_AddGetAssignedLabels_ExtendedASCIIChars(self):
            categories = ['category1', "category2", "category3"]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            self._test_method([(u'®¶', u'œŒ', 'category1'),
                (u'ÀÆË', u'™ž¤©', 'category2'),
                (u'ëñ', u'µ¼Úæ', 'category3')])

        def test_AddGetAssignedLabels_UnicodeChars(self):
            categories = ['category1', "category2", "category3"]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            self._test_method([(u'ૉେஇ', u'ΨҖӖմ؂څ', 'category1'),
                (u'ూഹ', u'ܬआਖ਼', 'category2')])

if __name__ == '__main__':
    unittest.main()
