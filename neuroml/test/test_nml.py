#!/usr/bin/env python3
"""
Test nml.py functions/methods.

File: neuroml/test/test_nml.py

Copyright 2023 NeuroML contributors
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import neuroml
from neuroml.utils import component_factory, print_hierarchy


class TestNML(unittest.TestCase):
    """Tests related to nml.py"""

    def test_get_members(self):
        """Test get_members()"""
        example_base = neuroml.Base(id="examplebase")
        base_members = example_base._get_members()

        member_names = []
        for m in base_members:
            member_names.append(m.get_name())

        # From itself
        self.assertIn("id", member_names)
        # Not in here:
        self.assertNotIn("cell", member_names)

        # check with IonChannel: inherits from IonChannel
        ionchannelhh = neuroml.IonChannelHH()
        ion_members = ionchannelhh._get_members()
        member_names = []
        for m in ion_members:
            member_names.append(m.get_name())
        self.assertIn("conductance", member_names)
        self.assertIn("gates", member_names)
        self.assertIn("gate_hh_rates", member_names)

        # check with Cell
        acell = neuroml.Cell()
        cell_members = acell._get_members()
        member_names = []
        for m in cell_members:
            member_names.append(m.get_name())
        self.assertIn("properties", member_names)
        self.assertIn("morphology", member_names)
        self.assertIn("biophysical_properties", member_names)

        # again---ensure things aren't added again
        cell_members = acell._get_members()
        member_names = []
        for m in cell_members:
            member_names.append(m.get_name())
        self.assertIn("properties", member_names)
        self.assertIn("morphology", member_names)
        self.assertIn("biophysical_properties", member_names)

    def test_generic_add_single(self):
        """Test the generic add function for single addition."""
        doc = neuroml.NeuroMLDocument(id="testdoc")
        cell = neuroml.Cell(id="testcell")
        cell1 = neuroml.Cell(id="testcell1")
        biprop = neuroml.BiophysicalProperties(id="biprops")
        net = neuroml.Network(id="net")

        # Success: returns object
        self.assertIsNotNone(doc.add(cell))

        # Already added, so throw exception
        with self.assertWarns(UserWarning):
            doc.add(cell)

        # Success
        self.assertIsNotNone(doc.add(cell1))

        # str is not the type for any member
        with self.assertRaises(Exception):
            doc.add("A STRING")

        # success
        self.assertIsNotNone(cell.add(biprop))
        self.assertIsNotNone(cell1.add(biprop))

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

        # first will not validate, reverse_rate is missing
        gate_m.add(m_forward_rate, hint="forward_rate", validate=False)
        gate_m.add(m_reverse_rate, hint="reverse_rate", validate=True)

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

        gate_h.add(h_forward_rate, hint="forward_rate", validate=False)
        gate_h.add(h_reverse_rate, hint="reverse_rate")

    def test_add_to_container(self):
        """Test adding multiple objects to a container class."""
        network = neuroml.Network(id="test")
        # They have the same id, but they are unique objects as far as Python
        # is concerned
        pop0 = neuroml.Population(id="1")
        pop1 = neuroml.Population(id="2")
        pop2 = neuroml.Population(id="3")

        network.add(pop0)
        network.add(pop1)
        network.add(pop2)

        pop3 = neuroml.Population(id="unique")
        network.add(pop3)
        # warning because this is already added
        with self.assertWarns(UserWarning):
            network.add(pop3)

        # Note that for Python, this is a new object
        # So we can add it again
        pop4 = neuroml.Population(id="unique")
        network.add(pop4)

    def test_info(self):
        """Test getting member info."""
        cell = neuroml.Cell(id="testcell")
        cell.set_spike_thresh("40mV")
        cell.set_init_memb_potential("-70mV")
        cell.set_specific_capacitance("1 uF_per_cm2")
        info = cell.info()
        self.assertRegex(info, "morphology")
        self.assertRegex(info, "biophysical_properties")
        self.assertNotRegex(info, "network")

        # check with IonChannel: inherits from IonChannel
        ionchannelhh = neuroml.IonChannelHH()
        info = ionchannelhh.info(return_format="list")
        self.assertIn("conductance", info)
        self.assertIn("gates", info)
        self.assertIn("gate_hh_rates", info)

    def test_get_by_id(self):
        """Test the get_by_id method"""
        network = neuroml.Network(id="test")
        pop = neuroml.Population(id="pop0")
        network.add(pop)
        test_pop = network.get_by_id("pop0")
        self.assertIs(test_pop, pop)

    def test_component_validate(self):
        """Test validate function"""
        network = neuroml.Network()
        with self.assertRaises(ValueError) as cm:
            network.validate()
        print(cm.exception)

        res = neuroml.Resistivity(value="100 seconds")
        with self.assertRaises(ValueError) as cm:
            res.validate()
        print(cm.exception)

    def test_parentinfo(self):
        """Test the parent info method"""
        cell = neuroml.Cell(id="testcell")
        cell.set_spike_thresh("40mV")
        cell.set_init_memb_potential("-70mV")
        cell.set_specific_capacitance("1 uF_per_cm2")
        info = cell.parentinfo()
        self.assertRegex(info, "NeuroMLDocument")

        ionchannelhh = neuroml.IonChannelHH()
        info = ionchannelhh.parentinfo(return_format="list")
        self.assertIn("NeuroMLDocument", info)

        hhrate = neuroml.HHRate()
        info = hhrate.parentinfo(return_format="list")
        self.assertIn("GateHHRates", info)
        self.assertIn("GateHHRatesInf", info)
        self.assertIn("GateHHRatesTau", info)
        self.assertIn("GateHHRatesTauInf", info)

    def test_component_argument_list_checker(self):
        """Test the check_component_type_arg_list utility function"""
        nml_doc = neuroml.nml.nml.NeuroMLDocument()
        with self.assertRaises(ValueError) as cm:
            nml_doc._check_arg_list(random_argument="nope")
        print(cm.exception)
        nml_doc._check_arg_list(id="yep")

    def test_add_segment(self):
        """Test adding a segment."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        segment = new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        self.assertIsInstance(segment, neuroml.Segment)
        self.assertEqual(segment.proximal.diameter, 20.0)
        self.assertEqual(segment.proximal.x, 0.0)
        self.assertEqual(segment.distal.diameter, 20.0)
        self.assertEqual(segment.distal.x, 20.0)

        self.assertIsNone(new_cell.validate(True))

    def test_add_segment_no_group(self):
        """Test adding a segment but without a group."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        segment = new_cell.add_segment(
            (0, 0, 0, 20), (20, 0, 0, 20), name="soma", group_id=None, seg_type="soma"
        )
        self.assertIsInstance(segment, neuroml.Segment)
        self.assertEqual(segment.proximal.diameter, 20.0)
        self.assertEqual(segment.proximal.x, 0.0)
        self.assertEqual(segment.distal.diameter, 20.0)
        self.assertEqual(segment.distal.x, 20.0)

        self.assertIsNone(new_cell.validate(True))

    def test_setting_init_memb_potential(self):
        """Test adding initial membrane potential."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        new_cell.set_init_memb_potential("-65mV")

        self.assertIsNone(new_cell.validate(True))

    def test_setting_spike_thresh(self):
        """Test adding spike threshold."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")

        self.assertIsNone(new_cell.validate(True))

    @unittest.expectedFailure
    def test_setting_init_memb_potential_should_fail(self):
        """Units of membrane potential are wrong: should fail."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        # Make it invalid: wrong dimensions for membrane potential
        new_cell.set_init_memb_potential(new_cell, "-65 cm")

        self.assertIsNone(new_cell.validate(True))

    def test_setting_resistivity(self):
        """Test setting the resistivity."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        new_cell.set_resistivity("2000 ohm_cm")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        self.assertIsNone(new_cell.validate(True))

    @unittest.expectedFailure
    def test_setting_resistivity_should_fail(self):
        """Test setting the resistivity."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        new_cell.set_resistivity("2000 kilO")
        self.assertIsNone(new_cell.validate(True))

    def test_setting_specific_capacitance(self):
        """Test setting the specific_capacitance."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        new_cell.set_specific_capacitance("1.0 uF_per_cm2")
        self.assertIsNone(new_cell.validate(True))

    @unittest.expectedFailure
    def test_setting_specific_capacitance_should_fail(self):
        """Test setting the specific_capacitance."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        new_cell.set_specific_capacitance("kilo")
        self.assertIsNone(new_cell.validate(True))

    def test_setting_channel_density(self):
        """Test setting the channel_density."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        nml_doc = component_factory(
            "NeuroMLDocument", id="test_cell_with_channel_density_doc"
        )
        nml_doc.cells.append(new_cell)

        nml_doc.add(
            "IonChannel", id="pas", conductance="10 pS", type="ionChannelPassive"
        )

        new_cell.add_channel_density(
            nml_doc,
            "pas_chan",
            "pas",
            "0.021 mS_per_cm2",
            "-70.0 mV",
            "all",
            "non_specific",
            "",
        )
        # check that it was added
        self.assertNotEqual(
            len(new_cell.biophysical_properties.membrane_properties.channel_densities),
            0,
        )
        self.assertEqual(
            new_cell.biophysical_properties.membrane_properties.channel_densities[0].id,
            "pas_chan",
        )
        self.assertNotEqual(
            new_cell.biophysical_properties.membrane_properties.channel_densities[0].id,
            "some_other_chan",
        )
        self.assertIsNone(nml_doc.validate(True))

    def test_setting_channel_density_v(self):
        """Test setting the channel_density."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        nml_doc = component_factory(
            "NeuroMLDocument", id="test_cell_with_channel_density_doc"
        )
        nml_doc.add(new_cell)

        nml_doc.add(
            "IonChannel", id="pas", conductance="10 pS", type="ionChannelPassive"
        )

        new_cell.add_channel_density_v(
            "ChannelDensity",
            nml_doc,
            "",
            id="pas_chan",
            ion_channel="pas",
            cond_density="0.021 mS_per_cm2",
            erev="-70.0 mV",
            segment_groups="all",
            ion="non_specific",
        )
        # check that it was added
        self.assertNotEqual(
            len(new_cell.biophysical_properties.membrane_properties.channel_densities),
            0,
        )
        self.assertEqual(
            new_cell.biophysical_properties.membrane_properties.channel_densities[0].id,
            "pas_chan",
        )
        self.assertNotEqual(
            new_cell.biophysical_properties.membrane_properties.channel_densities[0].id,
            "some_other_chan",
        )

        self.assertIsNone(nml_doc.validate(True))

    @unittest.expectedFailure
    def test_setting_channel_density_should_fail(self):
        """Test setting the channel_density."""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        nml_doc = component_factory(
            "NeuroMLDocument", id="test_cell_with_channel_density_doc"
        )
        nml_doc.add(new_cell)

        ion_chan = nml_doc.add(
            "IonChannel", id="pas", conductance="10 pS", type="ionChannelPassive"
        )

        new_cell.add_channel_density(
            nml_doc,
            "pas_chan",
            "NOT A NUMBER",
            "pas",
            "",
            "-70.0 mV",
            "non_specific",
            group_id="all",
        )
        self.assertIsNone(new_cell.validate(True))
        self.assertIsNone(nml_doc.validate(True))

    def test_setting_membrane_property(self):
        """Test adding a new membrane property"""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        new_cell.add_membrane_property("InitMembPotential", value="-65mV")

        self.assertEqual(
            new_cell.biophysical_properties.membrane_properties.init_memb_potentials[
                0
            ].value,
            "-65mV",
        )

        self.assertIsNone(new_cell.validate(True))

    def test_setting_intracellular_property(self):
        """Test adding a new membrane property"""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        new_cell.add_segment(
            (0, 0, 0, 20),
            (20, 0, 0, 20),
            name="soma",
            group_id="soma_group",
            seg_type="soma",
        )
        new_cell.add_intracellular_property(
            "Resistivity",
            value="0ohm_cm",
        )

        self.assertEqual(
            new_cell.biophysical_properties.intracellular_properties.resistivities[
                0
            ].value,
            "0ohm_cm",
        )

        self.assertIsNone(new_cell.validate(True))

    def test_simple_cell(self):
        "Test a simple cell."
        # test with component_factory
        cell = component_factory("Cell", id="simple_cell")
        cell.set_spike_thresh("40mV")
        cell.set_init_memb_potential("-70mV")
        cell.set_specific_capacitance("1 uF_per_cm2")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 10.0
        soma_0 = cell.add_segment(
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 10.0, 0.0, diam],
            name="Seg0_soma_0",
            group_id="soma_0",
            seg_type="soma",
        )

        self.assertIsInstance(soma_0, neuroml.Segment)

        self.assertIsNone(cell.validate(True))

    def test_complex_cell(self):
        """Test a complex cell."""
        # with component_factory
        cell = component_factory("Cell", id="complex_cell")  # type: neuroml.Cell
        cell.set_spike_thresh("40mV")
        cell.set_init_memb_potential("-70mV")
        cell.set_specific_capacitance("1 uF_per_cm2")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 30.0
        soma_0 = cell.add_segment(
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 20.0, 0.0, diam],
            name="Seg0_soma_0",
            group_id="soma_0",
            seg_type="soma",
        )
        self.assertIsInstance(soma_0, neuroml.Segment)

        dend_0 = cell.add_segment(
            prox=[soma_0.distal.x, soma_0.distal.y, soma_0.distal.z, 5],
            dist=[soma_0.distal.x, soma_0.distal.y + 50, soma_0.distal.z, 2],
            name="dend_0",
            group_id="dend_0",
            parent=soma_0,
            seg_type="soma",
        )
        self.assertIsInstance(dend_0, neuroml.Segment)

        self.assertIsNone(cell.validate(True))

    def test_component_factory_create_cell(self):
        """Test cell creation"""
        new_cell = component_factory("Cell", id="test_cell")
        new_cell.set_spike_thresh("40mV")
        new_cell.set_init_memb_potential("-70mV")
        new_cell.set_specific_capacitance("1 uF_per_cm2")
        self.assertIsInstance(new_cell, neuroml.Cell)

        # cell does not have segments: is invalid NeuroML
        with self.assertRaises(ValueError):
            new_cell.validate(True)

    def test_add_unbranched_segments(self):
        "Test add_unbranced_segments"
        # test with component_factory
        cell = component_factory("Cell", id="simple_cell")
        cell.set_spike_thresh("40mV")
        cell.set_init_memb_potential("-70mV")
        cell.set_specific_capacitance("1 uF_per_cm2")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 10.0
        soma_0 = cell.add_segment(
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 10.0, 0.0, diam],
            name="Seg0_soma_0",
            group_id="soma_0",
            seg_type="soma",
        )

        dend_group = cell.add_unbranched_segments(
            points=[
                [0.0, 10.0, 0.0, diam],
                [0.0, 20.0, 0.0, diam],
                [0.0, 30.0, 0.0, diam],
            ],
            parent=soma_0,
            fraction_along=1.0,
            group_id="dend_group_0",
            use_convention=True,
            seg_type="dendrite",
        )

        self.assertIsInstance(dend_group, neuroml.SegmentGroup)

        self.assertIsNone(cell.validate(True))
        self.assertEqual(3, len(cell.morphology.segments))

        cell.summary()

    def test_optimise_segment_group(self):
        """Test `optimise_segment_group`"""
        cell = component_factory("Cell", id="simple_cell")  # type: neuroml.Cell
        cell.set_spike_thresh("40mV")
        cell.set_init_memb_potential("-70mV")
        cell.set_specific_capacitance("1 uF_per_cm2")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 10.0
        soma_0 = cell.add_segment(
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 10.0, 0.0, diam],
            name="Seg0_soma_0",
            group_id="soma_0",
            seg_type="soma",
        )

        # add the segment again to all group
        cell.get_segment_group("all").members.append(
            cell.component_factory(
                neuroml.Member,
                segments=cell.get_segment_group("soma_0").members[0].segments,
            )
        )

        # add group to all, explicitly
        cell.get_segment_group("all").add(
            neuroml.Include, segment_groups="soma_0", force=True
        )
        cell.get_segment_group("all").add(
            neuroml.Include, segment_groups="soma_0", force=True
        )
        cell.get_segment_group("all").add(
            neuroml.Include, segment_groups="soma_0", force=True
        )
        self.assertEqual(4, len(cell.get_segment_group("all").includes))
        # should have only one included segment group
        # should have no segments, because the segment is included in the one
        # segment group already
        cell.optimise_segment_group("all")
        self.assertEqual(1, len(cell.get_segment_group("all").includes))

    def test_create_unbranched_segment_group_branches(self):
        "Test create_unbranched_segment_group_branches"
        cell = component_factory("Cell", id="simple_cell")  # type: neuroml.Cell
        cell.set_spike_thresh("40mV")
        cell.set_init_memb_potential("-70mV")
        cell.set_specific_capacitance("1 uF_per_cm2")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 10.0
        soma_0 = cell.add_segment(
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 10.0, 0.0, diam],
            name="Seg0_soma_0",
            group_id="soma_0",
            seg_type="soma",
        )

        # create two unbranched segment group
        dend_group = cell.add_unbranched_segments(
            points=[
                [0.0, 10.0, 0.0, diam],
                [0.0, 20.0, 0.0, diam],
                [0.0, 30.0, 0.0, diam],
            ],
            parent=soma_0,
            fraction_along=1.0,
            group_id="dend_group_0",
            use_convention=True,
            seg_type="dendrite",
        )
        dend_group_1 = cell.add_unbranched_segments(
            points=[
                [0.0, 10.0, 0.0, diam],
                [0.0, 20.0, 5.0, diam],
                [0.0, 30.0, 5.0, diam],
            ],
            parent=soma_0,
            fraction_along=1.0,
            group_id="dend_group_1",
            use_convention=True,
            seg_type="dendrite",
        )
        cell.optimise_segment_groups()

        self.assertIsNone(cell.validate(True))
        self.assertEqual(5, len(cell.morphology.segments))
        # all, dend_group_1, dend_group_0, soma_0, and dendrite_group,
        # soma_group
        self.assertEqual(6, len(cell.morphology.segment_groups))
        print("initial")
        for g in cell.morphology.segment_groups:
            print(g)
            print([x.segments for x in g.members])

        # remove the two unbranched groups
        cell.morphology.segment_groups.remove(cell.get_segment_group("soma_0"))
        cell.morphology.segment_groups.remove(dend_group)
        cell.morphology.segment_groups.remove(dend_group_1)
        print("after removal")
        for g in cell.morphology.segment_groups:
            print(g)
            print([x.segments for x in g.members])

        # create the unbranched segments
        cell.create_unbranched_segment_group_branches(soma_0.id)
        print("after re-creation")
        for g in cell.morphology.segment_groups:
            print(g)
            print([x.segments for x in g.members])

    def test_morphinfo(self):
        """Test the morphinfo method"""
        # with component_factory
        cell = component_factory("Cell", id="complex_cell")  # type: neuroml.Cell
        cell.set_spike_thresh("40mV")
        cell.set_init_memb_potential("-70mV")
        cell.set_specific_capacitance("1 uF_per_cm2")
        cell.notes = "NeuroML cell created by CellBuilder"

        # Add soma segment
        diam = 30.0
        soma_0 = cell.add_segment(
            prox=[0.0, 0.0, 0.0, diam],
            dist=[0.0, 20.0, 0.0, diam],
            name="Seg0_soma_0",
            group_id="soma_0",
            seg_type="soma",
        )
        self.assertIsInstance(soma_0, neuroml.Segment)

        dend_0 = cell.add_segment(
            prox=[soma_0.distal.x, soma_0.distal.y, soma_0.distal.z, 5],
            dist=[soma_0.distal.x, soma_0.distal.y + 50, soma_0.distal.z, 2],
            name="dend_0",
            group_id="dend_0",
            parent=soma_0,
            seg_type="soma",
        )

        cell.morphinfo(True)
        cell.biophysinfo()

    def test_class_hierarchy(self):
        """Test the class hierarchy getter and printer"""
        hier = neuroml.Cell.get_class_hierarchy()
        self.assertIsNotNone(hier)
        print()
        print_hierarchy(hier)

        hier = neuroml.Morphology.get_class_hierarchy()
        self.assertIsNotNone(hier)
        print()
        print(hier)
        print()
        print_hierarchy(hier)


if __name__ == "__main__":
    ta = TestNML()

    ta.test_add_segment()
