# -*- coding: UTF-8 -*-
import unittest
from client import TroiaClient
from testSettings import *


class TestGoldLabels(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def test_AddGetEmptyGoldLabels(self):
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

        #post the empty gold labels
        goldLabels = []
        response = self.client.await_completion(self.client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])

        #get the gold labels
        response = self.client.await_completion(self.client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertFalse(result)

    def test_AddGetGoldLabel_PrintableASCII_RegularChars(self):
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

        #post the gold labels
        expectedGoldLabels = [{"correctCategory": "notporn", "objectName": "url1"}]
        goldLabels = [("url1", "notporn")]
        response = self.client.await_completion(self.client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])

        #get the gold labels
        response = self.client.await_completion(self.client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        self.assertTrue(expectedGoldLabels[0] == result[0])

    def test_AddGetGoldLabel_PrintableASCII_SpecialChars(self):
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

        #post the gold labels
        expectedGoldLabels = [{"correctCategory": "notporn", "objectName": "~!@#$^&*()_+=-[]{}|:;<> ,./"}]
        goldLabels = [("~!@#$^&*()_+=-[]{}|:;<> ,./", "notporn")]
        response = self.client.await_completion(self.client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])

        #get the gold labels
        response = self.client.await_completion(self.client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        self.assertTrue(expectedGoldLabels[0] == result[0])

    def test_AddGetGoldLabel_ExtendedASCIIChars(self):
        self.assertEqual('OK', response['status'])

        #post the gold labels
        goldLabels = [("™ž¤©", "notporn")]
        response = self.client.await_completion(self.client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])

        #get the gold labels
        response = self.client.await_completion(self.client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        expectedGoldLabel = [{u'correctCategory': u'notporn', u'objectName': u'™ž¤©'}]
        self.assertTrue(result[0] in expectedGoldLabel)

    def test_AddGetGoldLabel_UnicodeChars(self):
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

        #post the gold labels
        goldLabels = [("ૉେஇ", "notporn")]
        response = self.client.await_completion(self.client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])

        #get the gold labels
        response = self.client.await_completion(self.client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        expectedGoldLabel = [{u'correctCategory': u'notporn', u'objectName': u'ૉେஇ'}]
        self.assertTrue(result[0] in expectedGoldLabel)

if __name__ == '__main__':
    unittest.main()
