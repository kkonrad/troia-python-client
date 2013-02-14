# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *

class TestCategories(unittest.TestCase):
    
        def setUp(self):
            self.client = TroiaClient(ADDRESS)
            
        def tearDown(self):
            self.client.delete()
    
        def test_AddGetCategories_PrintableASCII_RegularChars(self):
            categories = [{"prior":0.123, "name":"category1"}, {"prior":0.456, "name":"category2"}, {"prior":0.421, "name":"category3"}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            
            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])
            
            expectedCategories = ['category1', 'category2', 'category3']
            for category in expectedCategories:
                self.assertTrue(category in response['result'])
    
        def test_AddGetCategories_PrintableASCII_SpecialChars(self):
            categories = [{"prior":0.5, "name":"!@#$:;,.{}[]"}, {"prior":0.5, "name":"2ndCategory"}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            
            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])
            expectedCategories = [u'!@#$:;,.{}[]', u'2ndCategory']
            for category in expectedCategories:
                self.assertTrue(category in response['result'])    
                
        def test_AddGetCategories_ExtendedASCIIChars(self):
            categories = [{"prior":0.5, "name":"œŒ"}, {"prior":0.5, "name":"ÀÆË™ž¤©"}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            
            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])
            
            expectedCategories = [u'œŒ', u'ÀÆË™ž¤©']
            for category in expectedCategories:
                self.assertTrue(category in response['result'])    
                
                
        def test_AddGetCategories_UnicodeChars(self):
            categories = [{"prior":0.5, "name":"ૉେஇΨҖӖմ؂څ"}, {"prior":0.5, "name":"ూഹܬआਖ਼"}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            
            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])
            
            expectedCategories = [u'ૉେஇΨҖӖմ؂څ', u'ూഹܬआਖ਼']
            for category in expectedCategories:
                self.assertTrue(category in response['result'])                
             
        def test_CostMatrix_01Values(self):
            categories = [{"name":"porn", "prior":0.3, "misclassificationCost": [{'categoryName': 'porn', 'value': 0.0}, {'categoryName': 'notporn', 'value': 1.0}]}, 
                          {"name":"notporn", "prior":0.7, "misclassificationCost":[{'categoryName': 'porn', 'value': 1.0}, {'categoryName': 'notporn', 'value': 0.0}]}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + self.client.jid, response['result'])
            
            response = self.client.await_completion(self.client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            self.assertEqual(len(categories), len(response['result']))
            expectedCategories = [{u'prior': 0.3, u'misclassificationCost': [{u'categoryName': u'porn', u'value': 0.0}, {u'categoryName': u'notporn', u'value': 1.0}], u'name': u'porn'}, 
                                  {u'prior': 0.7, u'misclassificationCost': [{u'categoryName': u'porn', u'value': 1.0}, {u'categoryName': u'notporn', u'value': 0.0}], u'name': u'notporn'}]
            for result in response['result']:  
                self.assertTrue(result in expectedCategories)

        def test_CostMatrix_DoubleValues(self):
            categories = [{"name":"porn", "prior":0.3, "misclassificationCost": [{'categoryName': 'porn', 'value': 0.4}, {'categoryName': 'notporn', 'value': 0.6}]}, 
                          {"name":"notporn", "prior":0.7, "misclassificationCost":[{'categoryName': 'porn', 'value': 0.6}, {'categoryName': 'notporn', 'value': 0.4}]}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + self.client.jid, response['result'])
            
            response = self.client.await_completion(self.client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            self.assertEqual(len(categories), len(response['result']))
            expectedCategories = [{u'prior': 0.3, u'misclassificationCost': [{u'categoryName': u'porn', u'value': 0.4}, {u'categoryName': u'notporn', u'value': 0.6}], u'name': u'porn'}, 
                                  {u'prior': 0.7, u'misclassificationCost': [{u'categoryName': u'porn', u'value': 0.6}, {u'categoryName': u'notporn', u'value': 0.4}], u'name': u'notporn'}]
            for result in response['result']:  
                self.assertTrue(result in expectedCategories)
                
        def test_UpdateCostMatrix(self):
            #create a job with some default categories
            categories = [{"name":"porn", "prior":0.5, "misclassificationCost": [{'categoryName': 'porn', 'value': 0.0}, {'categoryName': 'notporn', 'value': 1.0}]}, 
                          {"name":"notporn", "prior":0.5, "misclassificationCost":[{'categoryName': 'porn', 'value': 1.0}, {'categoryName': 'notporn', 'value': 0.0}]}]
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])
            self.assertEqual('New job created with ID: ' + self.client.jid, response['result'])
            
            #update the cost matrix
            newCostMatrix = [{"categoryTo":"porn", "cost":0.3, "categoryFrom":"porn"}, {"categoryTo":"porn", "cost":1.7, "categoryFrom":"notporn"}, {"categoryTo":"notporn", "cost":1.7, "categoryFrom":"porn"}, {"categoryTo":"notporn", "cost":0.3, "categoryFrom":"notporn"}]
            
            response = self.client.await_completion(self.client.post_cost_matrix(newCostMatrix))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Costs set', response['result'])
            
            #retrieve the cost matrix and check that it is updated correctly
            response = self.client.await_completion(self.client.get_cost_matrix())
            self.assertEqual('OK', response['status'])
            result = response['result']
            expectedCategories = [{u'prior': 0.5, u'misclassificationCost': [{u'categoryName': u'porn', u'value': 0.3}, {u'categoryName': u'notporn', u'value': 1.7}], u'name': u'porn'}, 
                                  {u'prior': 0.5, u'misclassificationCost': [{u'categoryName': u'porn', u'value': 1.7}, {u'categoryName': u'notporn', u'value': 0.3}], u'name': u'notporn'}]
            for result in response['result']:  
                self.assertTrue(result in expectedCategories)
            
            
            