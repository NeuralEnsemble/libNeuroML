# -*- coding: utf-8 -*-
"""

Reading in NeuroML from XML file, then creating HDF5 based object tree and parsing both with approx the same API...


Author: Padraig Gleeson
"""

from neuroml2 import *

if __name__ == "__main__":


    reader = NeuroMLReader()

    filename = "../../../testFiles/NML2_FullCell.nml"

    print "Reading in NeuroML 2 file: "+ filename

    nml2Doc = reader.read_neuroml(filename)

    cell = nml2Doc.cell[0]

    morph = cell.morphology

    segments = morph.segment  # not segments, this is a limitation of the code that generateDS.py creates...

    print "------------------  Parsing XML object tree  --------------------"
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


    print
    
    from NeuroMLH5 import *

    neuromlH5 = NeuroMLH5("Test1")
    cell = neuromlH5.createCell("cell1")

   
    cell.addTestMorph(5) # A helper function to quickly add a valid morphology

    print "%s; %s"%(neuromlH5, cell)
    
    morph = cell.morphology

    print "Created morphology: %s"%morph.id

    print "------------------  Parsing HDF5 object tree  --------------------"
    for seg in morph.segments:
        dist = seg.distal
        prox = seg.proximal
        
        print "  Segment %s (%s) from (%f, %f, %f) to (%f, %f, %f)"%(seg.id,
                                                         (seg.name if seg.name is not None else "??"),
                                                         prox.x,
                                                         prox.y,
                                                         prox.z,
                                                         dist.x,
                                                         dist.y,
                                                         dist.z)
    
