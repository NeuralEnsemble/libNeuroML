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

r"""
Prototype for object model backend for the libNeuroML project

AUTHORS:

- Mike Vella: initial version
- Mike Hull - Large parts of MorphologyArray and SWCLoader
"""

import numpy as np

class MorphologyBase(object):
    def __init__():
        raise NotImplementedError

class MorphologyArray(MorphologyBase):
    """Provides the array-based object model backend.

    Provides the core arrays -
    vertices,connectivity and section_types. Unlike in
    Morphforge these are all the same length so that corresponding
    sections have the same index in each array.
    
    example::
    vertices[3] and connectivity[3] refer to the vertex and
    connectivity of the same section.

    The root section must be at index 0 and by convention
    has connectivity==0.

    -connectivity array::
    The connectivity array is a list of indices pointing to which
    other element an element is connected. So for instance,
    connectivity[3] is an integer with the index of the section
    it refers to in the MorphologyArray

    -note on Sections::
    a Section class is provided (see further down) however this
    does not result in a tree-based object model. Rather, the section
    objects manipulate the MorphologyArray backend in a way that 
    is invisible to the user. The user may still use the 
    MorphologyArray class, depending on their needs.

    MorphologyArray[i] returns the Section object relating to
    element i

    Because sections exist in memory independently of the,
    MorphologyArray, a MorphologyArray must keep a register
    of all the sections which handle its elements. These
    are updated when their information changes via a MorphologyArray
    operation such as the indices changing when a connection
    to a new MorphologyArray is made and indices all change.
    """

    def __init__(self,vertices,connectivity,section_types=None,
                name=None):

        self._connectivity=np.array(connectivity)
        self._vertices=np.array(vertices)
        self.name=name

        if section_types:
            self._section_types=np.array(section_types)
        else:
            self._section_types=np.zeros(len(connectivity),
                                        dtype='int32')

        #validity test:
        M=self._vertices.shape[0]
        N=self._connectivity.shape[0]
        P=self._section_types.shape[0]
        assert N==M==P,'Invalid morphology'

        #morphology needs to know which sections are exist in memory
        #then if something like connecting to another morphology
        #happens, the indices etc get updated, there may be a better
        #way of doing this
        self._registered_sections=[]

        self.root_index=np.where(self._connectivity==-1)[0][0]

    @property
    def vertices(self):
        return self._vertices

    @property
    def connectivity(self):
        return self._connectivity

    @property
    def section_types(self):
        return self._section_types

    @property
    def root_section(self):
        index=self.root_index
        return self[index]

    def register_section(self,section):
        #keep a register of section objects which are in memory and which
        #morphology they relate to
        #this could be improved, perhaps by using an index:section dict?
        self._registered_sections=np.append(self._registered_sections,section)
        section.morphology=self

    def pop_section(self,sid):
        raise NotImplementedError

    def parent_id(self,index):
        """
        Return the parent index for the given index
        """
        return self._connectivity[index]

    def vertex(self,index):
        """
        Return vertex corresponding to index in morphology
        """
        return self.vertices[index]

    def delete(self):
        #haven't figured out the best way to do this yet
        #this doesn't work:
        del(self)
    
    def adopt(self,child_morphology,parent_index):
        """
        Connect another morphology to this one.

        A lot of this can essentially be done via simple matrix 
        algebra.       
        """

        #root of one (index=0) needs to connect to
        #section we are connecting to
        num_parent_sections=len(self._connectivity)
        new_connectivity=child_morphology.connectivity
        new_connectivity+=num_parent_sections
        new_connectivity[0]=parent_index#point root to its new parent
        self._connectivity=np.append(self._connectivity,
                                    new_connectivity,axis=0)
        self._section_types=np.append(self._section_types,
                                    child_morphology.section_types,axis=0)
        #treat the parent section as the origin of 
        #the new root and translate the array, 
        #there is probably a cleaner way to do this using numpy

        xyz0=np.array(self.vertices[parent_index])
        xyz0[3]=0
        new_vertices=child_morphology.vertices+xyz0
        self._vertices=np.append(self._vertices,new_vertices,axis=0)

        #register the sections to the new morphology
        for section in child_morphology._registered_sections:
            section.index+=num_parent_sections
            self.register_section(section)

        #delete the old morphology, still not implemented properly
        child_morphology.delete()

    def __getitem__(self,i):
        #create a section object:
        sec=Section(vertex=[self.vertices[i]])
        #register the section:
        sec.index=i
        self.register_section(sec)
        return sec

  
class Section():
    """
    The idea of the Section class is to provide a user with a natural
    way of manipulating compartments while still utilising an array-
    based backend. The user does not have to use Section objects,
    it is provided in particular for users who create models 
    with a small number of compartments.

    A section can be instantiated independently of a morphology, however
    such a section genernates its own morphology when it is instantiated.

        A=Section()
        B=Section()

    Will create two morphology objects and two section objects
    call the morphology objects A_morph and B_morph
    
    When A.connect(B) is executed, the pattern is

    child.connect(parent). hence A now becomes part of the
    B_morph object and the A_morph object is destroyed (actually
    as of 22/5/12 the morphology destruction isn't implemented, but
    this should be easy enough to do).

    The idea of this "hidden" complexity is that it 
    combines the power of a more natural object-oriented 
    way of manipulating small numbers of compartments with an
    array-based backend.

    There is still a lot to do here, as I add complexity, 
    I can add other features like the direction in which 
    a section extends, right now it is designed such that 
    it extends only in x which is of course incorrect, 
    a unit vector parameter would be a nice feature.

    Additionally, things like which side (distal or proximal)
    of the section is being connected to have still not been
    implemented.
    """

    def __init__(self,vertex=None,radius=50.0,length=10.0):

        self._index=0

        if vertex==None:
            self._radius=radius
            self._length=length
            self.vertex=[[self._length,0.0,0.0,self._radius]]
        else:
            self.vertex=vertex

        #make the morphology and register this section to it
        connectivity=np.array([-1],dtype='int32')
        self._morphology=MorphologyArray(vertices=self.vertex,
                                        connectivity=connectivity)
        self._morphology.register_section(self)

    @property
    def length(self):
        return self._length

    @property
    def radius(self):
        return self._radius

    @property
    def index(self):
        return self._index

    @property
    def vertex(self):
        return self.morphology.vertex(self.index)

    @property
    def parent_id(self):
        return self.morphology.parent_id(self.index)

    @property
    def morphology(self):
        return self._morphology

    @property
    def is_root(self):
        """
        Returns True if section is root
        """
        return self.parent_id==-1

    def adopt(self,child):
        """
        Connect a child to this section
        """

        child_morphology=child.morphology
    
        assert child.is_root, 'child must be root of its morphology'

        child_index=child.index
        self.morphology.adopt(child_morphology=child.morphology,
                            parent_index=self.index)
                                
        #delete the old morpholoy:
        child.morphology.delete()

    def connect(self,parent):
        """
        connect this section to a new parent

        This is done by connecting the child morphology 
        to the parent morphology and delting the child morphology
        """
        
        parent_morphology=parent.morphology

        assert self.is_root, 'section must be root to connect'

        parent_index=parent.index
        #connect the morphologies to each other:
        parent_morphology.adopt(child_morphology=self.morphology,
                                 parent_index=parent_index)

        #delete the old morpholoy:
        self._morphology.delete()

        #the parent morphology is now the child morphology:
        self._morphology=parent.morphology
