import unittest

from client import TroiaClient


ADRESS = 'http://localhost:8080/troia-server-0.0.1'


ITERATIONS = 5

# porn/not-porn data in Python data structures

COST_MATRIX = [
    ('porn', {
        'porn':     0.,
        'notporn':  1.,
    }),
    ('notporn', {
        'notporn':  0.,
        'porn':     1.,
    }),
]

GOLD_SAMPLES = [
    ('url1', 'notporn'),
    ('url2', 'porn'),
]


WORKERS_LABELS = [
    ('worker1', 'url1', 'porn'),
    ('worker1', 'url2', 'porn'),
    ('worker1', 'url3', 'porn'),
    ('worker1', 'url4', 'porn'),
    ('worker1', 'url5', 'porn'),
    ('worker2', 'url1', 'notporn'),
    ('worker2', 'url2', 'porn'),
    ('worker2', 'url3', 'notporn'),
    ('worker2', 'url4', 'porn'),
    ('worker2', 'url5', 'porn'),
    ('worker3', 'url1', 'notporn'),
    ('worker3', 'url2', 'porn'),
    ('worker3', 'url3', 'notporn'),
    ('worker3', 'url4', 'porn'),
    ('worker3', 'url5', 'notporn'),
    ('worker4', 'url1', 'notporn'),
    ('worker4', 'url2', 'porn'),
    ('worker4', 'url3', 'notporn'),
    ('worker4', 'url4', 'porn'),
    ('worker4', 'url5', 'notporn'),
    ('worker5', 'url1', 'porn'),
    ('worker5', 'url2', 'notporn'),
    ('worker5', 'url3', 'porn'),
    ('worker5', 'url4', 'notporn'),
    ('worker5', 'url5', 'porn'),
]


class TroiaClientTestBase(unittest.TestCase):

    def setUp(self):
        self.tc = TroiaClient(ADRESS, self.JOB_ID)
        self.tc.delete()

    def assert_fail_with_code(self, fun, expected_code):
        try:
            fun()
            self.fail('Expected error with status_code ' + expected_code)
        except Exception as ex:
            self.assertEqual(expected_code, ex.args[0])
            return ex.args[1]


class TestJobManipulation(TroiaClientTestBase):

    JOB_ID = "TESTING_JOB_MANIUPULATION"

    def setUp(self):
        super(TestJobManipulation, self).setUp()

    def test_job_creation(self):
        w = self.assert_fail_with_code(self.tc.info, 400)
        self.assertEqual('ERROR', w['status'])
        w = self.tc.create(COST_MATRIX)
        self.assertEqual('OK', w['status'])
        w = self.tc.info()
        self.assertEqual('OK', w['status'])

    def test_job_deletion(self):
        w = self.assert_fail_with_code(self.tc.info, 400)
        self.assertEqual('ERROR', w['status'])
        w = self.tc.create(COST_MATRIX)
        self.assertEqual('OK', w['status'])
        w = self.tc.info()
        self.assertEqual('OK', w['status'])
        w = self.tc.delete()
        self.assertEqual('OK', w['status'])
        w = self.assert_fail_with_code(self.tc.info, 400)
        self.assertEqual('ERROR', w['status'])


class TestStatus(TroiaClientTestBase):

    JOB_ID = "TESTING_OVERAL_STATUSES"

    def setUp(self):
        super(TestStatus, self).setUp()

    def test_ping(self):
        w = self.tc.ping()
        self.assertEqual('OK', w['status'])

    def test_pingDB(self):
        w = self.tc.pingDB()
        self.assertEqual('OK', w['status'])


class TestJobDataFilling(TroiaClientTestBase):

    JOB_ID = "TESTING_JOB_DATA_FILLING"

    def setUp(self):
        super(TestJobDataFilling, self).setUp()
        w = self.tc.create(COST_MATRIX)
        self.assertEqual('OK', w['status'])

    def data_init_upload_test(self, after_upload, exp_str, get_fun):
        w = self.tc.await_completion(after_upload)
        self.assertEqual('OK', w['status'])
        self.assertEqual(exp_str, w['result'])

        w = self.tc.await_completion(get_fun())
        self.assertEqual('OK', w['status'])
        return w

    def test_get_categories_load(self):
        w = self.tc.await_completion(self.tc.get_categories())
        self.assertEqual(set(('porn', 'notporn')), set(w['result']))

    def test_golds_load(self):
        w = self.data_init_upload_test(
            self.tc.post_gold_data(GOLD_SAMPLES),
            'Correct data added', self.tc.get_gold_data)
        expected = [
                {u'correctCategory': u'notporn', u'objectName': u'url1'},
                {u'correctCategory': u'porn', u'objectName': u'url2'}
            ]
        res = w['result']
        self.assertTrue(expected[0] == res[0] or expected[0] == res[1])
        self.assertTrue(expected[1] == res[0] or expected[1] == res[1])
        self.assertTrue(res[0] != res[1])


if __name__ == '__main__':
    unittest.main()
