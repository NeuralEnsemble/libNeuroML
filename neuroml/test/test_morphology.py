"""
Unit tests for the Morphology class


"""

import neuroml

try:
    import unittest2 as unittest
except ImportError:
    import unittest
    

class TestSingleMorphology(unittest.TestCase):

    def test_id(self):
        """
        Test if Morphology instantiation and id assignment is working
        """
        
        test_morphology = neuroml.Morphology()
        test_morphology.id = "TestMorph"
        self.assertEqual(test_morphology.id,"TestMorph")
