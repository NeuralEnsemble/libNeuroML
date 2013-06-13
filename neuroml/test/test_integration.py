import neuroml
import neuroml.arraymorph as arraymorph
import neuroml.writers as writers

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestIntegration(unittest.TestCase):

    def test_arraymorph_write(self):

        vertices = [[0,0,0,0.1],[1,0,0,0.2],[2,0,0,0.3],[3,0,0,0.4]]
        connectivity = [-1,0,1,2]
        
        test_morphology = arraymorph.Morphology(vertices=vertices,
                                        connectivity=connectivity)

        neuroml_morphology = test_morphology.to_neuroml_morphology(id="Test")

        self.assertEqual(neuroml_morphology.id,"Test")
        self.assertEqual(len(neuroml_morphology.segments),3)

        writers.NeuroMLWriter.write(neuroml_morphology,'/dev/null')
        
