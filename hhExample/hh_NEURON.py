#############   Some imports

from neuron import NeuroMLReader



#############  Load the morphology

reader = NeuroMLReader()

filename = "../../../testFiles/CA1.nml"
print "Reading in NeuroML 2 file: "+ filename
nml2Doc = reader.read_neuroml(filename)
print "Read in cells in v2 file with Id: "+nml2Doc.id


#############  Load the ion channels


#############  Define cell types (templates)


#############  Define populations


#############  Define inputs


#############  Define which variables to record


#############  Connect populations


#############  Run simulation