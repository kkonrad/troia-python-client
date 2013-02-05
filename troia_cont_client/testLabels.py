import unittest
from contClient import TroiaContClient
from testSettings import TestSettings

class TestLabels(unittest.TestCase):

        def test_AddGetAssignedLabels(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_assigned_labels(TestSettings.ASSIGNED_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            assignedLabels = str(result).replace('u\'', '\'')
            
            keys = ["worker", "object", "label"]
            for initialLabel in TestSettings.ASSIGNED_LABELS_CONT:
                dictionary = dict(zip(keys, initialLabel))
                self.assertTrue(str(dictionary) in assignedLabels)
                
            
        def test_AddGetGoldLabels(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #post the assigned labels
            response = client.await_completion(client.post_gold_data(TestSettings.GOLD_LABELS_CONT))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Correct data added', response['result'])
            
            #get the assigned labels
            response = client.await_completion(client.get_assigned_labels())
            self.assertEqual('OK', response['status'])
            result = response['result']
            assignedLabels = str(result).replace('u\'', '\'')
            
            keys = ["worker", "object", "label"]
            for initialLabel in TestSettings.ASSIGNED_LABELS_CONT:
                dictionary = dict(zip(keys, initialLabel))
                self.assertTrue(str(dictionary) in assignedLabels)
                
        def test_AddGetObjects(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #add an object
            response = client.await_completion(client.post_objects(["object1"]))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Object without labels added', response['result'])
            
            #get all the objects
            response = client.await_completion(client.get_data())
            self.assertEqual('OK', response['status'])
            self.assertEqual(1, len(response['result']))
            result = dict(response['result'][0])
                  
            self.assertFalse(result['isGold'])
            self.assertEqual("testObject1", result['name'])
            
        def test_GetObjectData(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #add objects
            objects = ["object2", "object3"]
            response = client.await_completion(client.post_objects([objects]))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Object without labels added', response['result'])
            
            #get the data for the given object
            response = client.await_completion(client.get_object_data(objects[0]))
            self.assertEqual('OK', response['status'])
            self.assertEqual(1, len(response['result']))
            result = dict(response['result'][0])
            
        def test_GetObjectAssigns(self):
            client = TroiaContClient(TestSettings.ADDRESS)
            response = client.createNewJob()
            self.assertEqual('OK', response['status'])
             
            #add objects
            objects = ["object2", "object3"]
            response = client.await_completion(client.post_objects([objects]))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Object without labels added', response['result'])
            
            #get the assigned labels for the given object
            response = client.await_completion(client.get_object_assigns(objects[0]))
            self.assertEqual('OK', response['status'])
            self.assertEqual(1, len(response['result']))
            result = dict(response['result'][0])

        
            
                
        