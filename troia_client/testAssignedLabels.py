# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *


class TestAssignedLabels(unittest.TestCase):
        def setUp(self):
            self.client = TroiaClient(ADDRESS)

        def tearDown(self):
            self.client.delete()

        def _test_method(self, assigned_labels):
            #post the empty assigned labels
            response = self.client.await_completion(self.client.post_assigned_labels(assigned_labels))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])

            #get the assigned labels
            response = self.client.await_completion(self.client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            self.assertEqual(len(response['result']), len(assigned_labels))
            results = [tuple(receivedLabel.values()) for receivedLabel in response['result']]
            for label in assigned_labels:
                self.assertTrue(label in results)

        def test_AddGetEmptyAssignedLabels(self):
            response = self.client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
            self._test_method([])

        def test_AddAssignedLabelsWithInvalidCategory(self):
            categories = [{"prior":0.3, "name":"category1"}, {"prior":0.7, "name":"category2"}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            #post the assigned labels
            assignedLabels = [('worker1', 'url1', 'category3')]
            response = self.client.await_completion(self.client.post_assigned_labels(assignedLabels))
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Internal error: attempting to add invalid category: category3', response['result'])

            #get the assigned labels
            response = self.client.await_completion(self.client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertFalse(result)

        def test_AddGetAssignedLabels_PrintableASCII_RegularChars(self):
            response = self.client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
            self._test_method(ASSIGNED_LABELS)

        def test_AddGetAssignedLabels_PrintableASCII_SpecialChars(self):
            categories = [{"prior":0.4, "name":"category1"},
                          {"prior":0.239, "name":"category2"},
                          {"prior":0.361, "name":"category3"}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            self._test_method([('a%a', '~!@#$%^&*()_+=-[]{}|:;<> ,./', 'category1'),
                ('b%%b', '%%%', 'category2'),
                ('c%%!<>c', '~!@#$^&*[](){}-_+=<>?/.,;:', 'category3')])

        def test_AddGetAssignedLabels_ExtendedASCIIChars(self):
            categories = [{"prior":0.4, "name":"category1"},
                {"prior":0.239, "name":"category2"},
                {"prior":0.361, "name":"category3"}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            self._test_method([('®¶', 'œŒ', 'category1'),
                ('ÀÆË', '™ž¤©', 'category2'),
                ('ëñ', 'µ¼Úæ', 'category3')])

        def test_AddGetAssignedLabels_UnicodeChars(self):
            categories = [{"prior":0.4, "name":"category1"},
                {"prior":0.239, "name":"category2"},
                {"prior":0.361, "name":"category3"}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            self._test_method([('ૉେஇ', 'ΨҖӖմ؂څ', 'category1'),
                ('ూഹ', 'ܬआਖ਼', 'category2')])

if __name__ == '__main__':
    unittest.main()
