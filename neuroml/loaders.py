# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull, Michael Vella
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

import numpy as np
from nml.nml import parse as nmlparse

class NeuroMLLoader(object):

    @classmethod
    def load(cls,src):
        doc = cls.__nml2_doc(src)
        return doc

    @classmethod    
    def __nml2_doc(cls,src):
        import sys

        try:
            nml2_doc = nmlparse(src)
        except Exception:
            print("Not a valid NeuroML 2 doc: %s" % str(sys.exc_info())) 
            return None    
        return nml2_doc

    

#class NeuroMLDocument(object):
#    def __init__(self,cells=None,morphologies=None,networks=None,
#                 ion_channels=None,synapses=None,extracellular_properties=None,
#                 izhikevich_cells=None):
#
#        self.cells = cells
#        self.morphologies = morphologies
#        self.networks = networks
#        self.ion_channels = ion_channels
#        self.synapses = synapses
#        self.extracellular_properties = extracellular_properties
#        self.izhikevich_cells = izhikevich_cells

#class NeuroMLLoader(object):
#
#    @classmethod
#    def __nml2_doc(cls,src):
#        import sys
#        import neuroml.v2
#
#        try:
#            nml2_doc = neuroml.v2.parse(src)
#        except Exception:
#            print("Not a valid NeuroML 2 doc: %s" % str(sys.exc_info())) 
#            return None    
#        return nml2_doc
#    
#    @classmethod
#    def __load_vertices(cls,segments):
#        index=0
#        id_to_index={}#dict for a neuroml segment ID gives the index in the vertex,connectivity etc arrays of the proximal node of that segment
#        id_to_fraction_along = {}
#        id_to_parent_id = {}
#        vertices = []
#        for seg in segments:
#            seg_id = int(seg.id)
#            id_to_index[seg_id] = index
#            dist = seg.distal
#            prox = seg.proximal
#            parent = seg.parent
#
#            if parent != None:
#                id_to_fraction_along[seg_id] = float(parent.fractionAlong)
#                id_to_parent_id[seg_id] = int(parent.segment)
#            else:
#                id_to_fraction_along[seg_id] = 1.0
#                id_to_parent_id[seg_id] = None
#
#            #probably better ways to do this:
#            if prox is None:
#                for segP in segments:
#                    if int(segP.id) == int(parent.segment):
#                        prox = segP.distal
#                    
#            vertices.append([prox.x,prox.y,prox.z,prox.diameter])
#            vertices.append([dist.x,dist.y,dist.z,dist.diameter])
#
#            index+=2
#        return vertices,id_to_index,id_to_fraction_along,id_to_parent_id
#
#
#    @classmethod
#    def __connectivity(cls,id_to_index,id_to_fraction_along,vertices,id_to_parent_id):
#    
#        connectivity = np.zeros(len(id_to_index)*2)
#        fractions_along = np.zeros(len(id_to_index)*2)
#        
#        for i in id_to_index:
#            proximal_index=id_to_index[i]
#            distal_index = proximal_index + 1
#            fraction_along=id_to_fraction_along[i]
#            parent_id=id_to_parent_id[i]
#            if parent_id != None:
#                parent_proximal_index = id_to_index[parent_id]
#                parent_distal_index = id_to_index[parent_id]+1
#            else:
#                parent_distal_index = -1
#                parent_proximal_index = None
#
#            assert fraction_along == None or (fraction_along >= 0.0 and fraction_along <= 1.0), "fraction along outside (1U0) bounds"
#
#            connectivity[proximal_index] = parent_distal_index
#            connectivity[distal_index] = proximal_index
#
#            fractions_along[distal_index] = fraction_along
#            fractions_along[proximal_index] = None
#        return connectivity, fractions_along
#
#    @classmethod
#    def load_neuroml(cls,src):
#
#        """
#        This code is highly experimental - also a lot of it needs to be
#        broken down into helper functions
#        This code is still mainly a proof of principle - work in progress,
#        mapping from the segment-based space of neuroML to the node-based
#        space of libNeuroML is the main conceptual difficulty..
#        
#        Also, I'm not sure how LEMS compatible it is since eg izhikevich_cells
#        is being hard-coded but this shouldn't be strictly necessary if the user
#        can define their own abstract cell types.
#        """
#
#        nml2_doc=cls.__nml2_doc(src)
#        try:
#            cells_array=[]
#            for cell in nml2_doc.cell:
#                print('Loading cell..')
#                morph = cell.morphology
#                segments = morph.segment  # not segments, limitation of the code that generateDS.py creates...
#                vertices,id_to_index,id_to_fraction_along,id_to_parent_id = cls.__load_vertices(segments)
#                connectivity,fractions_along = cls.__connectivity(id_to_index,id_to_fraction_along,vertices,
#                                                                 id_to_parent_id)
#                physical_mask=np.tile([1,0],len(connectivity)/2) #Is this always valid?
#                morph_array = Backend(vertices,connectivity,fractions_along=fractions_along,
#                                              physical_mask=physical_mask)
#                segment_group=ml.SegmentGroup(morph_array)
#                ml_cell=ml.Cell(segment_group)
#                cells_array.append(ml_cell)
#
#        except:
#            pass
#
#        try:
#            izhikevich_cell_array = []
#            for izhikevich_cell in nml2_doc.izhikevichCell:
#                print('Loading izhikevich cell..')
#                izhikevich_cell_array.append(izhikevich_cell)
#        except:
#            pass
#
#        return NeuroMLDocument(cells=cells_array,
#                               izhikevich_cells=izhikevich_cell_array)

class SWCLoader(object):
    
    @classmethod
    def load_swc_single(cls,  src, name=None):
      
        dtype= {'names':   ('id', 'type', 'x','y','z','r','pid'),
                'formats': ('int32', 'int32', 'f4','f4','f4','f4','int32') }
        
        d = np.loadtxt(src,dtype=dtype )
        
        if len( np.nonzero( d['pid']==-1)) != 1:
            assert False, "Unexpected number of id's of -1 in file" 
            
        num_nodes=len(d['pid'])

        root_index=np.where(d['pid']==-1)[0][0]
 
        # We might not nessesarily have continuous indices in the 
        # SWC file, so lets convert them:
        index_to_id = d['id']
        id_to_index_dict = dict( [(id,index) for index,id in enumerate(index_to_id) ] )

        if len(id_to_index_dict) != len(index_to_id):
            s =  "Internal Error Loading SWC: Index and ID map are different lengths."
            s += " [ID:%d, Index:%d]"%( len(index_to_id), len(id_to_index_dict) )
            raise MorphologyImportError(s)
        
        # Vertices and section types are easy:
        vertices =  d[ ['x','y','z','r'] ]
        vertices =  np.vstack( [d['x'], d['y'],d['z'],d['r'] ]).T
        section_types = [ swctype for ID,swctype in d[['id','type']]]

        #for connection indices we want the root to have index -1:
        connection_indices=np.zeros(num_nodes,dtype='int32')
        for i in range(num_nodes):
            pID=d['pid'][i]
            if pID !=-1:
                parent_index=id_to_index_dict[pID]
                connection_indices[i]=parent_index
            else:
                connection_indices[i]=-1

        #This needs to become a SegmentGroup
        return Backend(vertices=vertices, 
                              connectivity=connection_indices, 
                              name=name )
