#!/usr/bin/env python3
"""
Test utilities

File: neuroml/test/test_utils.py

Copyright 2023 NeuroML contributors
"""

import os
import unittest

import neuroml
from neuroml.utils import (
    component_factory,
    fix_external_morphs_biophys_in_cell,
    get_relative_component_path,
    print_hierarchy,
)
from neuroml.writers import NeuroMLWriter


class UtilsTestCase(unittest.TestCase):
    """Test the Utils module"""

    def test_component_factory(self):
        "Test the component factory."

        nml_doc = component_factory("NeuroMLDocument", id="emptydocument")
        self.assertIsInstance(nml_doc, neuroml.NeuroMLDocument)

        iaf_cell = component_factory(
            "IafCell",
            id="test_cell",
            leak_reversal="-50 mV",
            thresh="-55mV",
            reset="-70 mV",
            C="0.2nF",
            leak_conductance="0.01uS",
        )
        self.assertIsInstance(iaf_cell, neuroml.IafCell)

    @unittest.expectedFailure
    def test_component_factory_should_fail(self):
        "Test the component factory."

        iaf_cell = component_factory(
            "IafCell",
            id="test_cell",
        )

    def test_networkx_hier_graph(self):
        """Test constructing a networkx graph of a hierarchy"""
        hier = neuroml.NeuroMLDocument.get_class_hierarchy()
        self.assertIsNotNone(hier)
        print_hierarchy(hier)

        path, graph = get_relative_component_path("Input", "Instance")
        self.assertIsNotNone(graph)
        self.assertEqual(path, "../Population/Instance")

    def test_fix_external_morphs_biophys_in_cell(self):
        """Test fix_external_morphs_biophys_in_cell function"""
        # document that includes cell and morphology with cell referring to
        # morphology
        nml_doc = component_factory("NeuroMLDocument", id="testdoc")
        nml_doc.add("Morphology", id="test_morph_1", validate=False)
        test_cell_1 = nml_doc.add(
            "Cell", id="test_cell_1", morphology_attr="test_morph_1"
        )
        test_cell_1.morphology = None

        fix_external_morphs_biophys_in_cell(nml_doc)
        self.assertIsNotNone(nml_doc.cells[0].morphology)
        self.assertIsNone(nml_doc.cells[0].morphology_attr)
        self.assertEqual(nml_doc.cells[0].morphology.id, "test_morph_1")
        print(nml_doc)

        # check that a key error is raised if the referenced morph cannot be
        # found
        nml_doc_2 = component_factory("NeuroMLDocument", id="testdoc")
        nml_doc_2.add("Morphology", id="test_morph_5", validate=False)
        test_cell_2 = nml_doc_2.add(
            "Cell", id="test_cell_1", morphology_attr="test_morph_1"
        )
        test_cell_2.morphology = None

        with self.assertRaises(KeyError):
            fix_external_morphs_biophys_in_cell(nml_doc_2)
            print(nml_doc_2)

    def test_fix_external_morphs_biophys_in_cell_2(self):
        """Test fix_external_morphs_biophys_in_cell function"""
        # document that includes cell and biophysical properties with cell
        # referring to biophysical properties
        nml_doc = component_factory("NeuroMLDocument", id="testdoc")
        nml_doc.add("BiophysicalProperties", id="test_biophys_1", validate=False)
        test_cell_1 = nml_doc.add(
            "Cell", id="test_cell_1", biophysical_properties_attr="test_biophys_1"
        )
        test_cell_1.biophysical_properties = None

        fix_external_morphs_biophys_in_cell(nml_doc)
        self.assertIsNotNone(nml_doc.cells[0].biophysical_properties)
        self.assertIsNone(nml_doc.cells[0].biophysical_properties_attr)
        self.assertEqual(nml_doc.cells[0].biophysical_properties.id, "test_biophys_1")
        print(nml_doc)

        # check that a key error is raised if the referenced biophysical
        # property cannot be found
        nml_doc_2 = component_factory("NeuroMLDocument", id="testdoc")
        nml_doc_2.add("BiophysicalProperties", id="test_biophys_5", validate=False)
        test_cell_2 = nml_doc_2.add(
            "Cell", id="test_cell_1", biophysical_properties_attr="test_biophys_1"
        )
        test_cell_2.biophysical_properties = None
        print(nml_doc_2)

        with self.assertRaises(KeyError):
            fix_external_morphs_biophys_in_cell(nml_doc_2)

    def test_fix_external_morphs_biophys_in_cell_3(self):
        """Test fix_external_morphs_biophys_in_cell function"""
        filename = "nml_morph_doc.nml"
        nml_doc = component_factory("NeuroMLDocument", id="testdoc")
        nml_doc.add("Morphology", id="test_morph_1", validate=False)
        NeuroMLWriter.write(nml_doc, file=filename)

        # doc that includes
        nml_doc_2 = component_factory("NeuroMLDocument", id="testdoc")
        nml_doc_2.add("IncludeType", href=filename)
        test_cell_1 = nml_doc_2.add(
            "Cell", id="test_cell_1", morphology_attr="test_morph_1"
        )
        test_cell_1.morphology = None

        fix_external_morphs_biophys_in_cell(nml_doc_2)
        self.assertIsNotNone(nml_doc_2.cells[0].morphology)
        self.assertIsNone(nml_doc_2.cells[0].morphology_attr)
        self.assertEqual(nml_doc_2.cells[0].morphology.id, "test_morph_1")
        print(nml_doc_2)
        os.unlink(filename)

        # doc that does not include, and should fail
        nml_doc_3 = component_factory("NeuroMLDocument", id="testdoc")
        test_cell_2 = nml_doc_3.add(
            "Cell", id="test_cell_1", morphology_attr="test_morph_1"
        )
        test_cell_2.morphology = None
        print(nml_doc_3)
        with self.assertRaises(KeyError):
            fix_external_morphs_biophys_in_cell(nml_doc_3)

    def test_fix_external_morphs_biophys_in_cell_4(self):
        """Test fix_external_morphs_biophys_in_cell function"""
        # document that includes cell and biophysical properties with cell
        # referring to biophysical properties
        filename = "nml_biophys_doc.nml"
        nml_doc = component_factory("NeuroMLDocument", id="testdoc")
        nml_doc.add("BiophysicalProperties", id="test_biophys_1", validate=False)
        NeuroMLWriter.write(nml_doc, file=filename)

        # doc that includes
        nml_doc_2 = component_factory("NeuroMLDocument", id="testdoc")
        nml_doc_2.add("IncludeType", href=filename)
        test_cell_1 = nml_doc_2.add(
            "Cell", id="test_cell_1", biophysical_properties_attr="test_biophys_1"
        )
        test_cell_1.biophysical_properties = None

        fix_external_morphs_biophys_in_cell(nml_doc_2)
        self.assertIsNotNone(nml_doc_2.cells[0].biophysical_properties)
        self.assertIsNone(nml_doc_2.cells[0].biophysical_properties_attr)
        self.assertEqual(nml_doc_2.cells[0].biophysical_properties.id, "test_biophys_1")
        print(nml_doc_2)
        os.unlink(filename)

        # doc that does not include, and should fail
        nml_doc_3 = component_factory("NeuroMLDocument", id="testdoc")
        test_cell_2 = nml_doc_3.add(
            "Cell", id="test_cell_1", biophysical_properties_attr="test_biophys_1"
        )
        test_cell_2.biophysical_properties = None
        print(nml_doc_3)
        with self.assertRaises(KeyError):
            fix_external_morphs_biophys_in_cell(nml_doc_3)
