# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *

class TestAssignedLabels(unittest.TestCase):
    
        def test_AddGetEmptyAssignedLabels(self):
            client = TroiaClient(ADDRESS)
            response = client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the empty assigned labels
            response = client.await_completion(client.post_assigned_labels([]))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
           
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertFalse(result)
        
        def test_AddAssignedLabelsWithInvalidCategory(self):
            client = TroiaClient(ADDRESS)
            categories = [{"prior":0.3, "name":"category1"}, {"prior":0.7, "name":"category2"}]
            response = client.create(categories)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            assignedLabels = [('worker1', 'url1', 'category3')]
            response = client.await_completion(client.post_assigned_labels(assignedLabels))
            print response
            self.assertEqual('ERROR', response['status'])
            self.assertEqual('Internal error: attempting to add invalid category: category3', response['result'])
           
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertFalse(result)
            
        def test_AddGetAssignedLabels_PrintableASCII_RegularChars(self):
            client = TroiaClient(ADDRESS)
            response = client.create(CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(ASSIGNED_LABELS))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            
            results = []
            for receivedLabel in result:
                labelTouple = (receivedLabel['workerName'], receivedLabel['objectName'], receivedLabel['categoryName'])
                results.append(labelTouple)
            for label in ASSIGNED_LABELS:
                self.assertTrue(label in results)
            
            
        def test_AddGetAssignedLabels_PrintableASCII_SpecialChars(self):
            client = TroiaClient(ADDRESS)
            categories = [{"prior":0.4, "name":"category1"}, {"prior":0.239, "name":"category2"}, {"prior":0.361, "name":"category3"}]
            response = client.create(categories)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            assignedLabels = [
            ('a%a', '~!@#$%^&*()_+=-[]{}|:;<> ,./', 'category1'),
            ('b%%b', '%%%', 'category2'),
            ('c%%!<>c', '~!@#$^&*[](){}-_+=<>?/.,;:', 'category3')]
            
            response = client.await_completion(client.post_assigned_labels(assignedLabels))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
           
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(3, len(result))
         
            results = []
            for receivedLabel in result:
                labelTouple = (receivedLabel['workerName'], receivedLabel['objectName'], receivedLabel['categoryName'])
                results.append(labelTouple)
            for label in assignedLabels:
                self.assertTrue(label in results)
                
        def test_AddGetAssignedLabels_ExtendedASCIIChars(self):
            client = TroiaClient(ADDRESS)
            categories = [{"prior":0.4, "name":"category1"}, {"prior":0.239, "name":"category2"}, {"prior":0.361, "name":"category3"}]
            response = client.create(categories)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            assignedLabels = [
            ('®¶', 'œŒ', 'category1'),
            ('ÀÆË', '™ž¤©', 'category2'),
            ('ëñ', 'µ¼Úæ', 'category3')]
            
            response = client.await_completion(client.post_assigned_labels(assignedLabels))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
           
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(3, len(result))
         
            results = []
            for receivedLabel in result:
                labelTouple = (receivedLabel['workerName'], receivedLabel['objectName'], receivedLabel['categoryName'])
                results.append(labelTouple)
            for label in assignedLabels:
                self.assertTrue(label in results)
         
        def test_AddGetAssignedLabels_UnicodeChars(self):
            client = TroiaClient(ADDRESS)
            categories = [{"prior":0.4, "name":"category1"}, {"prior":0.239, "name":"category2"}, {"prior":0.361, "name":"category3"}]
            response = client.create(categories)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            assignedLabels = [
            ('ૉେஇ', 'ΨҖӖմ؂څ', 'category1'),
            ('ూഹ', 'ܬआਖ਼', 'category2')]
            
            response = client.await_completion(client.post_assigned_labels(assignedLabels))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
           
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            self.assertEqual(2, len(result))
         
            results = []
            for receivedLabel in result:
                labelTouple = (receivedLabel['workerName'], receivedLabel['objectName'], receivedLabel['categoryName'])
                results.append(labelTouple)
            for label in assignedLabels:
                self.assertTrue(label in results)             

if __name__ == '__main__':
    unittest.main()

