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
from neuroml.morphology import MorphologyArray

class NeuroMLLoader(object):

    @classmethod
    def load_neuroml(cls,src):

        """
        This code is highly experimental - also a lot of it needs to be
        broken down into helper functions
        This code is still mainly a proof of principle - work in progress,
        mapping from the segment-based space of neuroML to the node-based
        space of libNeuroML is the main conceptual difficulty..
        """
        import v2
        import sys

        try:
            nml2_doc = v2.parse(src)
            print "Read in NeuroML 2 doc with id: %s"%nml2_doc.id
        except Exception:
            print "Not a valid NeuroML 2 doc:", sys.exc_info()
            return None

        cell = nml2_doc.cell[0]
        morph = cell.morphology
        segments = morph.segment  # not segments, this is a limitation of the code that generateDS.py creates...

        print "Id of cell: %s, which has %i segments"%(cell.id,len(segments))

        num_seg=len(segments)
        vertices=[]
        connectivity=np.zeros(num_seg*2)
        physical_mask=np.zeros(num_seg*2)
        id_to_index={}#dict for a neuroml segment ID gives the index in the vertex,connectivity etc arrays of the proximal node of that segment
        id_to_fraction_along={}
        id_to_parent_id={}

        #here is how I think all the staging needs to happen:
        #1.build up the id_to_index dictionary by looping through
        #the segments, all the while inserting the vertex information
        #into the relevant index

        #1.loop through the id_to_index dict, building up the connectivity matrix
        #at this stage it will also be possible to set the physical mask

        index=0
        for seg in segments:
            index *= 2
            seg_id = int(seg.id)
            dist = seg.distal
            prox = seg.proximal
            parent = seg.parent
            id_to_index[seg_id] = index

            if parent != None:
                id_to_fraction_along[seg_id] = float(parent.fractionAlong)
                id_to_parent_id[seg_id] = int(parent.segment)
            else:
                id_to_fraction_along[seg_id] = 0.0
                id_to_parent_id[seg_id] = 0 #I think this is OK - not sure, is root segment ID always 0?

            #probably better ways to do this:
            if prox is None:
                for segP in segments:
                    if int(segP.id) == int(parent.segment):
                        prox = segP.distal
                    
            vertices.append([prox.x,prox.y,prox.z,prox.diameter])
            vertices.append([dist.x,dist.y,dist.z,dist.diameter])

        #now build the connectivity matrix:
        #need to check if the vertex is located in the correct
        #position to make the connection, otherwise need to
        #add a non-physical connection
        connectivity=np.zeros(len(id_to_index))

        for i in id_to_index:
            seg_index=id_to_index[i]
            distal_index = seg_index + 1
            proximal_index = seg_index
            fraction_along=id_to_fraction_along[i]
            parent_id=id_to_parent_id[i]
            parent_distal_index = id_to_index[parent_id+1]
            parent_distal_vertex=vertices[parent_distal_index]
            parent_proximal_index = id_to_index[parent_id]
            parent_proximal_vertex=vertices[parent_proximal_index]

            #let us assume the segment always connects from its
            #distal node and the fraction along is where along the
            #parent the connection is made

            assert fraction_along > 0.0 and fraction_along < 1.0, "fraction along outside normal fractional bounds"

            if fraction_along == None or fraction_along == 1:
                #what does this actually mean? as far as I know
                #the distal node connects to the parent segment
                #between its distal and proximal nodes at
                #fractionAlong
                connected_index=parent_distal_index
            elif fraction_along==0.0:
                connected_index=parent_proximal_index
            else:
                #using linear interpolation
                new_vertex=parent_proximal_vector[:3]-parent_distal_vector[:3]
                radius=(parent_proximal_vector[3]-parent_distal_vector[3])*fraction_along
                np.append(new_vertex,radius)
                new_vertex_index=len(vertices)
                np.append(vertices,new_vertex)

            connectivity[proximal_index] = distal_index
            connectivity[distal_index] = connected_index


            #now need to set the physical mask by looking at how many of the connections are physical
        print connectivity

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

        #This needs to become a SegmentCollection
        return MorphologyArray(vertices=vertices, 
                              connectivity=connection_indices, 
                              name=name )
