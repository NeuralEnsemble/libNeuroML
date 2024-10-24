"""
Unit tests for writers

"""

import tempfile

import numpy as np

import neuroml
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

        a = 6  # not NeuroML-writeable
        writer_method = neuroml.writers.NeuroMLWriter.write
        self.assertRaises(AttributeError, writer_method, a, "tmpfile")


class TestArrayMorphWriter(unittest.TestCase):
    def setUp(self):
        num_segments = int(1e6)
        num_vertices = num_segments + 1

        x = np.linspace(0, 10, num_vertices)
        y = np.zeros(num_vertices)
        z = np.zeros(num_vertices)
        d = np.linspace(1, 0.01, num_vertices)

        vertices = np.array([x, y, z, d]).T

        connectivity = range(-1, num_segments)

        big_arraymorph = am.ArrayMorphology(
            vertices=vertices, connectivity=connectivity
        )
        transposed_x = x + 10
        transposed_vertices = np.array([transposed_x, y, z, d]).T

        transposed_arraymorph = am.ArrayMorphology(
            vertices=transposed_vertices, connectivity=connectivity
        )

        bigger_d = d + 0.5
        fatter_vertices = np.array([x, y, z, bigger_d]).T

        fatter_arraymorph = am.ArrayMorphology(
            vertices=fatter_vertices, connectivity=connectivity
        )

        self.transposed_arraymorph = transposed_arraymorph
        self.fatter_arraymorph = fatter_arraymorph
        self.big_arraymorph = big_arraymorph

        self.cell_1 = neuroml.Cell(id="cell_1")
        self.cell_2 = neuroml.Cell(id="cell_2")
        self.cell_3 = neuroml.Cell(id="cell_3")

        self.cell_1.morphology = transposed_arraymorph
        self.cell_2.morphology = fatter_arraymorph
        self.cell_3.morphology = big_arraymorph

        self.test_doc = neuroml.NeuroMLDocument(id="TestDocument")

        self.test_doc.cells.append(self.cell_1)
        self.test_doc.cells.append(self.cell_2)
        self.test_doc.cells.append(self.cell_3)

    def test_write_big_arraymorph(self):
        writer_method = neuroml.writers.ArrayMorphWriter.write
        filename = tempfile.mkstemp()[1]

        try:
            writer_method(self.test_doc, filename)
        except:
            self.fail("Exception raised!")

    def test_write_expected(self):
        """
        More of an integration test, write a file and confirm the contents are
        as expected.
        """

        filename = tempfile.mkstemp()[1]

        writer_method = neuroml.writers.ArrayMorphWriter.write
        writer_method(self.big_arraymorph, filename)

        loader_method = neuroml.loaders.ArrayMorphLoader.load
        doc = loader_method(filename)
        array_morph = doc.morphology[0]

        connectivity_equal = np.testing.assert_array_equal(
            array_morph.connectivity, self.big_arraymorph.connectivity
        )
        physical_masks_equal = np.testing.assert_array_equal(
            array_morph.physical_mask, self.big_arraymorph.physical_mask
        )
        vertices_equal = np.testing.assert_array_equal(
            array_morph.vertices, self.big_arraymorph.vertices
        )

        self.assertEqual(connectivity_equal, None)  # None when equal
        self.assertEqual(physical_masks_equal, None)  # None when equal
        self.assertEqual(vertices_equal, None)  # None when equal

    def test_write_multiple_morphologies(self):
        filename = tempfile.mkstemp()[1]

        writer_method = neuroml.writers.ArrayMorphWriter.write
        try:
            writer_method(self.test_doc, filename)
        except:
            self.fail("Exception raised!")

    def test_write_multiple_morphologies(self):
        filename = tempfile.mkstemp()[1]
        writer_method = neuroml.writers.ArrayMorphWriter.write
        writer_method(self.test_doc, filename)

        loader_method = neuroml.loaders.ArrayMorphLoader.load
        document = loader_method(filename)

        self.assertIsInstance(document, neuroml.NeuroMLDocument)
