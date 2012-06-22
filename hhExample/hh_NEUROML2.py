'''

Generates the network with the NeuroML 2 API & saves as XML

Uses Python package in ../ideas/padraig/generatedFromV2Schema/

'''

#############   Some imports

from neuroml2 import NeuroMLReader
from neuroml2.v2 import Cell, BiophysicalProperties, MembraneProperties, ChannelDensity
from neuroml2.v2 import Morphology, Segment, Point3DWithDiam, SegmentParent, SegmentGroup, Member
from neuroml2.v2 import Population, Network, PulseGenerator, ExplicitInput, StpMechanism, StpSynapse, SynapticConnection
from neuroml2.v2.NeuroMLDocument import NeuroMLDocument, validate_nml2

# To save structure of model
model = NeuroMLDocument(id="NML2Network")


#############  Load the morphology

reader = NeuroMLReader()

filename = "../testFiles/Purk2M9s.nml"
nml2_doc = reader.read_neuroml(filename)
original_cell = nml2_doc.cell[0]
purkinje_morph = original_cell.morphology
print "Read in morphology with %i segments" % len(purkinje_morph.segment)


#############  Load the ion channels

nml2_doc = reader.read_neuroml("../testFiles/NaF.nml")
naf_chan = nml2_doc.ionChannel[0]
model.add_ionChannel(naf_chan)

nml2_doc = reader.read_neuroml("../testFiles/Kdr.nml")
kdr_chan = nml2_doc.ionChannel[0]
model.add_ionChannel(kdr_chan)

nml2_doc = reader.read_neuroml("../testFiles/Leak.nml")
leak_chan = nml2_doc.ionChannel[0]
model.add_ionChannel(leak_chan)


#############  Define cell types (templates)

# ... declarative style
purkinje_cell = Cell(id="PurkCell")
purkinje_cell.morphology = purkinje_morph

purkinje_cell.biophysicalProperties = BiophysicalProperties(id="biophys_"+purkinje_cell.id)
membProp = MembraneProperties()
purkinje_cell.biophysicalProperties.membraneProperties = membProp

membProp.add_channelDensity(ChannelDensity("nafChans", ionChannel=naf_chan.id, segmentGroup="all", condDensity="120.0 mS_per_cm2"))
membProp.add_channelDensity(ChannelDensity("kdrChans", ionChannel=kdr_chan.id, segmentGroup="all", condDensity="36 mS_per_cm2"))
membProp.add_channelDensity(ChannelDensity("leakChans", ionChannel=leak_chan.id, segmentGroup="all", condDensity="3 mS_per_cm2"))

model.add_cell(purkinje_cell)

# ... imperative style
granule_cell = Cell(id="GranCell")
granule_cell.morphology = Morphology(id="morph_"+granule_cell.id)

gc_soma = Segment(id="0", name="soma", proximal=Point3DWithDiam(0,0,0,10), distal=Point3DWithDiam(0,10,0,10))
granule_cell.morphology.add_segment(gc_soma)
gc_dend = Segment(id="1", name="dend", proximal=Point3DWithDiam(0,10,0,2), distal=Point3DWithDiam(0,30,0,2), parent=SegmentParent(segment=gc_soma.id))
granule_cell.morphology.add_segment(gc_dend)

soma_group = SegmentGroup("soma_group")
soma_group.add_member(Member(segment=gc_soma.id))
granule_cell.morphology.add_segmentGroup(soma_group)

dend_group = SegmentGroup("dend_group")
dend_group.add_member(Member(segment=gc_dend.id))
granule_cell.morphology.add_segmentGroup(dend_group)

granule_cell.biophysicalProperties = BiophysicalProperties(id="biophys_"+granule_cell.id)
membProp = MembraneProperties()
granule_cell.biophysicalProperties.membraneProperties = membProp

membProp.add_channelDensity(ChannelDensity("nafChans", ionChannel=naf_chan.id, segmentGroup="all", condDensity="120.0 mS_per_cm2"))
membProp.add_channelDensity(ChannelDensity("kdrChans", ionChannel=kdr_chan.id, segmentGroup="all", condDensity="36 mS_per_cm2"))
membProp.add_channelDensity(ChannelDensity("leakChans", ionChannel=leak_chan.id, segmentGroup="all", condDensity="3 mS_per_cm2"))


model.add_cell(granule_cell)

#############  Define populations

net = Network(id="FullNetwork")

purkinje_pop = Population(id="purkinje_cells", cell=purkinje_cell.id, size="100")
net.add_population(purkinje_pop)

granule_pop = Population(id="granule_cells", cell=granule_cell.id, size="1000")
net.add_population(granule_pop)

model.add_network(net)

#############  Define inputs

pulseGen = PulseGenerator(id="pg1", delay="100ms", duration="100ms", amplitude="1nA")
model.add_pulseGenerator(pulseGen)

# Only one input!!
net.add_explicitInput(ExplicitInput(target="%s[%i]"%(granule_pop.id,0), input=pulseGen.id))


#############  Define which variables to record

# No recording in NeuroML, wait for SED-ML...

#############  Connect populations

# Define synapse

stpMechanism = StpMechanism(initReleaseProb="0.5", tauFac="0 ms", tauRec="120 ms")
stpSynapse = StpSynapse(id="stpSynDep", gbase="1nS", erev="0mV", tauRise="0.1ms", tauDecay="2ms", stpMechanism=stpMechanism)
model.add_stpSynapse(stpSynapse)

# Only one connection!!
net.add_synapticConnection(SynapticConnection(fromxx="%s[%i]"%(granule_pop.id,0), \
                                              to="%s[%i]"%(purkinje_pop.id,0), \
                                              synapse=stpSynapse.id))



#############  Run simulation

# NOTE: not running simulation, just saving NeuroML to file..


new_nml_file = model.id+".xml"
model.write_neuroml(new_nml_file)

validate_nml2(new_nml_file)
