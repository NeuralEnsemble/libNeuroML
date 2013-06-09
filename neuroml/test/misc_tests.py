"""
Miscelaneous unit tests

"""

import sys
import inspect

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
        
        for name,test_class in inspect.getmembers(sys.modules[neuroml.__name__]):
            if inspect.isclass(test_class):
                ob = test_class()
                self.assertIsInstance(ob,test_class)
