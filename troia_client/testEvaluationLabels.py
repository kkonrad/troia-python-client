# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *

class TestEvaluationLabels(unittest.TestCase):

    def test_AddGetEmptyEvaluationLabels(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
             
        #post the empty assigned labels
        response = client.await_completion(client.post_evaluation_data([]))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Evaluation datums added', response['result'])
           
        #get the evaluation labels and check that the list is empty 
        response = client.await_completion(client.get_evaluation_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertFalse(result)
        
        
    def test_AddGetEvaluationLabels_PrintableASCII_RegularChars(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
            
        response = client.await_completion(client.post_evaluation_data(EVALUATION_DATA))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Evaluation datums added', response['result'])
            
        #get the unassigned labels
        response = client.await_completion(client.get_evaluation_data())

        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(5, len(result))
           
        results = []  
        for evaluationLabel in response['result']:
            label = (evaluationLabel['objectName'], evaluationLabel['correctCategory'])
            results.append(label) 
                
        for evalLabel in EVALUATION_DATA:
            self.assertTrue(evalLabel in results)
                
    def test_AddGetEvaluationLabel_PrintableASCII_SpecialChars(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
        
        evaluationLabel = [('~!@%#$^&*()_+=-[]{}|:;<> ,./', 'notporn')]          
        response = client.await_completion(client.post_evaluation_data(evaluationLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Evaluation datums added', response['result'])
            
        #get the unassigned labels
        response = client.await_completion(client.get_evaluation_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        receivedLabel = (result[0]['objectName'], result[0]['correctCategory'])
        self.assertTrue(evaluationLabel[0] == receivedLabel)     
    
    def test_AddGetEvaluationLabel_ExtendedASCIIChars(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
        
        evaluationLabel = [('™ž¤©', 'notporn')]          
        response = client.await_completion(client.post_evaluation_data(evaluationLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Evaluation datums added', response['result'])
            
        #get the unassigned labels
        response = client.await_completion(client.get_evaluation_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        receivedLabel = (result[0]['objectName'], result[0]['correctCategory'])
        self.assertTrue(evaluationLabel[0] == receivedLabel)    
    
    def test_AddGetEvaluationLabel_UnicodeChars(self):
        client = TroiaClient(ADDRESS)
        response = client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])
        
        evaluationLabel = [('ૉେஇ', 'notporn')]          
        response = client.await_completion(client.post_evaluation_data(evaluationLabel))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Evaluation datums added', response['result'])
            
        #get the unassigned labels
        response = client.await_completion(client.get_evaluation_data())
        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(1, len(result))
        receivedLabel = (result[0]['objectName'], result[0]['correctCategory'])
        self.assertTrue(evaluationLabel[0] == receivedLabel)     
      



if __name__ == '__main__':
    unittest.main()