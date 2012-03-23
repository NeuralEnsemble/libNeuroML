# -*- coding: utf-8 -*-
"""
Initial version of Python API for LEMS
Author: Padraig Gleeson
"""

from neuroml.v2 import *
from neuroml.v2.NeuroMLDocument import *


if __name__ == "__main__":

    #####################################################

    print "Writing NeuroML 2 file with Izhikevich cell"

    nmlDoc = NeuroMLDocument(id="IzhNet")

    izhCell = IzhikevichCell(id="izBurst", v0 = "-70mV", thresh = "30mV", a ="0.02", b = "0.2", c = "-50.0", d = "2", Iamp="15", Idel="22ms", Idur="2000ms")
    nmlDoc.addIzhikevichCell(izhCell)

    newnmlfile = "testIzhNml2.xml"
    nmlDoc.writeNeuroML(newnmlfile)

    validateNml2(newnmlfile)

    ############################################################

    print "Writing NeuroML 2 file with detailed morph"

    nmlDoc = NeuroMLDocument(id="BigCell")

    cell = Cell(id="pyramidal")
    nmlDoc.addCell(cell)

    morph = Morphology("morph")
    cell.setMorphology(morph)


    for i in range(100):
        seg = Segment(id=i, name="seg_%i"%i)

        seg.setDistal(Point3DWithDiam(0, int(i*5), 0, 2))
        if i>0:
            seg.setParent(SegmentParent(segment=i-1))
        else:
            seg.setProximal(Point3DWithDiam(0, 0, 0, 5))

        morph.addSegment(seg)

    newnmlfile = "testCellNml2.xml"
    nmlDoc.writeNeuroML(newnmlfile)

    validateNml2(newnmlfile)

    ############################################################

