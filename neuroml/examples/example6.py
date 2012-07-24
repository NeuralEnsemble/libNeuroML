"""
Loading an abstract cell - example with izhikevichCell

the neuroml element which we are going to load is this:

<izhikevichCell id="izBurst" v0 = "-70mV" thresh = "30mV" a ="0.02" b = "0.2" c = "-50.0" d = "2" Iamp="15" Idel="22ms" Idur="2000ms"/>


"""

import neuroml.loaders as loaders
import os

filepath = '../../testFiles/NML2_AbstractCells.nml'

doc=loaders.NeuroMLLoader.load_neuroml(filepath)
izhikevich_cell = doc.izhikevich_cells[0]

#All the elements are accessible..:
print izhikevich_cell.a
print izhikevich_cell.b
print izhikevich_cell.Idur
