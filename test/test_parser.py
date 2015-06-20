__author__ = 'rwardrup'

import unittest
from wilks import parse_results


class ParserTest(unittest.TestCase):
    """
    Test Powerlifting results CSV parser
    """
    def testType(self):
        """
        Make sure parser returns a dict
        :return:
        """
        path = '../data/openpowerlifting.csv'
        self.assertEqual(type(parse_results(path)), dict)


if __name__ == '__main__':
    unittest.main()