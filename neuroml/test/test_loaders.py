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

try:
    import pathlib
except ImportError:
    pathlib = False


class TestNeuroMLLoader(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(neuroml.__file__)
        print('root dir is:')
        print(root_dir)
        self.test_file_path = os.path.join(root_dir, 'examples/test_files/Purk2M9s.nml')

    def check_can_load_nml(self, test_file_path):
        print('test file path is:')
        print(test_file_path)
        # f = open(test_file_path, 'r'):
        # print(f.read())
        doc = loaders.NeuroMLLoader.load(test_file_path)
        self.assertEqual(doc.id, 'Purk2M9s')

    def test_load_neuroml_str_path(self):
        self.check_can_load_nml(self.test_file_path)

    @unittest.skipUnless(pathlib, "requires pathlib (>py3.4)")
    def test_load_neuroml_pathlib(self):
        self.check_can_load_nml(pathlib.Path(self.test_file_path))
