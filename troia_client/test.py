import unittest

from client import TroiaClient


ADRESS = 'http://localhost:8080/troia-server-0.0.1'


class TroiaClientTestBase(unittest.TestCase):

    def setUp(self):
        self.tc = TroiaClient(ADRESS, self.JOB_ID)


class TestJobManipulation(TroiaClientTestBase):

    JOB_ID = "TESTING_JOB_MANIUPULATION"

    def setUp(self):
        super(TestJobManipulation, self).setUp()
        self.tc.delete()

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
        self.assertTrue('OK', w['status'])

    def test_pingDB(self):
        w = self.tc.pingDB()
        self.assertTrue('OK', w['status'])


if __name__ == '__main__':
    unittest.main()
