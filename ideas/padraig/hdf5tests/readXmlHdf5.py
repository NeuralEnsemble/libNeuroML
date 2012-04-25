# -*- coding: utf-8 -*-
"""
Initial version of Python API for NeuroML2
Author: Padraig Gleeson
"""

from neuroml import *
import h5py
import numpy

class MorphologyH5(object):
    
    _point_dtype = numpy.dtype([('x', 'f'), ('y', 'f'), ('z', 'f'), ('diameter', 'f')])

    _str_type = h5py.new_vlen(str)
    _my_dtype = numpy.dtype([('id', 'i'), ('name', _str_type), ('parent', 'i'), ('distal_point', 'i')])


    def __init__(self, id):
        self.id = id
        f = h5py.File('%s.hdf'%id, 'w')
        f.attrs['neurohdf_version'] = '0.1'
        f.attrs['id'] = id

        self._morphology = f.create_group("morphology")

    def __getattr__(self, name):
        print "MorphologyH5 asked for attr: %s"%name
        
        if name is "segments":
            print "Asked for my %i segments"%self._segment_dataset.shape[0]
            segments = []
            for i in range(self._segment_dataset.shape[0]):
                print "Creating object for %s: "%str(self._segment_dataset[i][0])
                seg = SegmentH5(self._segment_dataset[i][0], self)
                segments.append(seg)
            return segments
        else:
            return None

    def __get_segment_name__(self, id):
        '''print "Asking for name of seg %i: %s"%(id, self.segment_dataset[id][1])'''
        return self._segment_dataset[id][1]

    def __get_segment_parent__(self, id):
        return self._segment_dataset[id][2]

    def __get_segment_distal_point__(self, id):
        return self._segment_dataset[id][3]


    def __get_point_x__(self, index):
        return self._point_dataset[index][0]
    def __get_point_y__(self, index):
        return self._point_dataset[index][1]
    def __get_point_z__(self, index):
        return self._point_dataset[index][2]
    def __get_point_diameter__(self, index):
        return self._point_dataset[index][3]


class SegmentH5(object):

    def __init__(self, id, morphology):
        self.id = id
        self._morphology = morphology
        self._distal = DistalH5(morphology, id)

    def __getattr__(self, name):
        print "SegmentH5 %i asked for SegmentH5: %s"% (self.id,name)
        if name is "name":
            return self._morphology.__get_segment_name__(self.id)
        if name is "parent":
            return self._morphology.__get_segment_parent__(self.id)
        if name is "distal":
            return self._distal
        else:
            return None

    def __str__(self):
        return "Segment: %i (%s), parent: %s"%(self.id, self.name, self.parent)

    

class DistalH5():

    def __init__(self, morphology, segment_id):
        self._morphology = morphology
        self._segment_id = segment_id
        self._distal_point = morphology.__get_segment_distal_point__(segment_id)


    def __getattr__(self, name):
        print "DistalH5 asked for SegmentH5: %s"% (name)
        if name is "x":
            return self._morphology.__get_point_x__(self._distal_point)
        if name is "y":
            return self._morphology.__get_point_y__(self._distal_point)
        if name is "z":
            return self._morphology.__get_point_z__(self._distal_point)
        if name is "diameter":
            return self._morphology.__get_point_diameter__(self._distal_point)
        else:
            return None




def getTestMorph(id, size):
    morph = MorphologyH5(id)

    morph._point_dataset = morph._morphology.create_dataset(  "points",   [size], morph._point_dtype, compression='gzip', compression_opts=4)
    morph._segment_dataset = morph._morphology.create_dataset("segments", [size], morph._my_dtype,    compression='gzip', compression_opts=4)

    for i in range(0,size):

        morph._point_dataset[i] = (i*0.1,i*0.2,i*0.3,3)
        morph._segment_dataset[i] = (i, "seg_%i"%i, i-1, i)


    print morph._point_dataset
    print morph._segment_dataset
    return morph


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
    

    morph = getTestMorph("MyTestMorph", 5)

    print "Created morphology: %s"%morph.id
    for seg in morph.segments:
        dist = seg.distal
        print "Distal: "+str(dist.x)
        print "  Segment %s (%s) from (???) to (%f, %f, %f)"%(seg.id,
                                                         (seg.name if seg.name is not None else "??"),
                                                         dist.x,
                                                         dist.y,
                                                         dist.z)
    
