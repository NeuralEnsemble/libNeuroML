"""
Unit tests for writers

"""

import neuroml
from neuroml import writers
import os
import numpy as np
from neuroml import arraymorph as am

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
        writer_method(self.big_arraymorph,'dev/null')        
        try:
            writer_method(self.big_arraymorph,'dev/null')
        except:
            self.fail("Exception raised!")
