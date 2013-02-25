# -*- coding: utf-8 -*-
"""
Initial version of Python API for NeuroML2
Author: Padraig Gleeson
"""

from neuroml2 import *


if __name__ == "__main__":


    reader = NeuroMLReader()

    filename = "../../../testFiles/CA1.nml"

    print "Reading in NeuroML 2 file: "+ filename

    nml2Doc = reader.read_neuroml(filename)


    print "Read in cells in v2 file with Id: "+nml2Doc.id

    cell = nml2Doc.cell[0]

    morph = cell.morphology

    segments = morph.segment  # not segments, this is a limitation of the code that generateDS.py creates...

    print "Id of cell: %s, which has %i segments"%(cell.id,len(segments))

    import h5py
    import numpy
    f = h5py.File('ca1.hdf', 'w')
    f.attrs['neurohdf_version'] = '0.1'


    neuroml = f.create_group("neuroml")

    neuroml.attrs["id"] = nml2Doc.id

    cell1 = neuroml.create_group("cell__"+cell.id)
    cell1.attrs["id"] = cell.id

    point_dtype = numpy.dtype([('x', 'f'), ('y', 'f'), ('z', 'f'), ('diameter', 'f')])
    point_dataset = cell1.create_dataset("points", [len(segments)], point_dtype, compression='gzip', compression_opts=4)
    
    str_type = h5py.new_vlen(str)
    my_dtype = numpy.dtype([('id', 'i'), ('name', str_type), ('parent', 'i'), ('distal_point', 'i')])

    segment_dataset = cell1.create_dataset("segments", [len(segments)], my_dtype, compression='gzip', compression_opts=4)

    i=0
    for seg in segments:
        dist = seg.distal
        prox = seg.proximal

        parent_id = int(seg.parent.segment) if seg.parent is not None else -1
        point_dataset[i] = (dist.x, dist.y, dist.z, dist.diameter)
        segment_dataset[i] = (int(seg.id), seg.name, parent_id, i)
        i +=1
    
    f.close()