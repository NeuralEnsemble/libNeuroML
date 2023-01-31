#!/usr/bin/env python3
"""
Test utilities

File: neuroml/test/test_utils.py

Copyright 2023 NeuroML contributors
"""

import neuroml
from neuroml.utils import component_factory
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
