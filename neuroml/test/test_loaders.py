"""
Unit tests for loaders

"""

import os

import neuroml
from neuroml import loaders

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestNeuroMLLoader(unittest.TestCase):
    def test_load_neuroml(self):
        root_dir = os.path.dirname(neuroml.__file__)
        print("root dir is: " + root_dir)
        test_file_path = os.path.join(root_dir, "examples/test_files/Purk2M9s.nml")
        print("test fi le path is: " + test_file_path)

        f = open(test_file_path, "r")
        # print(f.read())
        doc = loaders.NeuroMLLoader.load(test_file_path)
        self.assertEqual(doc.id, "Purk2M9s")
        f.close()
        print("Finished test")

    def test_read_neuroml2_file(self):
        """Test the `read_neuroml2_file` method"""
        root_dir = os.path.dirname(neuroml.__file__)
        test_file_path = os.path.join(root_dir, "examples/test_files/MediumNet.net.nml")
        doc = loaders.read_neuroml2_file(test_file_path, include_includes=True)
        doc_info = doc.info(show_contents=True, return_format="dict")
        doc2 = loaders.read_neuroml2_file(test_file_path, include_includes=True)
        doc2_info = doc2.info(show_contents=True, return_format="dict")

        # check that the ids of the two are the same
        self.assertEqual(doc_info["id"], doc2_info["id"])

    def test_non_neuroml_file(self):
        """Test an non-NeuroML document."""
        root_dir = os.path.dirname(neuroml.__file__)
        test_file_path = os.path.join(root_dir, "examples/test_files/sbml-example.xml")
        print("test file path is: " + test_file_path)

        try:
            loaders.NeuroMLLoader.load(test_file_path)
        except TypeError:
            print("Exception raised. Test passes.")


if __name__ == "__main__":
    t = TestNeuroMLLoader()
    t.test_load_neuroml()
