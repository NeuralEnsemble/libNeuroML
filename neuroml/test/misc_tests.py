"""
Miscelaneous unit tests

"""

import inspect
import sys

import neuroml

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestCommonProperties(unittest.TestCase):
    def test_instatiation(self):
        """
        Since classes are auto-generated, need to test that they correctly instantiate
        """

        for name, test_class in inspect.getmembers(sys.modules[neuroml.__name__]):
            if sys.version_info >= (2, 7):
                print(sys.version_info)
                if inspect.isclass(test_class):
                    ob = test_class()
                    self.assertIsInstance(ob, test_class)
            else:
                print("Warning - Python<2.7 does not support this test")
                pass
