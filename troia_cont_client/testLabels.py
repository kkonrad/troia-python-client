import unittest
from contClient import TroiaContClient
from testSettings import *


class TestLabels(unittest.TestCase):

    def setUp(self):
        self.client = TroiaContClient(ADDRESS)
        response = self.client.createNewJob()
        self.assertEqual('OK', response['status'])

    def tearDown(self):
        self.client.delete()

    def load_assigns(self):
        #post the assigned labels
        response = self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS_CONT))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Assigns added', response['result'])

    def test_AddGetAssignedLabels(self):
        self.load_assigns()

        #get the assigned labels
        response = self.client.await_completion(self.client.get_assigned_labels())
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(ASSIGNED_LABELS_CONT), len(response['result']))
        for al in response['result']:
            self.assertTrue(al['worker'] in [w for w, _, _ in ASSIGNED_LABELS_CONT])

    def test_AddGetGoldLabels(self):
        #post the gold labels
        response = self.client.await_completion(self.client.post_gold_data(GOLD_LABELS_CONT))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Gold objects added', response['result'])

        #get the gold labels
        response = self.client.await_completion(self.client.get_gold_data())
        self.assertEqual('OK', response['status'])
        self.assertEqual(len(GOLD_LABELS_CONT), len(response['result']))

        result = response['result']
        self.assertEqual(len(GOLD_LABELS_CONT), len(result))
        goldLabelsList = []
        for receivedGoldLabel in response['result']:
            labelName = receivedGoldLabel['name']
            goldLabelData = (labelName, receivedGoldLabel['goldLabel']['value'], receivedGoldLabel['goldLabel']['zeta'])
            goldLabelsList.append(goldLabelData)
        for label in GOLD_LABELS_CONT:
            self.assertTrue(label in goldLabelsList)

    def test_AddGetObject(self):
        #add an object
        response = self.client.await_completion(self.client.post_objects(["object1"]))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Objects without labels added', response['result'])

        #get all the objects
        response = self.client.await_completion(self.client.get_objects())
        self.assertEqual('OK', response['status'])
        self.assertEqual(1, len(response['result']))
        self.assertEqual('object1', response['result'][0]['name'])

    def test_AddGetObjects(self):
        #add multiple object
        objects = ["object1", "object2", "object3"]
        response = self.client.await_completion(self.client.post_objects(objects))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Objects without labels added', response['result'])

        #get all the objects
        response = self.client.await_completion(self.client.get_objects())
        self.assertEqual('OK', response['status'])
        self.assertEqual(3, len(response['result']))
        for obj in response['result']:
            self.assertTrue(obj['name'] in objects)

    def test_GetObjectData(self):
        #add objects
        objects = ["object2", "object3"]
        response = self.client.await_completion(self.client.post_objects(objects))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Objects without labels added', response['result'])

        #get the data for the given object
        for obj in objects:
            response = self.client.await_completion(self.client.get_object(obj))
            self.assertEqual('OK', response['status'])
            self.assertEqual(obj, response['result']['name'])

    def test_GetObjectAssigns(self):
        #add objects
        objects = ["object2", "object3"]
        response = self.client.await_completion(self.client.post_objects(objects))
        self.assertEqual('OK', response['status'])
        self.assertEqual('Objects without labels added', response['result'])

        #get the assigned labels for the given object
        for obj in objects:
            response = self.client.await_completion(self.client.get_object_assigns(obj))
            self.assertEqual('OK', response['status'])
            for al in response['result']:
                self.assertEqual(obj, al['object'])
