import unittest
from client import TroiaClient
from testSettings import TestSettings
import random
import string

class TestLabels(unittest.TestCase):
    
        def generateId(self, length):
            return "".join([random.choice(string.ascii_lowercase) for x in xrange(length)])
        
        def test_AddGetAssignedLabels(self):
            jobId = self.generateId(10).join('job')
            client = TroiaClient(TestSettings.ADDRESS, jobId)
            response = client.createNewJob(TestSettings.CATEGORIES)
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.post_assigned_labels(TestSettings.ASSIGNED_LABELS)
            self.assertEqual('OK', response['status'])
            command_id = response['redirect']
            
            #check the command status
            response = client.get_status(command_id)
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #get the assigned labels
            response = client.get_assigned_labels()
            command_id = response['redirect']
            
            #check the command status
            response = client.get_status(command_id)
            self.assertEqual('OK', response['status'])
            result = response['result']
            assignedLabels = str(result).replace('u\'', '\'')
            
            keys = ["workerName", "objectName", "categoryName"]
            for initialLabel in TestSettings.ASSIGNED_LABELS:
                dictionary = dict(zip(keys, initialLabel))
                self.assertTrue(str(dictionary) in assignedLabels)
