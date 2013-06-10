"""
Unit tests for loaders

"""

import neuroml
from neuroml import loaders
import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLLoader(unittest.TestCase):
    def test_load_neuroml(self):
        root_dir = os.path.dirname(neuroml.__file__)
        test_file_path = os.path.join(root_dir,'test')
        test_file_path = os.path.join(test_file_path,'Purk2M9s.nml')
        f = open(test_file_path,'r')
        doc = loaders.NeuroMLLoader.load(test_file_path)
        self.assertEqual(doc.id,'Purk2M9s')
