__author__ = 'rwardrup'

import unittest
from wilks import *


class MyTestCase(unittest.TestCase):
    def test_coef(self):
        """
        Test output of Wilk's coefficient formula for myself
        :return:
        """
        weight = 168
        result = 0.3196888888888889

        self.assertEqual(coef('male', weight), result)

if __name__ == '__main__':
    unittest.main()
