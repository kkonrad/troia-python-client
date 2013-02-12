# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *

class TestGoldLabels(unittest.TestCase):
    
    def test_AddGetEmptyGoldLabels(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
             
        #post the empty gold labels
        goldLabels = []
        response = client.await_completion(client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])
            
        #get the gold labels
        response = client.await_completion(client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertFalse(result)   
    
    
    def test_AddGetGoldLabel_PrintableASCII_RegularChars(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
             
        #post the gold labels
        expectedGoldLabels = [{"correctCategory": "notporn", "objectName": "url1"}]
        goldLabels = [("url1", "notporn")]
        response = client.await_completion(client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])
            
        #get the gold labels
        response = client.await_completion(client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        self.assertTrue(expectedGoldLabels[0] == result[0])
    
    def test_AddGetGoldLabel_PrintableASCII_SpecialChars(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
             
        #post the gold labels
        expectedGoldLabels = [{"correctCategory": "notporn", "objectName": "~!@#$^&*()_+=-[]{}|:;<> ,./"}]
        goldLabels = [("~!@#$^&*()_+=-[]{}|:;<> ,./", "notporn")]
        response = client.await_completion(client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])
            
        #get the gold labels
        response = client.await_completion(client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        self.assertTrue(expectedGoldLabels[0] == result[0])      
    
    def test_AddGetGoldLabel_ExtendedASCIIChars(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
             
        #post the gold labels
        expectedGoldLabels = [{"correctCategory": "notporn", "objectName": "™ž¤©"}]
        goldLabels = [("™ž¤©", "notporn")]
        response = client.await_completion(client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])
            
        #get the gold labels
        response = client.await_completion(client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        self.assertTrue(expectedGoldLabels[0] == result[0])     
    
    def test_AddGetGoldLabel_UnicodeChars(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
             
        #post the gold labels
        expectedGoldLabels = [{"correctCategory": "notporn", "objectName": "ૉେஇ"}]
        goldLabels = [("ૉେஇ", "notporn")]
        response = client.await_completion(client.post_gold_data(goldLabels))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])
            
        #get the gold labels
        response = client.await_completion(client.get_gold_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        self.assertTrue(expectedGoldLabels[0] == result[0])     
  


if __name__ == '__main__':
    unittest.main()