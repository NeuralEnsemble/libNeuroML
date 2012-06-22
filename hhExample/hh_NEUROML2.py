
#############   Some imports

# package from ../ideas/padraig/generatedFromV2Schema/
from neuroml2 import NeuroMLReader
from neuroml2.v2 import Cell, BiophysicalProperties, MembraneProperties, ChannelDensity
from neuroml2.v2 import Population, Network, PulseGenerator, ExplicitInput
from neuroml2.v2.NeuroMLDocument import NeuroMLDocument, validate_nml2



#############  Load the morphology

reader = NeuroMLReader()

filename = "../testFiles/CA1.nml"
nml2_doc = reader.read_neuroml(filename)
original_cell = nml2_doc.cell[0]
ca1_morph = original_cell.morphology
print "Read in morphology with %i segments" % len(ca1_morph.segment)


#############  Load the ion channels

nml2_doc = reader.read_neuroml("../testFiles/NaF.nml")
naf_chan = nml2_doc.ionChannel[0]
nml2_doc = reader.read_neuroml("../testFiles/Kdr.nml")
kdr_chan = nml2_doc.ionChannel[0]
nml2_doc = reader.read_neuroml("../testFiles/Leak.nml")
leak_chan = nml2_doc.ionChannel[0]

#############  Define cell types (templates)

ca1_cell = Cell(id="CA1")
ca1_cell.morphology = ca1_morph

ca1_cell.biophysicalProperties = BiophysicalProperties(id="biophys_"+ca1_cell.id)
membProp = MembraneProperties()
ca1_cell.biophysicalProperties.membraneProperties = membProp

membProp.add_channelDensity(ChannelDensity("nafChans", ionChannel=naf_chan.id, segmentGroup="all", condDensity="120.0 mS_per_cm2"))
membProp.add_channelDensity(ChannelDensity("kdrChans", ionChannel=kdr_chan.id, segmentGroup="all", condDensity="36 mS_per_cm2"))
membProp.add_channelDensity(ChannelDensity("leakChans", ionChannel=leak_chan.id, segmentGroup="all", condDensity="3 mS_per_cm2"))


#############  Define populations

net = Network(id="FullNetwork")
ca1_pop = Population(id="ca1_cells", cell=ca1_cell.id, size="5")
net.add_population(ca1_pop)

#############  Define inputs

pulseGen = PulseGenerator(id="pg1", delay="100ms", duration="100ms", amplitude="1nA")

net.add_explicitInput(ExplicitInput(target="%s[%i]"%(ca1_pop.id,0), input=pulseGen.id))


#############  Define which variables to record


#############  Connect populations


#############  Run simulation

# NOTE: not running simulation, just saving NeuroML to file..
new_nml_doc = NeuroMLDocument(id=net.id)
new_nml_doc.add_cell(ca1_cell)

new_nml_doc.add_ionChannel(naf_chan)
new_nml_doc.add_ionChannel(kdr_chan)
new_nml_doc.add_ionChannel(leak_chan)

new_nml_doc.add_pulseGenerator(pulseGen)

new_nml_doc.add_network(net)

new_nml_file = net.id+".xml"
new_nml_doc.write_neuroml(new_nml_file)

validate_nml2(new_nml_file)
