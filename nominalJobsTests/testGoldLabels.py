﻿# -*- coding: UTF-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *


class TestGoldLabels(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

    def tearDown(self):
        self.client.delete()

    def _test_method(self, goldLabels):
        response = self.client.await_completion(self.client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])

        #get the gold labels
        response = self.client.await_completion(self.client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(len(goldLabels), len(result))

        results = [tuple(receivedLabel.values()) for receivedLabel in response['result']]
        for label in goldLabels:
            self.assertTrue(label in results)

    def test_AddGetEmptyGoldLabels(self):
        self._test_method([])

    def test_AddGetGoldLabel_LongLabelName(self):
        response = self.client.await_completion(self.client.post_gold_data([("sdgfdgfgfhdsjgfhgfhgfhhjhgjhjjghghkgkhjkfklsdjfkljssdgfdgfgfhdsjgfhgfhgfhhjhgjhjjghghkgkhjkfklsdjfkljs", "notporn")]))
        self.assertEqual('ERROR', response['status'])
        self.assertEqual('Internal error: Object name should be shorter than 100 chars', response['result'])

    def test_AddGetGoldLabel_PrintableASCII_RegularChars(self):
        self._test_method([("url1", "notporn")])

    def test_AddGetGoldLabel_PrintableASCII_SpecialChars(self):
        self._test_method([("~!@#^&*()_+=-[]{}:<>,./", "notporn")])

    def test_AddGetGoldLabel_ExtendedASCIIChars(self):
        self._test_method([(u"™ž¤©", "notporn")])

    def test_AddGetGoldLabel_UnicodeChars(self):
        self._test_method([(u"ૉେஇ", "notporn")])

if __name__ == '__main__':
    unittest.main()
