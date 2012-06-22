
#############   Some imports

# package from ../ideas/padraig/generatedFromV2Schema/
from neuroml2 import NeuroMLReader
from neuroml2.v2 import Cell
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


#############  Define populations


#############  Define inputs


#############  Define which variables to record


#############  Connect populations


#############  Run simulation

# NOTE: not running simulation, just saving NeuroML to file..
new_nml_doc = NeuroMLDocument(id="MyNet")
new_nml_doc.add_cell(ca1_cell)
new_nml_doc.add_ionChannel(naf_chan)
new_nml_doc.add_ionChannel(kdr_chan)
new_nml_doc.add_ionChannel(leak_chan)

new_nml_file = "MyNet.xml"
new_nml_doc.write_neuroml(new_nml_file)

validate_nml2(new_nml_file)
