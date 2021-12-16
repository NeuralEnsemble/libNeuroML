"""
Unit tests for the Morphology class

"""

import neuroml

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestSingleMorphology(unittest.TestCase):
    def setUp(self):
        self.test_morphology = neuroml.Morphology()
        self.test_morphology.id = "TestMorph"

        for i in range(10):
            self.test_morphology.segments.append(neuroml.Segment())

    def test_id(self):
        """
        Test if Morphology instantiation and id assignment is working
        """
        self.assertEqual(self.test_morphology.id, "TestMorph")

    def test_num_segments(self):
        self.assertEqual(self.test_morphology.num_segments, 10)
