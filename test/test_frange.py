__author__ = 'rwardrup'

import unittest
from wilks import frange

class FrangeTest(unittest.TestCase):
    def test_frange(self):
        self.assertEqual(frange(62, 79), True)

if __name__ == '__main__':
    unittest.main()
