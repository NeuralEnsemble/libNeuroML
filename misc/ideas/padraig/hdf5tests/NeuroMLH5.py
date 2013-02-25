# -*- coding: utf-8 -*-
"""

A set of classes for saving a neuronal morphology as a HDF5 file, while providing an API similar to the one generated 
by generateDS.py from the NeuroML2 XML Schema

Longer term the Morphology/Segment/Distal etc. classes should be substituted into the generated API for more efficient storage of morphologies...

Author: Padraig Gleeson
"""

from neuroml2 import *
import h5py
import numpy

class NeuroMLH5(object):

    def __init__(self, id):
        self.id = id
        f = h5py.File('%s.hdf'%id, 'w')
        f.attrs['neurohdf_version'] = '0.1'
        f.attrs['id'] = id

        self._neuroml = f.create_group("neuroml")
        self.cells = []

    def __str__(self):
        return "NeuroML: %s with %i cells"%(self.id, len(self.cells))

    def createCell(self, cell_id):
        cell_group = self._neuroml.create_group("cell_%s"%cell_id)
        cell = CellH5(cell_id, cell_group)
        self.cells.append(cell)
        return cell



class CellH5(object):

    def __init__(self, id, cell):
        self.id = id
        self._cell = cell
        self.morphology = MorphologyH5("morphology_%s"%id, self)

        
    def __str__(self):
        return "Cell: %s with %i segments"%(self.id, len(self.morphology.segments))

    def addTestMorph(self, size):

        self.morphology._point_dataset = self.morphology._morphology.create_dataset(  "points",   [size+1], self.morphology._point_dtype, compression='gzip', compression_opts=4)
        self.morphology._segment_dataset = self.morphology._morphology.create_dataset("segments", [size], self.morphology._my_dtype,    compression='gzip', compression_opts=4)

        for i in range(0,size):
            if i == 0:
                self.morphology._point_dataset[0] = (0,0,0,5)

            self.morphology._point_dataset[i+1] = ((i+1)*0.1,(i+1)*0.2,(i+1)*0.3,3)
            self.morphology._segment_dataset[i] = (i, "seg_%i"%i, i-1, i+1, i)
            
        #print self.morphology._point_dataset
        #print self.morphology._segment_dataset


class MorphologyH5(object):
    
    _point_dtype = numpy.dtype([('x', 'f'), ('y', 'f'), ('z', 'f'), ('diameter', 'f')])

    _str_type = h5py.new_vlen(str)
    _my_dtype = numpy.dtype([('id', 'i'), ('name', _str_type), ('parent', 'i'), ('distal_point', 'i'), ('proximal_point', 'i')])


    def __init__(self, id, cell):
        self.id = id
        self._cell = cell

        self._morphology = cell._cell.create_group("morphology")
        self._morphology.attrs['id'] = id


    def __getattr__(self, name):
        #print "MorphologyH5 asked for attr: %s"%name
        
        if name is "segments":
            #print "Asked for my %i segments"%self._segment_dataset.shape[0]

            #TODO: this should be cached!
            segments = []
            for i in range(self._segment_dataset.shape[0]):
                #print "Creating object for %s: "%str(self._segment_dataset[i][0])
                seg = SegmentH5(self._segment_dataset[i][0], self)
                segments.append(seg)

            return segments
        else:
            return None

    def __get_segment_name__(self, id):
        return self._segment_dataset[id][1]

    def __get_segment_parent__(self, id):
        return self._segment_dataset[id][2]

    def __get_segment_distal_point__(self, id):
        return self._segment_dataset[id][3]

    def __get_segment_proximal_point__(self, id):
        return self._segment_dataset[id][4]

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
        self._proximal = ProximalH5(morphology, id)

    def __getattr__(self, name):
        #print "SegmentH5 %i asked for SegmentH5: %s"% (self.id,name)
        if name is "name":
            return self._morphology.__get_segment_name__(self.id)
        if name is "parent":
            return self._morphology.__get_segment_parent__(self.id)
        if name is "distal":
            return self._distal
        if name is "proximal":
            return self._proximal
        else:
            return None

    def __str__(self):
        return "Segment: %i (%s), parent: %s"%(self.id, self.name, self.parent)



class PointH5():

    def __init__(self, morphology, segment_id):
        self._morphology = morphology
        self._segment_id = segment_id


    def __getattr__(self, name):
        #print "DistalH5 asked for SegmentH5: %s"% (name)
        if name is "x":
            return self._morphology.__get_point_x__(self._point)
        if name is "y":
            return self._morphology.__get_point_y__(self._point)
        if name is "z":
            return self._morphology.__get_point_z__(self._point)
        if name is "diameter":
            return self._morphology.__get_point_diameter__(self._point)
        else:
            return None


class DistalH5(PointH5):

    def __init__(self, morphology, segment_id):
        self._morphology = morphology
        self._segment_id = segment_id
        self._point = morphology.__get_segment_distal_point__(segment_id)

class ProximalH5(PointH5):

    def __init__(self, morphology, segment_id):
        self._morphology = morphology
        self._segment_id = segment_id
        self._point = morphology.__get_segment_proximal_point__(segment_id)





