import unittest
from client.galc import TroiaContClient
from testSettings import *


class TestLabels(unittest.TestCase):

    def setUp(self):
        self.client = TroiaContClient(ADDRESS)
        response = self.client.create()
        self.assertEqual('OK', response['status'])

    def tearDown(self):
        self.client.delete()

    def load_assigns(self):
        #post the assigned labels
        response = self.client.await_completion(self.client.post_assigned_labels(ASSIGNED_LABELS_CONT))
        self.assertEqual('OK', response['status'])

    def test_getJobStatus(self):
        response = self.client.get_job_status()
        self.assertEqual('OK', response['status'])
        response = self.client.get_status(response['redirect'])
        self.assertEqual('OK', response['status'])
        self.assertEqual(0, response['result']['Number of assigns'])
        self.assertEqual(0, response['result']['Number of gold objects'])
        self.assertEqual(0, response['result']['Number of objects'])
        self.assertEqual(0, response['result']['Number of workers'])

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

    def test_AddGetGoldLabel(self):
        #post the gold labels
        response = self.client.await_completion(self.client.post_gold_data(GOLD_LABELS_CONT))
        self.assertEqual('OK', response['status'])

        #get the gold labels
        response = self.client.await_completion(self.client.get_gold_object("url1"))
        self.assertTrue('OK', response['status'])
        self.assertTrue(1, len(response['result']))
        self.assertTrue('url1', response['result']['name'])
        self.assertTrue('0.292643407722905', response['result']['goldLabel']['zeta'])
        self.assertTrue('10.219077484951955', response['result']['goldLabel']['value'])

    def test_AddGetObject(self):
        #add an object
        response = self.client.await_completion(self.client.post_objects(["object1"]))
        self.assertEqual('OK', response['status'])

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

        #get all the objects
        response = self.client.await_completion(self.client.get_objects())
        self.assertEqual('OK', response['status'])
        self.assertEqual(3, len(response['result']))
        for obj in response['result']:
            self.assertTrue(obj['name'] in objects)

    def test_GetObjectInfo(self):
        #add objects
        objects = ["object2", "object3"]
        response = self.client.await_completion(self.client.post_objects(objects))
        self.assertEqual('OK', response['status'])

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

        #get the assigned labels for the given object
        for obj in objects:
            response = self.client.await_completion(self.client.get_object_assigns(obj))
            self.assertEqual('OK', response['status'])
            for al in response['result']:
                self.assertEqual(obj, al['object'])

