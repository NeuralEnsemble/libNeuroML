import neuroml.arraymorph as am
import neuroml
import numpy as np
import neuroml.writers as writers
import neuroml.loaders as loaders

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestMorphology(unittest.TestCase):

    def setUp(self):

        self.valid_vertices = [[0,0,0,0.1],[1,0,0,0.2],[2,0,0,0.3],[3,0,0,0.4]]
        self.valid_connectivity = [-1,0,1,2]

        self.optimized_morphology = am.ArrayMorphology(vertices=self.valid_vertices,
                                                  connectivity=self.valid_connectivity,
                                                  id = 'test_arraymorph')

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
        self.assertRaises(AssertionError,am.ArrayMorphology,vertices,connectivity)

        vertices=[[0,0,0],[1,1,1]]
        connectivity=[-1,0,0]
        self.assertRaises(AssertionError,am.ArrayMorphology,vertices,connectivity)

        vertices=[[0,0,0],[1,1,1]]
        connectivity=[]
        self.assertRaises(AssertionError,am.ArrayMorphology,vertices,connectivity)

    def test_root_index(self):
        self.assertEqual(self.optimized_morphology.root_index,0)
        
    def test_physical_indeces(self):
        physical_indices = self.optimized_morphology.physical_indices
        self.assertTrue(np.array_equal(physical_indices,[0,1,2,3]))

    def test_children(self):
        self.assertTrue(self.optimized_morphology.children(1),2)

    def test_to_root(self):
        new_morphology = am.ArrayMorphology(self.optimized_morphology.vertices,
                                       self.optimized_morphology.connectivity)

        new_morphology.to_root(2)
        new_connectivity = new_morphology.connectivity
        self.assertTrue(np.array_equal(new_connectivity,[1,2,-1,2]))

    def test_to_neuroml_morphology(self):
        neuroml_morphology = self.optimized_morphology.to_neuroml_morphology(id="Test")
        self.assertEqual(neuroml_morphology.id,"Test")
        self.assertEqual(len(neuroml_morphology.segments),3)


    def test_pop(self):
        new_morphology = am.ArrayMorphology(self.optimized_morphology.vertices,
                                       self.optimized_morphology.connectivity)#
 
        new_morphology.pop(1)
        new_connectivity = new_morphology.connectivity
        print new_connectivity
        self.assertTrue(np.array_equal(new_connectivity,[-1,0,1]))

    #TODO    
    #def test_write(self):
    #    writers.ArrayMorphWriter.write(self.optimized_morphology,'test.h5')

    def test_load(self):
        loaders.ArrayMorphLoader.load('test.h5')

    def test_segment_getter(self):
        segment = self.optimized_morphology.segments[0]
        self.assertIsInstance(segment,neuroml.Segment)
        self.assertEqual(segment.proximal.diameter,0.2)
        self.assertEqual(segment.distal.diameter,0.1)

    def test_segmentlist_getter(self):
        segment = self.optimized_morphology.segments[1]
        segment_again = self.optimized_morphology.segments[1]
        self.assertEqual(segment,segment_again)

    def test_segmentlist_setter(self):
        new_segment = neuroml.Segment(proximal=0.9)
        self.optimized_morphology.segments[2] = new_segment
        self.assertEqual(self.optimized_morphology.segments[2],new_segment)
        self.assertEqual(self.optimized_morphology.segments[2].proximal,0.9)
        self.setUp()

    def test_parents(self):
        """
        A segment by default uses its vertex index as its ID,
        as a consequence the first segment has index = 1
        """

        test_segment_1 = self.optimized_morphology.segments[0]
        test_segment_2 = self.optimized_morphology.segments[1]

        self.assertEqual(test_segment_1.id,1)
        self.assertEqual(test_segment_2.id,2)
        self.assertEqual(test_segment_2.parent.segments,1)
        self.assertIsNone(test_segment_1.parent)

    def test_large_arraymorph(self):
        """
        This will generate a morphology which will be difficult to
        generate without the optimized intenral representation.

        The morphology has 3 million segments
        """

        num_segments = int(1e6)
        num_vertices = num_segments + 1

        x = np.linspace(0,10,num_vertices)
        y = np.zeros(num_vertices)
        z = np.zeros(num_vertices)
        d = np.linspace(1,0.01,num_vertices)

        vertices = np.array([x,y,z,d]).T
        
        connectivity = range(-1,num_segments)

        big_arraymorph = am.ArrayMorphology(vertices = vertices,
                                            connectivity = connectivity)

        self.assertIsInstance(big_arraymorph.segments[3],neuroml.Segment)

        self.assertEqual(big_arraymorph.segments[0].distal.diameter,1.0)
        #following test not as obvious as it seems - first execution of getter does not have the same result as second
        self.assertEqual(big_arraymorph.segments[2333],big_arraymorph.segments[2333])
        
        self.assertEqual(big_arraymorph.segments[0].distal.diameter,1.0)
        self.assertEqual(big_arraymorph.segments[num_segments-1].proximal.x,10.0)
        self.assertEqual(big_arraymorph.segments[0].distal.x,0.0)
        self.assertEqual(big_arraymorph.segments[num_segments-1].proximal.diameter,0.01)
