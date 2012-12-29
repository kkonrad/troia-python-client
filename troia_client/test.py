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


class TestJobManipulation(TroiaClientTestBase):

    JOB_ID = "TESTING_JOB_MANIUPULATION"

    def setUp(self):
        super(TestJobManipulation, self).setUp()

    def test_creation(self):
        w = self.tc.info()
        self.assertEqual('ERROR', w['status'])
        w = self.tc.create()
        self.assertEqual('OK', w['status'])
        w = self.tc.info()
        self.assertEqual('OK', w['status'])

    def test_deletion(self):
        w = self.tc.info()
        self.assertEqual('ERROR', w['status'])
        w = self.tc.create()
        self.assertEqual('OK', w['status'])
        w = self.tc.info()
        self.assertEqual('OK', w['status'])
        w = self.tc.delete()
        self.assertEqual('OK', w['status'])
        w = self.tc.info()
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
        w = self.tc.create()
        self.assertEqual('OK', w['status'])

    def test_categories_load(self):
        tc = self.tc
        w = tc.await_completion(tc.post_categories_def_prior(COST_MATRIX))
        self.assertEqual('OK', w['status'])
        self.assertTrue('add' in w['result'].lower())
        self.assertTrue('categor' in w['result'].lower())

        w = tc.await_completion(tc.get_categories())
        self.assertEqual('OK', w['status'])
        self.assertEqual(set(('porn', 'notporn')), set(w['result']))


if __name__ == '__main__':
    unittest.main()
