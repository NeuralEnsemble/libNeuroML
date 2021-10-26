#!/usr/bin/env python3
"""
Enter one line description here.

File:

Copyright 2021 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import neuroml
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestNML(unittest.TestCase):

    """Tests related to nml.py"""

    def test_generic_add(self):
        """Test the generic add function.
        :returns: TODO

        """
        doc = neuroml.NeuroMLDocument(id="testdoc")
        cell = neuroml.Cell(id="testcell")
        cell1 = neuroml.Cell(id="testcell1")
        biprop = neuroml.BiophysicalProperties(id="biprops")
        net = neuroml.Network(id="net")

        # Success: returns nothing (None)
        self.assertIsNone(doc.add(cell))

        # Already added, so throw exception
        with self.assertRaises(Exception):
            doc.add(cell)

        # Success
        self.assertIsNone(doc.add(cell1))

        # str is not the type for any member
        with self.assertRaises(Exception):
            doc.add("A STRING")

        # success
        self.assertIsNone(cell.add(biprop))
        self.assertIsNone(cell1.add(biprop))

        # failures
        with self.assertRaises(Exception):
            cell.add(net)
        with self.assertRaises(Exception):
            biprop.add(net)

    def test_info(self):
        """Test getting member info."""
        cell = neuroml.Cell(id="testcell")
        info = cell.info()
        self.assertRegex(info, 'morphology')
        self.assertRegex(info, 'biophysical_properties')
        self.assertNotRegex(info, 'network')
