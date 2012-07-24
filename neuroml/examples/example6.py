"""
Loading an abstract cell - example with izhikevichCell

The neuroml element loaded is in this format:

<izhikevichCell id="izBurst" v0 = "-70mV" thresh = "30mV" a ="0.02" b = "0.2" c = "-50.0" d = "2" Iamp="15" Idel="22ms" Idur="2000ms"/>


"""

import neuroml.loaders as loaders
import os

filepath = '../../testFiles/NML2_AbstractCells_2.nml'

doc=loaders.NeuroMLLoader.load_neuroml(filepath)
izhikevich_cells = doc.izhikevich_cells

#All the elements are now accessible.. specification of dynamics is
#the LEMS spec
for cell in izhikevich_cells:
    print 'Cell ID: '+str(cell.id)
    print 'a: '+str(cell.a)
    print 'b: '+str(cell.b)
    print 'Current duration: '+str(cell.Idur)
    print '\n'
