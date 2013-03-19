#!/usr/bin/env python

#
# Generated Tue Mar 19 21:36:46 2013 by generateDS.py version 2.8b.
#

import sys

import ??? as supermod

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = range(3)
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError(
                        "Failed to import ElementTree from any known place")

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#

class AnnotationSub(supermod.Annotation):
    def __init__(self, anytypeobjs_=None):
        super(AnnotationSub, self).__init__(anytypeobjs_, )
supermod.Annotation.subclass = AnnotationSub
# end class AnnotationSub


class ComponentTypeSub(supermod.ComponentType):
    def __init__(self, extends=None, name=None, description=None, anytypeobjs_=None):
        super(ComponentTypeSub, self).__init__(extends, name, description, anytypeobjs_, )
supermod.ComponentType.subclass = ComponentTypeSub
# end class ComponentTypeSub


class IncludeTypeSub(supermod.IncludeType):
    def __init__(self, href=None, valueOf_=None, mixedclass_=None, content_=None):
        super(IncludeTypeSub, self).__init__(href, valueOf_, mixedclass_, content_, )
supermod.IncludeType.subclass = IncludeTypeSub
# end class IncludeTypeSub


class Q10SettingsSub(supermod.Q10Settings):
    def __init__(self, fixed_q10=None, experimental_temp=None, type=None, q10_factor=None):
        super(Q10SettingsSub, self).__init__(fixed_q10, experimental_temp, type, q10_factor, )
supermod.Q10Settings.subclass = Q10SettingsSub
# end class Q10SettingsSub


class HHRateSub(supermod.HHRate):
    def __init__(self, midpoint=None, rate=None, scale=None, type=None):
        super(HHRateSub, self).__init__(midpoint, rate, scale, type, )
supermod.HHRate.subclass = HHRateSub
# end class HHRateSub


class HHVariableSub(supermod.HHVariable):
    def __init__(self, midpoint=None, rate=None, scale=None, type=None):
        super(HHVariableSub, self).__init__(midpoint, rate, scale, type, )
supermod.HHVariable.subclass = HHVariableSub
# end class HHVariableSub


class HHTimeSub(supermod.HHTime):
    def __init__(self, midpoint=None, rate=None, scale=None, type=None, tau=None):
        super(HHTimeSub, self).__init__(midpoint, rate, scale, type, tau, )
supermod.HHTime.subclass = HHTimeSub
# end class HHTimeSub


class VoltageConcDepBlockSub(supermod.VoltageConcDepBlock):
    def __init__(self, block_concentration=None, scaling_conc=None, type=None, species=None, scaling_volt=None):
        super(VoltageConcDepBlockSub, self).__init__(block_concentration, scaling_conc, type, species, scaling_volt, )
supermod.VoltageConcDepBlock.subclass = VoltageConcDepBlockSub
# end class VoltageConcDepBlockSub


class StpMechanismSub(supermod.StpMechanism):
    def __init__(self, tau_rec=None, tau_fac=None, init_release_prob=None):
        super(StpMechanismSub, self).__init__(tau_rec, tau_fac, init_release_prob, )
supermod.StpMechanism.subclass = StpMechanismSub
# end class StpMechanismSub


class SegmentParentSub(supermod.SegmentParent):
    def __init__(self, fraction_along='1', segments=None):
        super(SegmentParentSub, self).__init__(fraction_along, segments, )
supermod.SegmentParent.subclass = SegmentParentSub
# end class SegmentParentSub


class Point3DWithDiamSub(supermod.Point3DWithDiam):
    def __init__(self, y=None, x=None, z=None, diameter=None):
        super(Point3DWithDiamSub, self).__init__(y, x, z, diameter, )
supermod.Point3DWithDiam.subclass = Point3DWithDiamSub
# end class Point3DWithDiamSub


class ProximalDetailsSub(supermod.ProximalDetails):
    def __init__(self, translation_start=None):
        super(ProximalDetailsSub, self).__init__(translation_start, )
supermod.ProximalDetails.subclass = ProximalDetailsSub
# end class ProximalDetailsSub


class DistalDetailsSub(supermod.DistalDetails):
    def __init__(self, normalization_end=None):
        super(DistalDetailsSub, self).__init__(normalization_end, )
supermod.DistalDetails.subclass = DistalDetailsSub
# end class DistalDetailsSub


class MemberSub(supermod.Member):
    def __init__(self, segments=None):
        super(MemberSub, self).__init__(segments, )
supermod.Member.subclass = MemberSub
# end class MemberSub


class IncludeSub(supermod.Include):
    def __init__(self, segment_groups=None):
        super(IncludeSub, self).__init__(segment_groups, )
supermod.Include.subclass = IncludeSub
# end class IncludeSub


class PathSub(supermod.Path):
    def __init__(self, fromxx=None, to=None):
        super(PathSub, self).__init__(fromxx, to, )
supermod.Path.subclass = PathSub
# end class PathSub


class SubTreeSub(supermod.SubTree):
    def __init__(self, fromxx=None, to=None):
        super(SubTreeSub, self).__init__(fromxx, to, )
supermod.SubTree.subclass = SubTreeSub
# end class SubTreeSub


class SegmentEndPointSub(supermod.SegmentEndPoint):
    def __init__(self, segments=None):
        super(SegmentEndPointSub, self).__init__(segments, )
supermod.SegmentEndPoint.subclass = SegmentEndPointSub
# end class SegmentEndPointSub


class MembranePropertiesSub(supermod.MembraneProperties):
    def __init__(self, channel_population=None, channel_density=None, spike_thresh=None, specific_capacitance=None, init_memb_potential=None, reversal_potential=None):
        super(MembranePropertiesSub, self).__init__(channel_population, channel_density, spike_thresh, specific_capacitance, init_memb_potential, reversal_potential, )
supermod.MembraneProperties.subclass = MembranePropertiesSub
# end class MembranePropertiesSub


class ValueAcrossSegOrSegGroupSub(supermod.ValueAcrossSegOrSegGroup):
    def __init__(self, segments=None, segment_groups='all', value=None, extensiontype_=None):
        super(ValueAcrossSegOrSegGroupSub, self).__init__(segments, segment_groups, value, extensiontype_, )
supermod.ValueAcrossSegOrSegGroup.subclass = ValueAcrossSegOrSegGroupSub
# end class ValueAcrossSegOrSegGroupSub


class VariableParameterSub(supermod.VariableParameter):
    def __init__(self, segment_groups=None, parameter=None, inhomogeneous_value=None):
        super(VariableParameterSub, self).__init__(segment_groups, parameter, inhomogeneous_value, )
supermod.VariableParameter.subclass = VariableParameterSub
# end class VariableParameterSub


class InhomogeneousValueSub(supermod.InhomogeneousValue):
    def __init__(self, inhomogeneous_param=None, value=None):
        super(InhomogeneousValueSub, self).__init__(inhomogeneous_param, value, )
supermod.InhomogeneousValue.subclass = InhomogeneousValueSub
# end class InhomogeneousValueSub


class ReversalPotentialSub(supermod.ReversalPotential):
    def __init__(self, segments=None, segment_groups='all', value=None, species=None):
        super(ReversalPotentialSub, self).__init__(segments, segment_groups, value, species, )
supermod.ReversalPotential.subclass = ReversalPotentialSub
# end class ReversalPotentialSub


class SpeciesSub(supermod.Species):
    def __init__(self, segments=None, segment_groups='all', value=None, ion=None, initial_ext_concentration=None, concentration_model=None, id=None, initial_concentration=None):
        super(SpeciesSub, self).__init__(segments, segment_groups, value, ion, initial_ext_concentration, concentration_model, id, initial_concentration, )
supermod.Species.subclass = SpeciesSub
# end class SpeciesSub


class IntracellularPropertiesSub(supermod.IntracellularProperties):
    def __init__(self, species=None, resistivity=None):
        super(IntracellularPropertiesSub, self).__init__(species, resistivity, )
supermod.IntracellularProperties.subclass = IntracellularPropertiesSub
# end class IntracellularPropertiesSub


class ExtracellularPropertiesLocalSub(supermod.ExtracellularPropertiesLocal):
    def __init__(self, temperature=None, species=None):
        super(ExtracellularPropertiesLocalSub, self).__init__(temperature, species, )
supermod.ExtracellularPropertiesLocal.subclass = ExtracellularPropertiesLocalSub
# end class ExtracellularPropertiesLocalSub


class SpaceStructureSub(supermod.SpaceStructure):
    def __init__(self, y_spacing=None, z_start=0, y_start=0, z_spacing=None, x_start=0, x_spacing=None):
        super(SpaceStructureSub, self).__init__(y_spacing, z_start, y_start, z_spacing, x_start, x_spacing, )
supermod.SpaceStructure.subclass = SpaceStructureSub
# end class SpaceStructureSub


class LayoutSub(supermod.Layout):
    def __init__(self, space=None, random=None, grid=None, unstructured=None):
        super(LayoutSub, self).__init__(space, random, grid, unstructured, )
supermod.Layout.subclass = LayoutSub
# end class LayoutSub


class UnstructuredLayoutSub(supermod.UnstructuredLayout):
    def __init__(self, number=None):
        super(UnstructuredLayoutSub, self).__init__(number, )
supermod.UnstructuredLayout.subclass = UnstructuredLayoutSub
# end class UnstructuredLayoutSub


class RandomLayoutSub(supermod.RandomLayout):
    def __init__(self, region=None, number=None):
        super(RandomLayoutSub, self).__init__(region, number, )
supermod.RandomLayout.subclass = RandomLayoutSub
# end class RandomLayoutSub


class GridLayoutSub(supermod.GridLayout):
    def __init__(self, z_size=None, y_size=None, x_size=None):
        super(GridLayoutSub, self).__init__(z_size, y_size, x_size, )
supermod.GridLayout.subclass = GridLayoutSub
# end class GridLayoutSub


class InstanceSub(supermod.Instance):
    def __init__(self, i=None, k=None, j=None, id=None, location=None):
        super(InstanceSub, self).__init__(i, k, j, id, location, )
supermod.Instance.subclass = InstanceSub
# end class InstanceSub


class LocationSub(supermod.Location):
    def __init__(self, y=None, x=None, z=None):
        super(LocationSub, self).__init__(y, x, z, )
supermod.Location.subclass = LocationSub
# end class LocationSub


class SynapticConnectionSub(supermod.SynapticConnection):
    def __init__(self, to=None, synapse=None, fromxx=None):
        super(SynapticConnectionSub, self).__init__(to, synapse, fromxx, )
supermod.SynapticConnection.subclass = SynapticConnectionSub
# end class SynapticConnectionSub


class ConnectionSub(supermod.Connection):
    def __init__(self, post_cell_id=None, id=None, pre_cell_id=None):
        super(ConnectionSub, self).__init__(post_cell_id, id, pre_cell_id, )
supermod.Connection.subclass = ConnectionSub
# end class ConnectionSub


class ExplicitInputSub(supermod.ExplicitInput):
    def __init__(self, input=None, destination=None, target=None):
        super(ExplicitInputSub, self).__init__(input, destination, target, )
supermod.ExplicitInput.subclass = ExplicitInputSub
# end class ExplicitInputSub


class InputSub(supermod.Input):
    def __init__(self, destination=None, id=None, target=None):
        super(InputSub, self).__init__(destination, id, target, )
supermod.Input.subclass = InputSub
# end class InputSub


class BaseSub(supermod.Base):
    def __init__(self, id=None, neuro_lex_id=None, extensiontype_=None):
        super(BaseSub, self).__init__(id, neuro_lex_id, extensiontype_, )
supermod.Base.subclass = BaseSub
# end class BaseSub


class StandaloneSub(supermod.Standalone):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, extensiontype_=None):
        super(StandaloneSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, extensiontype_, )
supermod.Standalone.subclass = StandaloneSub
# end class StandaloneSub


class InputListSub(supermod.InputList):
    def __init__(self, id=None, neuro_lex_id=None, component=None, population=None, input=None):
        super(InputListSub, self).__init__(id, neuro_lex_id, component, population, input, )
supermod.InputList.subclass = InputListSub
# end class InputListSub


class ProjectionSub(supermod.Projection):
    def __init__(self, id=None, neuro_lex_id=None, postsynaptic_population=None, presynaptic_population=None, synapse=None, connection=None):
        super(ProjectionSub, self).__init__(id, neuro_lex_id, postsynaptic_population, presynaptic_population, synapse, connection, )
supermod.Projection.subclass = ProjectionSub
# end class ProjectionSub


class CellSetSub(supermod.CellSet):
    def __init__(self, id=None, neuro_lex_id=None, select=None, anytypeobjs_=None):
        super(CellSetSub, self).__init__(id, neuro_lex_id, select, anytypeobjs_, )
supermod.CellSet.subclass = CellSetSub
# end class CellSetSub


class PopulationSub(supermod.Population):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, extracellular_properties=None, network=None, component=None, cells=None, type=None, size=None, layout=None, instance=None):
        super(PopulationSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, extracellular_properties, network, component, cells, type, size, layout, instance, )
supermod.Population.subclass = PopulationSub
# end class PopulationSub


class RegionSub(supermod.Region):
    def __init__(self, id=None, neuro_lex_id=None, space=None, anytypeobjs_=None):
        super(RegionSub, self).__init__(id, neuro_lex_id, space, anytypeobjs_, )
supermod.Region.subclass = RegionSub
# end class RegionSub


class SpaceSub(supermod.Space):
    def __init__(self, id=None, neuro_lex_id=None, based_on=None, structure=None):
        super(SpaceSub, self).__init__(id, neuro_lex_id, based_on, structure, )
supermod.Space.subclass = SpaceSub
# end class SpaceSub


class NetworkSub(supermod.Network):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, space=None, region=None, extracellular_properties=None, population=None, cell_set=None, synaptic_connection=None, projection=None, explicit_input=None, input_list=None):
        super(NetworkSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, space, region, extracellular_properties, population, cell_set, synaptic_connection, projection, explicit_input, input_list, )
supermod.Network.subclass = NetworkSub
# end class NetworkSub


class PulseGeneratorSub(supermod.PulseGenerator):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, delay=None, duration=None, amplitude=None):
        super(PulseGeneratorSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, delay, duration, amplitude, )
supermod.PulseGenerator.subclass = PulseGeneratorSub
# end class PulseGeneratorSub


class ReactionSchemeSub(supermod.ReactionScheme):
    def __init__(self, id=None, neuro_lex_id=None, source=None, type=None, anytypeobjs_=None):
        super(ReactionSchemeSub, self).__init__(id, neuro_lex_id, source, type, anytypeobjs_, )
supermod.ReactionScheme.subclass = ReactionSchemeSub
# end class ReactionSchemeSub


class ExtracellularPropertiesSub(supermod.ExtracellularProperties):
    def __init__(self, id=None, neuro_lex_id=None, temperature=None, species=None):
        super(ExtracellularPropertiesSub, self).__init__(id, neuro_lex_id, temperature, species, )
supermod.ExtracellularProperties.subclass = ExtracellularPropertiesSub
# end class ExtracellularPropertiesSub


class ChannelDensitySub(supermod.ChannelDensity):
    def __init__(self, id=None, neuro_lex_id=None, segment_groups='all', ion=None, ion_channel=None, erev=None, cond_density=None, segments=None, variable_parameter=None):
        super(ChannelDensitySub, self).__init__(id, neuro_lex_id, segment_groups, ion, ion_channel, erev, cond_density, segments, variable_parameter, )
supermod.ChannelDensity.subclass = ChannelDensitySub
# end class ChannelDensitySub


class ChannelPopulationSub(supermod.ChannelPopulation):
    def __init__(self, id=None, neuro_lex_id=None, segment_groups='all', ion=None, number=None, ion_channel=None, erev=None, segments=None, variable_parameter=None):
        super(ChannelPopulationSub, self).__init__(id, neuro_lex_id, segment_groups, ion, number, ion_channel, erev, segments, variable_parameter, )
supermod.ChannelPopulation.subclass = ChannelPopulationSub
# end class ChannelPopulationSub


class BiophysicalPropertiesSub(supermod.BiophysicalProperties):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, membrane_properties=None, intracellular_properties=None, extracellular_properties=None):
        super(BiophysicalPropertiesSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, membrane_properties, intracellular_properties, extracellular_properties, )
supermod.BiophysicalProperties.subclass = BiophysicalPropertiesSub
# end class BiophysicalPropertiesSub


class InhomogeneousParamSub(supermod.InhomogeneousParam):
    def __init__(self, id=None, neuro_lex_id=None, variable=None, metric=None, proximal=None, distal=None):
        super(InhomogeneousParamSub, self).__init__(id, neuro_lex_id, variable, metric, proximal, distal, )
supermod.InhomogeneousParam.subclass = InhomogeneousParamSub
# end class InhomogeneousParamSub


class SegmentGroupSub(supermod.SegmentGroup):
    def __init__(self, id=None, neuro_lex_id=None, member=None, include=None, path=None, sub_tree=None, inhomogeneous_param=None):
        super(SegmentGroupSub, self).__init__(id, neuro_lex_id, member, include, path, sub_tree, inhomogeneous_param, )
supermod.SegmentGroup.subclass = SegmentGroupSub
# end class SegmentGroupSub


class SegmentSub(supermod.Segment):
    def __init__(self, id=None, neuro_lex_id=None, name=None, parent=None, proximal=None, distal=None):
        super(SegmentSub, self).__init__(id, neuro_lex_id, name, parent, proximal, distal, )
supermod.Segment.subclass = SegmentSub
# end class SegmentSub


class MorphologySub(supermod.Morphology):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, segments=None, segment_groups=None):
        super(MorphologySub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, segments, segment_groups, )
supermod.Morphology.subclass = MorphologySub
# end class MorphologySub


class AbstractCellSub(supermod.AbstractCell):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, extensiontype_=None):
        super(AbstractCellSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, extensiontype_, )
supermod.AbstractCell.subclass = AbstractCellSub
# end class AbstractCellSub


class ConductanceBasedSynapseSub(supermod.ConductanceBasedSynapse):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, erev=None, gbase=None, extensiontype_=None):
        super(ConductanceBasedSynapseSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, erev, gbase, extensiontype_, )
supermod.ConductanceBasedSynapse.subclass = ConductanceBasedSynapseSub
# end class ConductanceBasedSynapseSub


class DecayingPoolConcentrationModelSub(supermod.DecayingPoolConcentrationModel):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, ion=None, shell_thickness=None, resting_conc=None, decay_constant=None, extensiontype_=None):
        super(DecayingPoolConcentrationModelSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, ion, shell_thickness, resting_conc, decay_constant, extensiontype_, )
supermod.DecayingPoolConcentrationModel.subclass = DecayingPoolConcentrationModelSub
# end class DecayingPoolConcentrationModelSub


class GateHHTauInfSub(supermod.GateHHTauInf):
    def __init__(self, id=None, neuro_lex_id=None, instances=1, type=None, notes=None, q10_settings=None, time_course=None, steady_state=None):
        super(GateHHTauInfSub, self).__init__(id, neuro_lex_id, instances, type, notes, q10_settings, time_course, steady_state, )
supermod.GateHHTauInf.subclass = GateHHTauInfSub
# end class GateHHTauInfSub


class GateHHRatesSub(supermod.GateHHRates):
    def __init__(self, id=None, neuro_lex_id=None, instances=1, type=None, notes=None, q10_settings=None, forward_rate=None, reverse_rate=None):
        super(GateHHRatesSub, self).__init__(id, neuro_lex_id, instances, type, notes, q10_settings, forward_rate, reverse_rate, )
supermod.GateHHRates.subclass = GateHHRatesSub
# end class GateHHRatesSub


class IonChannelSub(supermod.IonChannel):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, conductance=None, type=None, species=None, gate=None, gate_h_hrates=None, gate_h_htau_inf=None):
        super(IonChannelSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, conductance, type, species, gate, gate_h_hrates, gate_h_htau_inf, )
supermod.IonChannel.subclass = IonChannelSub
# end class IonChannelSub


class NeuroMLDocumentSub(supermod.NeuroMLDocument):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, include=None, extracellular_properties=None, intracellular_properties=None, morphology=None, ion_channel=None, decaying_pool_concentration_model=None, exp_one_synapse=None, exp_two_synapse=None, nmda_synapse=None, stp_synapse=None, biophysical_properties=None, cells=None, abstract_cell=None, iaf_tau_cell=None, iaf_cell=None, izhikevich_cell=None, ad_ex_ia_f_cell=None, pulse_generator=None, network=None, ComponentType=None):
        super(NeuroMLDocumentSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, include, extracellular_properties, intracellular_properties, morphology, ion_channel, decaying_pool_concentration_model, exp_one_synapse, exp_two_synapse, nmda_synapse, stp_synapse, biophysical_properties, cells, abstract_cell, iaf_tau_cell, iaf_cell, izhikevich_cell, ad_ex_ia_f_cell, pulse_generator, network, ComponentType, )
supermod.NeuroMLDocument.subclass = NeuroMLDocumentSub
# end class NeuroMLDocumentSub


class ConcentrationModel_DSub(supermod.ConcentrationModel_D):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, ion=None, shell_thickness=None, resting_conc=None, decay_constant=None, type=None):
        super(ConcentrationModel_DSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, ion, shell_thickness, resting_conc, decay_constant, type, )
supermod.ConcentrationModel_D.subclass = ConcentrationModel_DSub
# end class ConcentrationModel_DSub


class CellSub(supermod.Cell):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, biophysical_properties_attr=None, morphology_attr=None, morphology=None, biophysical_properties=None):
        super(CellSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, biophysical_properties_attr, morphology_attr, morphology, biophysical_properties, )
supermod.Cell.subclass = CellSub
# end class CellSub


class AdExIaFCellSub(supermod.AdExIaFCell):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, reset=None, EL=None, C=None, b=None, VT=None, del_t=None, a=None, thresh=None, g_l=None, tauw=None):
        super(AdExIaFCellSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, reset, EL, C, b, VT, del_t, a, thresh, g_l, tauw, )
supermod.AdExIaFCell.subclass = AdExIaFCellSub
# end class AdExIaFCellSub


class IzhikevichCellSub(supermod.IzhikevichCell):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, a=None, c=None, b=None, d=None, v0=None, thresh=None):
        super(IzhikevichCellSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, a, c, b, d, v0, thresh, )
supermod.IzhikevichCell.subclass = IzhikevichCellSub
# end class IzhikevichCellSub


class IaFCellSub(supermod.IaFCell):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, reset=None, C=None, thresh=None, leak_conductance=None, leak_reversal=None):
        super(IaFCellSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, reset, C, thresh, leak_conductance, leak_reversal, )
supermod.IaFCell.subclass = IaFCellSub
# end class IaFCellSub


class IaFTauCellSub(supermod.IaFTauCell):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, reset=None, tau=None, thresh=None, leak_reversal=None):
        super(IaFTauCellSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, reset, tau, thresh, leak_reversal, )
supermod.IaFTauCell.subclass = IaFTauCellSub
# end class IaFTauCellSub


class ExpTwoSynapseSub(supermod.ExpTwoSynapse):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, erev=None, gbase=None, tau_decay=None, tau_rise=None, extensiontype_=None):
        super(ExpTwoSynapseSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, erev, gbase, tau_decay, tau_rise, extensiontype_, )
supermod.ExpTwoSynapse.subclass = ExpTwoSynapseSub
# end class ExpTwoSynapseSub


class ExpOneSynapseSub(supermod.ExpOneSynapse):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, erev=None, gbase=None, tau_decay=None):
        super(ExpOneSynapseSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, erev, gbase, tau_decay, )
supermod.ExpOneSynapse.subclass = ExpOneSynapseSub
# end class ExpOneSynapseSub


class StpSynapseSub(supermod.StpSynapse):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, erev=None, gbase=None, tau_decay=None, tau_rise=None, stp_mechanism=None):
        super(StpSynapseSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, erev, gbase, tau_decay, tau_rise, stp_mechanism, )
supermod.StpSynapse.subclass = StpSynapseSub
# end class StpSynapseSub


class NmdaSynapseSub(supermod.NmdaSynapse):
    def __init__(self, id=None, neuro_lex_id=None, name=None, metaid=None, notes=None, annotation=None, erev=None, gbase=None, tau_decay=None, tau_rise=None, voltage_conc_dep_block=None):
        super(NmdaSynapseSub, self).__init__(id, neuro_lex_id, name, metaid, notes, annotation, erev, gbase, tau_decay, tau_rise, voltage_conc_dep_block, )
supermod.NmdaSynapse.subclass = NmdaSynapseSub
# end class NmdaSynapseSub



def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Annotation'
        rootClass = supermod.Annotation
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='',
        pretty_print=True)
    doc = None
    return rootObj


def parseString(inString):
    from StringIO import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Annotation'
        rootClass = supermod.Annotation
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
    return rootObj


def parseLiteral(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Annotation'
        rootClass = supermod.Annotation
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from ??? import *\n\n')
    sys.stdout.write('import ??? as model_\n\n')
    sys.stdout.write('rootObj = model_.Annotation(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="Annotation")
    sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


