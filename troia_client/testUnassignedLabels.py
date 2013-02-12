# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *

class TestUnassignedLabels(unittest.TestCase):
    
    def test_AddGetUnassignedLabels_EmptyLabels(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
             
        #post the empty assigned labels
        response = client.await_completion(client.post_data([]))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
           
        #get the evaluation labels and check that the list is empty 
        response = client.await_completion(client.get_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertFalse(result)
        
    def test_AddGetUnassignedLabel_LongLabelName(self):
        client = TroiaClient(ADDRESS)
        categories = [{"prior":"0.0000000001", "name":"category1"}, {"prior":"0.9999999999", "name":"category2"}]
        response = client.create(categories)
        self.assertEqual('OK', response['status'])
             
        #post the empty assigned labels
        unassignedLabel = ["hjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdhfhdfgjkshfghdsfkgjldkgjfdkgjdflgjfkdljajdghafdhjkdh"];
        response = client.await_completion(client.post_data(unassignedLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
           
        #get the unassigned labels
        response = client.await_completion(client.get_data("unassigned"))
        self.assertEqual('OK', response['status'])
        self.assertEqual(1, len(response['result']))
        
        result = response['result'][0]
        self.assertFalse(result['labels'])
        self.assertFalse(result['isGold'])
        self.assertEqual(unassignedLabel[0], result['name'])
        
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        categoryProbabilies = []
        for categoryProb in result['categoryProbability']:
            probTouple = (categoryProb['categoryName'], categoryProb['value'])
            categoryProbabilies.append(probTouple)
        
        for categoryProb in categoryProbabilies:
            self.assertTrue(categoryProb in expectedProbabilities)

    def test_AddGetUnassignedLabels_PrintableASCII_RegularChars(self):
        client = TroiaClient(ADDRESS)
        categories = [
                      {"prior":"0.1", "name":"category1"}, 
                      {"prior":"0.3", "name":"category2"},
                      {"prior":"0.5", "name":"category3"},
                      {"prior":"0.1", "name":"category4"}]
        response = client.create(categories)
        self.assertEqual('OK', response['status'])
             
        #post the unassigned labelscategory2
        response = client.await_completion(client.post_data(["testObject1"]))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
            
        #get the unassigned labels
        response = client.await_completion(client.get_data("unassigned"))
        self.assertEqual('OK', response['status'])
        self.assertEqual(1, len(response['result']))
        
        result = response['result'][0]
        self.assertFalse(result['labels'])
        self.assertFalse(result['isGold'])
        self.assertEqual("testObject1", result['name'])
        
        expectedProbabilities = [('category1', 0.25), ('category2', 0.25), ('category3', 0.25), ('category4', 0.25)]
        categoryProbabilies = []
        for categoryProb in result['categoryProbability']:
            probTouple = (categoryProb['categoryName'], categoryProb['value'])
            categoryProbabilies.append(probTouple)
        
        for categoryProb in categoryProbabilies:
            self.assertTrue(categoryProb in expectedProbabilities)
    
    def test_AddGetUnassignedLabels_PrintableASCII_SpecialChars(self):
        client = TroiaClient(ADDRESS)
        categories = [
                      {"prior":"0.2", "name":"category1"}, 
                      {"prior":"0.3", "name":"category2"},
                      {"prior":"0.5", "name":"category3"}]
        response = client.create(categories)
        self.assertEqual('OK', response['status'])
             
        #post the unassigned label
        unassignedLabel = ["~!@#$%^&*()_+=-[]{}|:;<> ,./"]
        response = client.await_completion(client.post_data(unassignedLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
            
        #get the unassigned labels
        response = client.await_completion(client.get_data("unassigned"))
        self.assertEqual('OK', response['status'])
        self.assertEqual(1, len(response['result']))
        
        result = response['result'][0]
        self.assertFalse(result['labels'])
        self.assertFalse(result['isGold'])
        self.assertEqual(unassignedLabel[0], result['name'])
        
        expectedProbabilities = [('category1', 0.3333333333333333), ('category2', 0.3333333333333333), ('category3', 0.3333333333333333)]
        categoryProbabilies = []
        for categoryProb in result['categoryProbability']:
            probTouple = (categoryProb['categoryName'], categoryProb['value'])
            categoryProbabilies.append(probTouple)
        
        for categoryProb in categoryProbabilies:
            self.assertTrue(categoryProb in expectedProbabilities)
    
    def test_AddGetUnassignedLabels_ExtendedASCIIChars(self):
        client = TroiaClient(ADDRESS)
        categories = [{"prior":"0.2", "name":"category1"}, {"prior":"0.8", "name":"category2"}]
        response = client.create(categories)
        self.assertEqual('OK', response['status'])
             
        #post the unassigned label
        unassignedLabel = ["ëñµ¼Úæ"]
        response = client.await_completion(client.post_data(unassignedLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
            
        #get the unassigned labels
        response = client.await_completion(client.get_data("unassigned"))
        self.assertEqual('OK', response['status'])
        self.assertEqual(1, len(response['result']))
        
        result = response['result'][0]
        self.assertFalse(result['labels'])
        self.assertFalse(result['isGold'])
        self.assertEqual(unassignedLabel[0], result['name'])
        
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        categoryProbabilies = []
        for categoryProb in result['categoryProbability']:
            probTouple = (categoryProb['categoryName'], categoryProb['value'])
            categoryProbabilies.append(probTouple)
        
        for categoryProb in categoryProbabilies:
            self.assertTrue(categoryProb in expectedProbabilities)
            
    def test_AddGetUnassignedLabels_UnicodeChars(self):
        client = TroiaClient(ADDRESS)
        categories = [{"prior":"0.2", "name":"category1"}, {"prior":"0.8", "name":"category2"}]
        response = client.create(categories)
        self.assertEqual('OK', response['status'])
             
        #post the unassigned label
        unassignedLabel = ["ూഹܬआਖ਼"]
        response = client.await_completion(client.post_data(unassignedLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
            
        #get the unassigned labels
        response = client.await_completion(client.get_data("unassigned"))
        self.assertEqual('OK', response['status'])
        self.assertEqual(1, len(response['result']))
        
        result = response['result'][0]
        self.assertFalse(result['labels'])
        self.assertFalse(result['isGold'])
        self.assertEqual(unassignedLabel[0], result['name'])
        
        expectedProbabilities = [('category1', 0.5), ('category2', 0.5)]
        categoryProbabilies = []
        for categoryProb in result['categoryProbability']:
            probTouple = (categoryProb['categoryName'], categoryProb['value'])
            categoryProbabilies.append(probTouple)
        
        for categoryProb in categoryProbabilies:
            self.assertTrue(categoryProb in expectedProbabilities)



if __name__ == '__main__':
    unittest.main()