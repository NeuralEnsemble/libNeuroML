import neuroml.arraymorph as am
import neuroml
import numpy as np
import neuroml.writers as writers
import neuroml.loaders as loaders

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestObjectBuiltMorphology(unittest.TestCase):

    def setUp(self):
        """
        Testing a complex hand-built morphology (from neuroml objects
        rather than arrays)
        """

        p = neuroml.Point3DWithDiam(x=0,y=0,z=0,diameter=50)
        d = neuroml.Point3DWithDiam(x=50,y=0,z=0,diameter=50)
        soma = neuroml.Segment(proximal=p, distal=d)
        soma.name = 'Soma'
        soma.id = 0
        
        #now make an axon with 100 compartments:
        
        parent = neuroml.SegmentParent(segments=soma.id)
        parent_segment = soma
        axon_segments = []
        seg_id = 1
        for i in range(100):
            p = neuroml.Point3DWithDiam(x=parent_segment.distal.x,
                                        y=parent_segment.distal.y,
                                        z=parent_segment.distal.z,
                                        diameter=0.1)
        
            d = neuroml.Point3DWithDiam(x=parent_segment.distal.x+10,
                                        y=parent_segment.distal.y,
                                        z=parent_segment.distal.z,
                                        diameter=0.1)
        
            axon_segment = neuroml.Segment(proximal = p, 
                                           distal = d, 
                                           parent = parent)
        
            axon_segment.id = seg_id
            
            axon_segment.name = 'axon_segment_' + str(axon_segment.id)
        
            #now reset everything:
            parent = neuroml.SegmentParent(segments=axon_segment.id)
            parent_segment = axon_segment
            seg_id += 1 
        
            axon_segments.append(axon_segment)

        test_morphology = am.ArrayMorphology()
        test_morphology.segments.append(soma)
        test_morphology.segments += axon_segments
        test_morphology.id = "TestMorphology"

        self.test_morphology = test_morphology

    def test_valid_morphology_ids(self):
        morphology = self.test_morphology
        self.assertTrue(morphology.valid_ids)

    def test_invalid_morphology_ids(self):
        morphology = self.test_morphology
        morphology.segments[0].id = 5 
        self.assertFalse(morphology.valid_ids)

    def test_num_segments(self):
        num_segments = len(self.test_morphology.segments)
        self.assertEqual(num_segments,101)

    def test_segments_ids_ok(self):
        self.assertEqual(self.test_morphology.segments[30].id,30)

    def test_soma_still_located_at_zero(self):
        self.assertEqual(self.test_morphology.segments[0].name,'Soma')
        self.assertEqual(self.test_morphology.segments[0].id,0)

    def test_segment_vertices_ok(self):
        self.assertEqual(self.test_morphology.segments[1].proximal.x,50.0)
                               
    def test_axon_names_ok(self):
        self.assertEqual(self.test_morphology.segments[32].name,'axon_segment_32')

    def test_segment_instance(self):
        seg = self.test_morphology.segments[47]
        self.assertIsInstance(seg,neuroml.nml.nml.Segment)

class TestArrayMorphology(unittest.TestCase):

    def setUp(self):

        num_segments = int(100)
        num_vertices = num_segments + 1

        x = np.linspace(0,10,num_vertices)
        y = np.zeros(num_vertices)
        z = np.zeros(num_vertices)
        d = np.linspace(1,0.01,num_vertices)

        connectivity = range(-1,num_segments)

        vertices = np.array([x,y,z,d]).T

        self.complex_vertices = vertices
        
        physical_mask = np.zeros(num_vertices)

        #third segment is non-physical:
        physical_mask[2] = 1
        physical_mask[20] = 1
        
        self.complex_morphology = am.ArrayMorphology(vertices=vertices,
                                                     connectivity=connectivity,
                                                     physical_mask=physical_mask,
                                                     id = 'test_arraymorph')

        self.valid_vertices = [[0,0,0,0.1],
                               [1,0,0,0.2],
                               [2,0,0,0.3],
                               [3,0,0,0.4]]

        self.valid_connectivity = [-1,0,1,2]

        self.optimized_morphology = am.ArrayMorphology(vertices=self.valid_vertices,
                                                       connectivity=self.valid_connectivity,
                                                       id = 'test_arraymorph')

        proximal_point = neuroml.Point3DWithDiam(x=0.1,
                                                 y=0.2,
                                                 z=0.3,
                                                 diameter=1.1,)

        distal_point = neuroml.Point3DWithDiam(x=0.0,
                                               y=0.0,
                                               z=0.0,
                                               diameter=1.1,)

        soma = neuroml.Segment(proximal = proximal_point,
                               distal = distal_point,)
        self.small_morphology = am.ArrayMorphology()
        self.small_morphology.segments.append(soma)

    def test_single_segment_morphology_instantiation(self):
        print(self.small_morphology.connectivity)
        seg = self.small_morphology.segments[0]
        self.assertIsInstance(seg,neuroml.nml.nml.Segment)

    def test_single_segment_morphology_length(self):
        self.assertEqual(len(self.small_morphology.segments),1)

    def test_index_error(self):
        """
        There is no segments[1] for a one-segment morphology
        """

        self.assertRaises(IndexError,self.small_morphology.segments.__getitem__,1)
        
    def test_single_floating_segment(self):
        """
        Because physical_mask[4] = 1 a segment should be skipped as it is
        floating.
        """
        
        seg = self.complex_morphology.segments[3]
        seg_proximal_x = seg.proximal.x
        seg_distal_x = seg.distal.x

        equivalent_proximal_vertex = self.complex_vertices[5][0]
        equivalent_distal_vertex = self.complex_vertices[4][0]

        self.assertEqual(seg_proximal_x,equivalent_proximal_vertex)       
        self.assertEqual(seg_distal_x,equivalent_distal_vertex)       

    def test_double_floating_segment(self):
        """
        Because physical_mask[4] = 1 a segment should be skipped as it is
        floating.
        """
        
        seg = self.complex_morphology.segments[3]
        seg_proximal_x = seg.proximal.x
        seg_distal_x = seg.distal.x

        equivalent_proximal_vertex = self.complex_vertices[5][0]
        equivalent_distal_vertex = self.complex_vertices[4][0]

        self.assertEqual(seg_proximal_x,equivalent_proximal_vertex)       
        self.assertEqual(seg_distal_x,equivalent_distal_vertex)       


    def test_segments_len(self):
        num_segments = 98
        len_segment_list = len(self.complex_morphology.segments)
        self.assertEqual(num_segments,len_segment_list)

    def test_add_segment_len(self):
        """
        Add a neuroml.Segment() object, the segments proximal
        and distal vertices should be used. The internal connectivity
        should be passed.
        """
        
        proximal_point = neuroml.Point3DWithDiam(x=0.1,
                                                 y=0.2,
                                                 z=0.3,
                                                 diameter=1.1,)

        distal_point = neuroml.Point3DWithDiam(x=0.0,
                                               y=0.0,
                                               z=0.0,
                                               diameter=1.1,)

        seg = neuroml.Segment(proximal = proximal_point,
                              distal = distal_point)

        num_segments = len(self.complex_morphology.segments)

        self.complex_morphology.segments.append(seg)

        len_segment_list = len(self.complex_morphology.segments)

        self.assertEqual(num_segments+1, len_segment_list)
        self.setUp()

    def test_add_segment_vertices_added(self):
        proximal_point = neuroml.Point3DWithDiam(x=0.1,
                                                 y=0.2,
                                                 z=0.3,
                                                 diameter=0.1,)

        distal_point = neuroml.Point3DWithDiam(x=0.0,
                                               y=0.0,
                                               z=0.0,
                                               diameter=0.1)

        seg = neuroml.Segment(proximal = proximal_point,
                              distal = distal_point)

        num_segments = len(self.complex_morphology.segments)

        self.optimized_morphology.segments.append(seg)

        true_vertices = self.optimized_morphology.vertices
        expected_vertices = np.array([[0,0,0,0.1],
                                      [1,0,0,0.2],
                                      [2,0,0,0.3],
                                      [3,0,0,0.4],
                                      [0,0,0,0.1],
                                      [0.1,0.2,0.3,0.1],])

        arrays_equal = np.array_equal(true_vertices,expected_vertices)

        self.assertTrue(arrays_equal)
        self.setUp()
        
    def tes_add_segment_connectivity_valid(self):
        pass

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
        self.assertTrue(np.array_equal(new_connectivity,[-1,0,1]))

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

        p = neuroml.Point3DWithDiam(x=0.9,
                                    y=0.0,
                                    z=0.0,
                                    diameter=0.1)
    
        d = neuroml.Point3DWithDiam(x=0.0,
                                    y=0.0,
                                    z=0.0,
                                    diameter=0.1)

        new_segment = neuroml.Segment(proximal=p,
                                      distal=d)

        self.optimized_morphology.segments[2] = new_segment

        self.assertEqual(self.optimized_morphology.segments[2],new_segment)

    def test_segmentlist_setter_by_inference(self):

        p = neuroml.Point3DWithDiam(x=0.9,
                                    y=0.0,
                                    z=0.0,
                                    diameter=0.1)
    
        d = neuroml.Point3DWithDiam(x=0.0,
                                    y=0.0,
                                    z=0.0,
                                    diameter=0.1)

        new_segment = neuroml.Segment(proximal=p,
                                      distal=d)

        self.optimized_morphology.segments[2] = new_segment
        self.assertEqual(self.optimized_morphology.segments[2].proximal.x,0.9)


    def test_instantiation(self):
        """
        Test an arraymorph can be instantiated with default parameters
        """
        morphology = am.ArrayMorphology()

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

    def test_valid_morphology_ids(self):
        morphology = self.optimized_morphology
        self.assertTrue(morphology.valid_ids)

    def test_invalid_morphology_ids(self):
        morphology = self.optimized_morphology
        morphology.segments[0].id = 5 
        self.assertFalse(morphology.valid_ids)

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
