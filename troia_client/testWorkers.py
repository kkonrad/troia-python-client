# -*- coding: utf-8 -*-
import unittest
from client import TroiaClient
from testSettings import *


class TestWorkers(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()
