# -*- coding: utf-8 -*-
"""
Initial version of Python API for NeuroML2
Author: Padraig Gleeson
"""

from neuroml import *


if __name__ == "__main__":


    reader = NeuroMLReader()

    filename = "../../../testFiles/NML2_FullCell.nml"

    print "Reading in NeuroML 2 file: "+ filename

    nml2Doc = reader.readNeuroML(filename)


    print "Read in cells in v2 file with Id: "+nml2Doc.getId()

    cell = nml2Doc.getCell()[0]

    morph = cell.getMorphology()

    segments = morph.getSegment()  # not getSegments...


    print "Id of cell: %s, which has %i segments"%(cell.getId(),len(segments))


    for seg in segments:
        dist = seg.getDistal()
        prox = seg.getProximal()

        # There should of course be a helper function for this...
        if prox is None:
            parent = int(seg.getParent().getSegment())
            for segP in segments:
                if int(segP.getId()) == parent:
                    prox = segP.getDistal()

        print "  Segment %s (%s) from (%f, %f, %f) to (%f, %f, %f)"%(seg.getId(),
                                                         (seg.getName() if seg.getName() is not None else "??"),
                                                         prox.x,
                                                         prox.y,
                                                         prox.z,
                                                         dist.x,
                                                         dist.y,
                                                         dist.z)
    

    
