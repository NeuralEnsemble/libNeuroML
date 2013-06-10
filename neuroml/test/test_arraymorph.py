import neuroml.arraymorph as am
import numpy as np

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestMorphology(unittest.TestCase):

    def setUp(self):

        self.valid_vertices = [[0,0,0,0.1],[1,1,1,0.1],[2,2,2,0.1],[3,3,3,0.1]]
        self.valid_connectivity = [-1,0,1,2]

        self.optimized_morphology = am.Morphology(vertices=self.valid_vertices,
                                             connectivity=self.valid_connectivity)

    def test_num_vertices(self):
        """
        Morphology with one segment
        """

        self.assertEqual(self.optimized_morphology.num_vertices,4)

    def test_valid_morphology(self):
        """
        Should return false if morphology is invalid
        """

        vertices=[[0,0,0],[1,1]]
        connectivity=[-1,0]
        self.assertRaises(AssertionError,am.Morphology,vertices,connectivity)

        vertices=[[0,0,0],[1,1,1]]
        connectivity=[-1,0,0]
        self.assertRaises(AssertionError,am.Morphology,vertices,connectivity)

        vertices=[[0,0,0],[1,1,1]]
        connectivity=[]
        self.assertRaises(AssertionError,am.Morphology,vertices,connectivity)

    def test_root_index(self):
        self.assertEqual(self.optimized_morphology.root_index,0)
        
    def test_physical_indeces(self):
        physical_indices = self.optimized_morphology.physical_indices
        self.assertTrue(np.array_equal(physical_indices,[0,1,2,3]))

    def test_children(self):
        self.assertTrue(self.optimized_morphology.children(1),2)
