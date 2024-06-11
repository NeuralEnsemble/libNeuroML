#!/usr/bin/env python3
"""
Test utilities

File: neuroml/test/test_utils.py

Copyright 2023 NeuroML contributors
"""

import unittest

import neuroml
from neuroml.utils import (
    component_factory,
    get_relative_component_path,
    print_hierarchy,
)


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
