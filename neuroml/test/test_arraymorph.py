import neuroml.arraymorph as am
import numpy as np

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestMorphology(unittest.TestCase):

    def setUp(self):

        self.valid_vertices = [[0,0,0,0.1],[1,0,0,0.2],[2,0,0,0.3],[3,0,0,0.4]]
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

    def test_to_root(self):
        new_morphology = am.Morphology(self.optimized_morphology.vertices,
                                       self.optimized_morphology.connectivity)

        new_morphology.to_root(2)
        new_connectivity = new_morphology.connectivity
        self.assertTrue(np.array_equal(new_connectivity,[1,2,-1,2]))

    def test_to_neuroml_morphology(self):
        neuroml_morphology = self.optimized_morphology.to_neuroml_morphology(id="Test")
        self.assertEqual(neuroml_morphology.id,"Test")
        self.assertEqual(len(neuroml_morphology.segments),3)


    def test_pop(self):
        new_morphology = am.Morphology(self.optimized_morphology.vertices,
                                       self.optimized_morphology.connectivity)#
 
        new_morphology.pop(1)
        new_connectivity = new_morphology.connectivity
        print new_connectivity
        self.assertTrue(np.array_equal(new_connectivity,[-1,0,1]))

