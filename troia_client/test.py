import unittest

from client import TroiaClient
from testSettings import ADDRESS, CATEGORIES, GOLD_SAMPLES, ASSIGNED_LABELS

class TroiaClientTestBase(unittest.TestCase):

    def setUp(self):
        self.tc = TroiaClient(ADDRESS)

    def tearDown(self):
        self.tc.delete()

    def assert_fail_with_code(self, fun, expected_code):
        try:
            fun()
            self.fail('Expected error with status_code ' + expected_code)
        except Exception as ex:
            self.assertEqual(expected_code, ex.args[0])
            return ex.args[1]

class TestUseCases(TroiaClientTestBase):

    JOB_ID = "TESTING_USE_cases"

    def setUp(self):
        super(TestUseCases, self).setUp()
        w = self.tc.create(CATEGORIES)
        self.assertEqual('OK', w['status'])

    def test_tutorial(self):
        w = self.tc.await_completion(
            self.tc.post_assigned_labels(ASSIGNED_LABELS))
        self.assertEqual('OK', w['status'])
        w = self.tc.await_completion(
            self.tc.post_gold_data(GOLD_SAMPLES))
        self.assertEqual('OK', w['status'])

        w = self.tc.await_completion(
            self.tc.post_compute())
        self.assertEqual('OK', w['status'])

        w = self.tc.await_completion(
            self.tc.get_prediction_workers_quality())
        self.assertEqual('OK', w['status'])
        res = w['result']
        for worker in set((x[0] for x in ASSIGNED_LABELS)):
            self.assertEqual(1, len([x for x in res if x['workerName'] == worker]))

        #for el in res:
         #   self.assertEqual(5, el['Number of Annotations'])

        w = self.tc.await_completion(
            self.tc.get_predictions_objects("DS", "MaxLikelihood"))
        self.assertEqual('OK', w['status'])
        print w['result']
        expectedCategories =(
            ('url1', 'notporn'),
            ('url2', 'porn'),
            ('url3', 'notporn'),
            ('url4', 'porn'),
            ('url5', 'notporn')
        )
        for r in w['result']:
            self.assertTrue((r['objectName'], r['categoryName']) in expectedCategories)
      


if __name__ == '__main__':
    unittest.main()
