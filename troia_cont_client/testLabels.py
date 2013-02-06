import unittest
from contClient import TroiaContClient
from testSettings import TestSettings

class TestLabels(unittest.TestCase):

    def setUp(self):
        self.client = TroiaContClient(TestSettings.ADDRESS)
        response = self.client.createNewJob()
        self.assertEqual('OK', response['status'])
        
    def load_assigns(self):
        #post the assigned labels
        for worker, obj, label in TestSettings.ASSIGNED_LABELS_CONT:
            response = self.client.await_completion(self.client.post_assigned_label(worker, obj, float(label)), 0.5)
            self.assertEqual('OK', response['status'])
            self.assertEqual('Assigns added', response['result'])
            
    def test_AddGetAssignedLabels(self):
        self.load_assigns()
        #get the assigned labels
        response = self.client.await_completion(self.client.get_assigned_labels())
        self.assertEqual('OK', response['status'])
        result = response['result']
        assignedLabels = str(result).replace('u\'', '\'')
        
        keys = ["worker", "object", "label"]
        for initialLabel in TestSettings.ASSIGNED_LABELS_CONT:
            dictionary = dict(zip(keys, initialLabel))
            self.assertTrue(str(dictionary) in assignedLabels)
            
    def test_AddGetGoldLabels(self):
        #post the assigned labels
        response = self.client.await_completion(self.client.post_gold_data(TestSettings.GOLD_LABELS_CONT))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Correct data added', response['result'])
        
        #get the assigned labels
        response = self.client.await_completion(self.client.get_gold_data()())
        self.assertEqual('OK', response['status'])

    def test_AddGetObjects(self):
        #add an object
        response = self.client.await_completion(self.client.post_objects(["object1"]))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
        
        #get all the objects
        response = self.client.await_completion(self.client.get_data())
        self.assertEqual('OK', response['status'])
        
    def test_GetObjectData(self):
        #add objects
        objects = ["object2", "object3"]
        response = self.client.await_completion(self.client.post_objects([objects]))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
        
        #get the data for the given object
        response = self.client.await_completion(self.client.get_object_data(objects[0]))
        self.assertEqual('OK', response['status'])
        
    def test_GetObjectAssigns(self):
        #add objects
        objects = ["object2", "object3"]
        response = self.client.await_completion(self.client.post_objects([objects]))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
        
        #get the assigned labels for the given object
        response = self.client.await_completion(self.client.get_object_assigns(objects[0]))
        self.assertEqual('OK', response['status'])

