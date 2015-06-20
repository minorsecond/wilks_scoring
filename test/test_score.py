__author__ = 'rwardrup'

import unittest
from wilks import wilkscore

class TestScores(unittest.TestCase):
    def test_score(self):
        """
        Test output of Wilk's score
        :return:
        """
        total = 900
        result = 287.72
        self.assertEqual(wilkscore(total, 0.3196888888888889), result)


if __name__ == '__main__':
    unittest.main()
