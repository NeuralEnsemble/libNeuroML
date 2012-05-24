# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull, Michael Vella
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are meet:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

"""
After a discussion with Mike Hull I've decided to make 
a signifcant change whereby nodes and sections have different
meaning in important ways. Node has vertex
and diam information as well as an index.

Node can also be able to have some self constructing 
properties?
"""

r"""
Prototype for object model backend for the libNeuroML project

AUTHORS:

- Mike Vella: initial version
- Mike Hull - Large parts of MorphologyArray and SWCLoader
"""

import math
import numpy as np

class MorphologyArray(object):
    """Provides the array-based object model backend.

    Provides the core arrays -
    vertices,connectivity and node_types. Unlike in
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

    -note on Nodes::
    a Node class is provided (see further down) however this
    does not result in a tree-based object model. Rather, the section
    objects manipulate the MorphologyArray backend in a way that 
    is invisible to the user. The user may still use the 
    MorphologyArray class, depending on their needs.

    MorphologyArray[i] returns the Node object relating to
    element i

    Because sections exist in memory independently of the,
    MorphologyArray, a MorphologyArray must keep a register
    of all the sections which handle its elements. These
    are updated when their information changes via a MorphologyArray
    operation such as the indices changing when a connection
    to a new MorphologyArray is made and indices all change.
    """

    def __init__(self,vertices,connectivity,node_types=None,
                name=None):

        self.connectivity=np.array(connectivity)
        self.vertices=np.array(vertices)
        self.name=name

        if node_types:
            self.node_types=np.array(node_types)
        else:
            self.node_types=np.zeros(len(connectivity),
                                        dtype='int32')

        #validity test:
        M=self.vertices.shape[0]
        N=self.connectivity.shape[0]
        P=self.node_types.shape[0]
        assert N==M==P,'Invalid morphology'

        #morphology needs to know which sections are exist in memory
        #then if something like connecting to another morphology
        #happens, the indices etc get updated, there may be a better
        #way of doing this
        self._registered_nodes=[]

    @property
    def root_index(self):
        return np.where(self.connectivity==-1)[0][0]    
    
    @property
    def root_node(self):
        index=self.root_index
        return self[index]

    def register_node(self,node):
        #keep a register of section objects which are in memory and which
        #morphology they relate to
        #this could be improved, perhaps by using an index:section dict?
        self._registered_nodes=np.append(self._registered_nodes,node)
        node.morphology=self

    def pop_section(self,sid):
        raise NotImplementedError

    def parent_id(self,index):
        """
        Return the parent index for the given index
        """
        return self.connectivity[index]

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
        num_parent_sections=len(self.connectivity)
        new_connectivity=child_morphology.connectivity
        new_connectivity+=num_parent_sections
        new_connectivity[0]=parent_index#point root to its new parent
        self.connectivity=np.append(self.connectivity,
                                    new_connectivity,axis=0)
        self.node_types=np.append(self.node_types,
                                    child_morphology.node_types,axis=0)
        #treat the parent section as the origin of 
        #the new root and translate the array, 
        #there is probably a cleaner way to do this using numpy

        xyz0=np.array(self.vertices[parent_index])
        xyz0[3]=0
        new_vertices=child_morphology.vertices+xyz0
        self.vertices=np.append(self.vertices,new_vertices,axis=0)

        #register the sections to the new morphology
        #this is being done ina clumsy way..
        for section in child_morphology._registered_nodes:
            section.index+=num_parent_sections
            self.register_node(section)

        #delete the old morphology, still not implemented properly
        child_morphology.delete()

    def __getitem__(self,i):
        #create a node object:
        node=Node(vertex=[self.vertices[i]])
        #register the node:
        node.index=i
        self.register_node(node)
        return node


class Node():
    """
    The idea of the Node class is to provide a user with a natural
    way of manipulating compartments while still utilising an array-
    based backend. The user does not have to use Node objects,
    it is provided in particular for users who create models 
    with a small number of compartments.

    A section can be instantiated independently of a morphology, however
    such a section genernates its own morphology when it is instantiated.

        A=Node()
        B=Node()

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

    def __init__(self,vertex,node_type=None):

        self.index=0
        self.vertex=vertex
        self.node_type=node_type

        #make the morphology and register this section to it
        connectivity=np.array([-1],dtype='int32')
        self.morphology=MorphologyArray(vertices=[self.vertex],
                                        connectivity=connectivity,
                                        node_types=node_type)

        self.morphology.register_node(self)

    @property
    def x(self):
        return self.vertex[0]

    @property
    def y(self):
        return self.vertex[1]

    @property
    def z(self):
        return self.vertex[2]

    @property
    def radius(self):
        return self.vertex[4]

    @property
    def vertex(self):
        return self.morphology.vertex(self.index)

    @property
    def parent_id(self):
        return self.morphology.parent_id(self.index)

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
        self.morphology.delete()

        #the parent morphology is now the child morpholoy
        self.morphology=parent.morphology

class Section(object):

    """
    In the process of implementing NEURON-like sections.

    These will also have their own connect() etc methods
    but will be more complicated than nodes as they
    have distal and proximal components.
    """

    def __init__(self,length=100,r1=10,r2=None,
                 section_type=None,name=None):

        if r2==None:r2=r1
        
        self.section_type=section_type
        self.name=name

        #create the vertices

        vertex1=np.array([0.0,0.0,0.0,r1])
        vertex2=np.array([0.0,0.0,length,r2])

        #create the morphology by connecting two nodes #
        #together

        self.node1=Node(vertex1,node_type=section_type)
        self.node2=Node(vertex2,node_type=section_type)
        self.node2.connect(self.node1)
    
    @property
    def r1(self):
        return self.node1.radius

    @property
    def r2(self):
        return self.node1.radius

    @property
    def length(self):
        displacement=self.node1.vertex-self.node2.vertex        
        return math.sqrt(sum(displacement**2))
    
    @length.setter
    def length(self,value):
        raise NotImplementedError

    @property
    def morphology(self):
        #need to stop user from being able to set length etc
        return self.node2.morphology

    @property
    def slant_height(self):
        r=self.r1
        R=self.r2
        
        s=math.sqrt((r-R)**2+self.length**2)
        return s

    @property
    def lateral_area(self):
        lsa=math.pi*(self.r1+self.r2)*self.slant_height
        return lsa

    @property
    def total_area(self):
        lsa=self.lateral_area
        end_areas=math.pi*(self.r1**2+self.r2**2)
        return lsa+end_areas

    @property
    def volume(self):
        r=self.r1
        R=self.r2
        V=(math.pi*self.length/3.0)*(R**2+r**2+R*r)
        return V
