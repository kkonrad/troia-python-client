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
    '''
    def test_AddGetAssignedLabels(self):
        self.load_assigns()
        #get the assigned labels
        response = self.client.await_completion(self.client.get_assigned_labels())
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(TestSettings.ASSIGNED_LABELS_CONT), len(response['result']))
        print response['result']
        for al in response['result']:
            self.assertTrue(al['worker'] in [w for w, _, _ in TestSettings.ASSIGNED_LABELS_CONT])
    '''        
    def test_AddGetGoldLabels(self):
        #post the assigned labels
        for obj, label, zeta in TestSettings.GOLD_LABELS_CONT:
            response = self.client.await_completion(self.client.post_gold_datum(obj, label, zeta))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Gold object added', response['result'])
        
        #get the assigned labels
        response = self.client.await_completion(self.client.get_gold_data())
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(TestSettings.GOLD_LABELS_CONT), len(response['result']))
        
        goldLabelsList=[]
        for receivedGoldLabel in response['result']:
            labelName = str(receivedGoldLabel['name']).replace('u\'', '\'')
            goldLabelData = (labelName, receivedGoldLabel['goldLabel']['value']['value'], receivedGoldLabel['goldLabel']['value']['zeta'])
            goldLabelsList.append(goldLabelData)
        for label in TestSettings.GOLD_LABELS_CONT:
            self.assertTrue(label in goldLabelsList)
                    
    '''
    def test_AddGetObjects(self):
        #add an object
        response = self.client.await_completion(self.client.post_object("object1"))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Object without labels added', response['result'])
        
        #get all the objects
        response = self.client.await_completion(self.client.get_objects())
        self.assertEqual('OK', response['status'])
        self.assertEqual(1, len(response['result']))
        self.assertEqual('object1', response['result'][0]['name'])
        
    def test_GetObjectData(self):
        #add objects
        objects = ["object2", "object3"]
        for obj in objects: 
            response = self.client.await_completion(self.client.post_object(obj))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Object without labels added', response['result'])
        
        #get the data for the given object
        for obj in objects: 
            response = self.client.await_completion(self.client.get_object(obj))
            self.assertEqual('OK', response['status'])
            self.assertEqual(obj, response['result']['name'])
        
    def test_GetObjectAssigns(self):
        #add objects
        objects = ["object2", "object3"]
        for obj in objects:
            response = self.client.await_completion(self.client.post_object(obj))
            self.assertEqual('OK', response['status'])
            self.assertEqual('Object without labels added', response['result'])
        
        #get the assigned labels for the given object
        for obj in objects:
            response = self.client.await_completion(self.client.get_object_assigns(obj))
            self.assertEqual('OK', response['status'])
            for al in response['result']:
                self.assertEqual(obj, al['object'])

    '''