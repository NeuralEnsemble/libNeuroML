#!/usr/bin/env python3
"""
Test utilities

File: neuroml/test/test_utils.py

Copyright 2022 NeuroML contributors
"""

import neuroml
from neuroml.utils import component_factory, create_cell
import unittest
import tempfile


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

    def test_simple_cell(self):
        "Test a simple cell."

        cell = create_cell("simple_cell")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 10.0
        soma_0 = add_segment(
            cell,
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 10.0, 0.0, diam],
            name="Seg0_soma_0",
            group="soma_0",
        )

        self.assertIsInstance(soma_0, neuroml.Segment)

        self.assertTrue(cell.validate(True))

        # test with component_factory
        cell = component_factory("Cell", id="simple_cell")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 10.0
        soma_0 = add_segment(
            cell,
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 10.0, 0.0, diam],
            name="Seg0_soma_0",
            group="soma_0",
        )

        self.assertIsInstance(soma_0, neuroml.Segment)

        self.assertTrue(cell.validate(True))

    def test_complex_cell(self):
        """Test a complex cell."""
        cell = create_cell("complex_cell")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 30.0
        soma_0 = add_segment(
            cell,
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 20.0, 0.0, diam],
            name="Seg0_soma_0",
            group="soma_0",
        )
        self.assertIsInstance(soma_0, neuroml.Segment)

        dend_0 = add_segment(
            cell,
            prox=[soma_0.distal.x, soma_0.distal.y, soma_0.distal.z, 5],
            dist=[soma_0.distal.x, soma_0.distal.y + 50, soma_0.distal.z, 2],
            name="dend_0",
            group="dend_0",
            parent=soma_0,
        )
        self.assertIsInstance(dend_0, neuroml.Segment)

        self.assertTrue(cell.validate(True))

        # with component_factory
        cell = component_factory("Cell", id="complex_cell")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 30.0
        soma_0 = add_segment(
            cell,
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 20.0, 0.0, diam],
            name="Seg0_soma_0",
            group="soma_0",
        )
        self.assertIsInstance(soma_0, neuroml.Segment)

        dend_0 = add_segment(
            cell,
            prox=[soma_0.distal.x, soma_0.distal.y, soma_0.distal.z, 5],
            dist=[soma_0.distal.x, soma_0.distal.y + 50, soma_0.distal.z, 2],
            name="dend_0",
            group="dend_0",
            parent=soma_0,
        )
        self.assertIsInstance(dend_0, neuroml.Segment)

        self.assertTrue(cell.validate(True))

    def test_create_cell(self):
        """Test cell creation"""
        new_cell = create_cell(cell_id="test_cell")
        self.assertIsInstance(new_cell, neuroml.Cell)

        nml_doc = component_factory("NeuroMLDocument", id="test_cell_doc")
        nml_doc.cells.append(new_cell)
        # cell does not have segments: is invalid NeuroML
        self.assertFalse(nml_doc.validate(False))
