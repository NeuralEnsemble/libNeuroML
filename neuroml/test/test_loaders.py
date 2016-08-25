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
        print('root dir is:')
        print(root_dir)
        test_file_path = os.path.join(root_dir,'examples/test_files/Purk2M9s.nml')
        print('test file path is:')
        print(test_file_path)
        f = open(test_file_path,'r')
        #print(f.read())
        doc = loaders.NeuroMLLoader.load(test_file_path)
        self.assertEqual(doc.id,'Purk2M9s')
