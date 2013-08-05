"""
Unit tests for writers

"""

import neuroml
from neuroml import writers
from neuroml import loaders
import os
import numpy as np
from neuroml import arraymorph as am
import tempfile

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLWriter(unittest.TestCase):

    def test_write_nonsense(self):
        """
        Should Throw an attribute error as integers do not have an export method
        """

        a = 6 #not NeuroML-writeable
        writer_method = neuroml.writers.NeuroMLWriter.write
        self.assertRaises(AttributeError, writer_method, a, "tmpfile")

class TestArrayMorphWriter(unittest.TestCase):
    
    def setUp(self):
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

        self.big_arraymorph = big_arraymorph

    def test_write_big_arraymorph(self):
        writer_method = neuroml.writers.ArrayMorphWriter.write
        filename = tempfile.mkstemp()[1]

        try:
            writer_method(self.big_arraymorph,filename)
        except:
            self.fail("Exception raised!")

    def test_write_expected(self):
        """
        More of an integration test, write a file and confirm the contents are
        as expected.
        """

        filename = tempfile.mkstemp()[1]

        writer_method = neuroml.writers.ArrayMorphWriter.write
        writer_method(self.big_arraymorph,filename)

        loader_method = neuroml.loaders.ArrayMorphLoader.load
        array_morph = loader_method(filename)

        connectivity_equal = np.testing.assert_array_equal(array_morph.connectivity,self.big_arraymorph.connectivity)
        physical_masks_equal = np.testing.assert_array_equal(array_morph.physical_mask,self.big_arraymorph.physical_mask)
        vertices_equal = np.testing.assert_array_equal(array_morph.vertices,self.big_arraymorph.vertices)


        self.assertEqual(connectivity_equal,None) #None when equal
        self.assertEqual(physical_masks_equal,None) #None when equal
        self.assertEqual(vertices_equal,None) #None when equal        
        
