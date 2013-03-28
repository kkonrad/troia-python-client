# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *


class TestCategories(unittest.TestCase):

        def setUp(self):
            self.client = TroiaClient(ADDRESS)

        def tearDown(self):
            self.client.delete()

        def _test_method(self, categories):
            response = self.client.create(categories)
            self.assertEqual('OK', response['status'])

            response = self.client.await_completion(self.client.get_categories())
            self.assertEqual('OK', response['status'])
            for category in categories:
                self.assertTrue(category in response['result'])

        def test_AddGetCategories_PrintableASCII_SpecialChars(self):
            categories = [u'!@#$:;,.{}[]', u'2ndCategory']
            self._test_method(categories)

        def test_AddGetCategories_ExtendedASCIIChars(self):
            categories = [u'œŒ', u'ÀÆË™ž¤©']
            self._test_method(categories)

        def test_AddGetCategories_UnicodeChars(self):
            categories = [u'ૉେஇΨҖӖմ؂څ', u'ూഹܬआਖ਼']
            self._test_method(categories)
