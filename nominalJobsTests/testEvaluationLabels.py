# -*- coding: utf-8 -*-
import unittest
from client.gal import TroiaClient
from testSettings import *


class TestEvaluationLabels(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        response = self.client.create(CATEGORIES)
        self.assertEqual('OK', response['status'])

    def tearDown(self):
        self.client.delete()

    def _test_method(self, eval_data):
        response = self.client.await_completion(self.client.post_evaluation_objects(eval_data))
        self.assertEqual('OK', response['status'])

        #get the unassigned labels
        response = self.client.await_completion(self.client.get_evaluation_objects())

        self.assertEqual('OK', response['status'])
        result = response['result']
        self.assertEqual(len(eval_data), len(result))

        results = [(evaluationLabel['name'], evaluationLabel['evaluationLabel']) for evaluationLabel in response['result']]

        for evalLabel in eval_data:
            self.assertTrue(evalLabel in results)

    def test_AddGetEmptyEvaluationLabels(self):
        self._test_method([])

    def test_AddGetEvaluationLabels_PrintableASCII_RegularChars(self):
        self._test_method(EVALUATION_DATA)

    def test_AddGetEvaluationLabel_PrintableASCII_SpecialChars(self):
        self._test_method([('~!@%#$^&*()_+=-[]{}|:;<> ,./', 'notporn')])

    def test_AddGetEvaluationLabel_ExtendedASCIIChars(self):
        self._test_method([(u'™ž¤©', 'notporn')])

    def test_AddGetEvaluationLabel_UnicodeChars(self):
        self._test_method([(u'ૉେஇ', 'notporn')])

    def test_AddGetEvaluationLabel_LongLabelNames(self):
        response = self.client.await_completion(self.client.post_evaluation_objects([('sdgfdgfgfhdsjgfhgfhgfhhjhgjhjjghghkgkhjkfklsdjfkljssdgfdgfgfhdsjgfhgfhgfhhjhgjhjjghghkgkhjkfklsdjfkljs', 'notporn')]))
        self.assertEqual('ERROR', response['status'])
        self.assertEqual('Internal error: Object name should be shorter than 100 chars', response['result'])


if __name__ == '__main__':
    unittest.main()
