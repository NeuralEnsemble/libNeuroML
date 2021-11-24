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

import platform


class TestNML(unittest.TestCase):

    """Tests related to nml.py"""

    def test_get_members(self):
        """Test get_members()"""
        example_base = neuroml.Base(id="examplebase")
        base_members = example_base.get_members()

        member_names = []
        for m in base_members:
            member_names.append(m.get_name())

        # From parent: baseWithoutId
        self.assertIn("neuro_lex_id", member_names)
        # From itself
        self.assertIn("id", member_names)
        # Not in here:
        self.assertNotIn("cell", member_names)

    def test_generic_add_single(self):
        """Test the generic add function for single addition."""
        doc = neuroml.NeuroMLDocument(id="testdoc")
        cell = neuroml.Cell(id="testcell")
        cell1 = neuroml.Cell(id="testcell1")
        biprop = neuroml.BiophysicalProperties(id="biprops")
        net = neuroml.Network(id="net")

        # Success: returns nothing (None)
        self.assertIsNone(doc.add(cell))

        # Already added, so throw exception
        if int(platform.python_version_tuple()[0]) > 2:
            with self.assertWarns(UserWarning):
                doc.add(cell)
        else:
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

    def test_generic_add_multiple(self):
        """Test add() when an object may belong to multiple members.

        From our example on the docs.
        """
        na_channel = neuroml.IonChannelHH(
            id="na_channel",
            notes="Sodium channel for HH cell",
            conductance="10pS",
            species="na",
        )
        gate_m = neuroml.GateHHRates(
            id="na_m", instances="3", notes="m gate for na channel"
        )

        m_forward_rate = neuroml.HHRate(
            type="HHExpLinearRate", rate="1per_ms", midpoint="-40mV", scale="10mV"
        )
        m_reverse_rate = neuroml.HHRate(
            type="HHExpRate", rate="4per_ms", midpoint="-65mV", scale="-18mV"
        )

        # HHRate can go to two different members, so an exception is thrown
        # needs hint, as done below
        with self.assertRaises(Exception):
            gate_m.add(m_forward_rate)
        with self.assertRaises(Exception):
            gate_m.add(m_reverse_rate)

        gate_m.add(m_forward_rate, hint="forward_rate")
        gate_m.add(m_reverse_rate, hint="reverse_rate")

        na_channel.gate_hh_rates.append(gate_m)

        gate_h = neuroml.GateHHRates(
            id="na_h", instances="1", notes="h gate for na channel"
        )
        h_forward_rate = neuroml.HHRate(
            type="HHExpRate", rate="0.07per_ms", midpoint="-65mV", scale="-20mV"
        )
        h_reverse_rate = neuroml.HHRate(
            type="HHSigmoidRate", rate="1per_ms", midpoint="-35mV", scale="10mV"
        )

        # HHRate can go to two different members, so an exception is thrown
        # needs hint, as done below
        with self.assertRaises(Exception):
            gate_h.add(h_forward_rate)
        with self.assertRaises(Exception):
            gate_h.add(h_reverse_rate)

        gate_h.add(h_forward_rate, hint="forward_rate")
        gate_h.add(h_reverse_rate, hint="reverse_rate")

    def test_add_to_container(self):
        """Test adding multiple objects to a container class."""
        network = neuroml.Network()
        # They have the same id, but they are unique objects as far as Python
        # is concerned
        pop0 = neuroml.Population()
        pop1 = neuroml.Population()
        pop2 = neuroml.Population()

        network.add(pop0)
        network.add(pop1)
        network.add(pop2)

        pop3 = neuroml.Population(id="unique")
        network.add(pop3)
        # warning because this is already added
        if int(platform.python_version_tuple()[0]) > 2:
            with self.assertWarns(UserWarning):
                network.add(pop3)
        else:
            network.add(pop3)

        # Note that for Python, this is a new object
        # So we can add it again
        pop4 = neuroml.Population(id="unique")
        network.add(pop4)

    def test_info(self):
        """Test getting member info."""
        cell = neuroml.Cell(id="testcell")
        info = cell.info()
        if int(platform.python_version_tuple()[0]) > 2:
            self.assertRegex(info, "morphology")
            self.assertRegex(info, "biophysical_properties")
            self.assertNotRegex(info, "network")
