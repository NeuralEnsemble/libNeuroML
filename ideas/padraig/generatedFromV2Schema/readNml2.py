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

    nml2Doc = reader.read_neuroml(filename)


    print "Read in cells in v2 file with Id: "+nml2Doc.id

    cell = nml2Doc.cell[0]

    morph = cell.morphology

    segments = morph.segment  # not segments, this is a limitation of the code that generateDS.py creates...


    print "Id of cell: %s, which has %i segments"%(cell.id,len(segments))

    for seg in segments:
        dist = seg.distal
        prox = seg.proximal

        # There should of course be a helper function for this...
        if prox is None:
            parent = int(seg.parent.segment)
            for segP in segments:
                if int(segP.id) == parent:
                    prox = segP.distal

        print "  Segment %s (%s) from (%f, %f, %f) to (%f, %f, %f)"%(seg.id,
                                                         (seg.name if seg.name is not None else "??"),
                                                         prox.x,
                                                         prox.y,
                                                         prox.z,
                                                         dist.x,
                                                         dist.y,
                                                         dist.z)
    

    
