#############   Some imports

from neuron import h

if '7.' in h.nrnversion(0):
    import neuron.gui # To not freeze the GUI


#############  Load the morphology


neuromlFile = '../testFiles/Purk2M9s_v1x.nml'

h.load_file('celbild.hoc')
cb = h.CellBuild(0)
cb.manage.neuroml(neuromlFile)
cb.continuous = 1
cb.cexport()

print "Loaded NeuroML from: " + neuromlFile

#############  Load the ion channels


#############  Define cell types (templates)


#############  Define populations


#############  Define inputs


#############  Define which variables to record


#############  Connect populations


#############  Run simulation