"""
Unit tests for writers

"""

import neuroml
from neuroml import writers
import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLLoader(unittest.TestCase):

    def test_write_nonsense(self):
        """
        Should Throw an attribute error as integers do not have an export method
        """

        a = 6 #not NeuroML-writeable
        writer_method = neuroml.writers.NeuroMLWriter.write
        self.assertRaises(AttributeError, writer_method, a, "tmpfile")
