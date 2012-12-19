# -*- coding: utf-8 -*-
"""
Initial version of Python API for LEMS
Author: Padraig Gleeson
"""

from neuroml2.v2 import *
from neuroml2.v2.NeuroMLDocument import *


if __name__ == "__main__":

    #####################################################

    print "Writing NeuroML 2 file with Izhikevich cell"

    nmlDoc = NeuroMLDocument(id="IzhNet")

    izhCell = IzhikevichCell(id="izBurst", v0 = "-70mV", thresh = "30mV", a ="0.02", b = "0.2", c = "-50.0", d = "2")
    nmlDoc.add_izhikevich_cell(izhCell)

    newnmlfile = "testIzhNml2.xml"
    nmlDoc.write_neuroml(newnmlfile)

    validate_nml2beta(newnmlfile)
    ############################################################

    print "Writing NeuroML 2 file with detailed morph"

    nmlDoc = NeuroMLDocument(id="BigCell")

    cell = Cell(id="pyramidal")
    nmlDoc.add_cell(cell)

    morph = Morphology("morph")
    cell.morphology = morph


    for i in range(100):
        seg = Segment(id=i, name="seg_%i"%i)

        seg.distal = Point3DWithDiam(0, int(i*5), 0, 2)
        if i>0:
            seg.parent = SegmentParent(segment=i-1)
        else:
            seg.proximal = Point3DWithDiam(0, 0, 0, 5)

        morph.add_segment(seg)

    newnmlfile = "testCellNml2.xml"
    nmlDoc.write_neuroml(newnmlfile)

    validate_nml2beta(newnmlfile)

    ############################################################

