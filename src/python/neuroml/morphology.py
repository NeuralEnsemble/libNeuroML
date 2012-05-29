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
import weakref

class MorphologyArray(object):
    """Provides the core of the array-based object model backend.

    Provides the core arrays -
    vertices,connectivity and node_types. Unlike in
    Morphforge these are all the same length so that corresponding
    sections have the same index in each array.
    
    example::
    vertices[3] and connectivity[3] refer to the vertex and
    connectivity of the same section.

    The root section by convention has connectivity==-1.

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

        #No node objects exist in memory:
        self.__registered_components=[]

    @property
    def root_index(self):
        return np.where(self.connectivity==-1)[0][0]    
    
    @property
    def root_node(self):
        index=self.root_index
        return self[index]

    def register_component(self,node):
        """Array of references to instatiated node objects of this morphology
        
        This attribute exists so that if something like connecting to 
        another morphology happens the node object can be updated.
        """        

        self.__registered_components=np.append(self.__registered_components,node)
        node._morphology=self

    def insert(self,index,x):
        """
        Inserts a node between a node and its parent at
        x between them. Where x ranges from 0 to 1, 0 being
        the location of the child and 1 the location of the
        parent.

        ..TO-DO: vertex of new node needs to be calculated through
        linear interpolation.
        """

        assert index !=0, 'Cannot insert on root node - It has no parent'

        parent_id=self.parent_id(index)
        parent_node=self[parent_id]        
        #TO DO - calculate the vertex from the parent and child and x, 
        new_node=Node()
        old_node=self[index]
        new_node.connect(parent_node)
        old_node.parent_id=new_node.index

    def children(self,index):
        """Returns an array with indexes of children"""
        return np.where(self.connectivity==index)

    def pop(self,index):
        """
        Deletes a node from the MorphologyArray, its children become
        children of the deleted node's parent.
        """    

        self.vertices=np.delete(self.vertices,index)
        self.node_types=np.delete(self.node_types,index)
        self.connectivity=np.delete(self.connectivity,index)

        #TO DO:
        #there is a more efficient way to implement this using np.where(self.connectivity>=index)
        k=0
        for i in self.connectivity:
            print k
            if i>=index:
                self.connectivity[k]=i-1
            k+=1
        pass

    def to_root(self,index):
        """
        Changes the connectivity matrix
        so that the node at index becomes the root
        """

        old_root_index=self.root_index
        new_root_index=index        
        #do a tree traversal:
        parent_index=self.connectivity[index]
        grandparent_index=self.connectivity[parent_index]
        while index!=old_root_index:
            self.connectivity[parent_index]=index
            index=parent_index
            parent_index=grandparent_index
            grandparent_index=self.connectivity[parent_index]
        self.connectivity[new_root_index]=-1

    def adopt(self,child_morphology,parent_index):
        """
        Connect another morphology to this one.
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

        #register the nodes to the new morphology
        #this is being done ina clumsy way..
        for section in child_morphology.__registered_components:
            section.index+=num_parent_sections
            self.register_component(section)

    def parent_id(self,index):
        """Return the parent index for the given index"""
        return self.connectivity[index]

    def vertex(self,index):
        """Return vertex corresponding to index in morphology"""
        return self.vertices[index]

    def __getitem__(self,i):
        node=Node(vertex=[self.vertices[i]],node_type=self.node_types [i])
        #prepare and register the node:
        node.index=i
        self.register_node(node)
        return node

    def __len__(self):
        return len(self.connectivity)
        
    def in_morphology(self,component):
        """True if the node is a member of the morphology"""
        return component in self.__registered_components

class MorphologyArrayObserver(object):
    """
    
    """

    def __init__(self):
        self.component=[]
        self.index_change=None
        self.new_morphology
        
    def observe(self):
    
    def stop_observing(self):
    
    def index_change(self,position,increment):
        for component in self.components:
            component.index_change(position,increment)

    def parent_change(self,morphology_array)
        for component in self.components:
            component.morphology_array=morphology_array

     
class __MorphologyComponent(object):

    def __init__(self):
        raise NotImplementedError
        
    def __connect__(self):
        raise NotImplementedError
        
class Node(__MorphologyComponent):
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

    def __init__(self,vertex=[0.0,0.0,0.0,0.0],node_type=None):

        self.index=0
        self.node_type=node_type

        #make the morphology and register this section to it
        connectivity=np.array([-1],dtype='int32')

        morphology_array=MorphologyArray(vertices=[vertex],
                                        connectivity=connectivity,
                                        node_types=node_type)

        self.__morphology_array=morphology_array
        self.__weak_morphology_array=weakref.proxy(morphology_array)
        self.__morphology_array.register_component(self)

    @property
    def morphology_array(self):
        """
        Return a weakly-referenced proxy to the MorphologyArray object
        which this node belongs to.
        """
        return self.__weak_morphology_array

    @property
    def morphology(self):
        """
        Return a node collection
        """
        return NodeCollection(self._morphology)

    @morphology.setter
    def morphology(self,morphology):
        raise NotImplementedError,"this probably isn't allowed..."
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
        return self._morphology.vertex(self.index)

    @property
    def parent_id(self):
        return self._morphology.parent_id(self.index)

    @parent_id.setter
    def parent_id(self,index):
        self._morphology.connectivity[self.index]=index

    @property
    def __is_root(self):
        """
        Returns True if section is root
        """
        return self.parent_id==-1

    def connect(self,parent):
        """
        connect this node to a new parent

        This is done by connecting the child morphology 
        to the parent morphology and delting the child morphology
        """

        #ensure this node isn't already in the same morphology as parent:
        assert parent.morphology_array.in_morphology(self)==False, 'Parent node already in morphology!'        

        #node needs to be root of its morphology_array to connect
        if not self.__is_root:self.__morphology_array.to_root(self.index)

        parent_morphology_array=parent.morphology_array
        parent_index=parent.index

        #connect the morphologies to each other:
        parent_morphology_array.adopt(child_morphology=self._morphology,
                                 parent_index=parent_index)

       #the parent morphology is now the child morpholoy
        self.__morphology_array=parent.morphology_array
        self.__weak_morphology_array=parent.morphology_array
        
class MorphologyCollection(__MorphologyComponent):
    def __init__(self):
        pass

class NodeCollection(MorphologyCollection):

    """
    Works as an iterable visitor, part of or all of a morphology
    all the nodes are connected.
    
    Morphology should not be iterable.
    
    using nodecollection is important in order to guarantee that
    there is only one copy of all the vertex and connectivity
    information at a given time, hence the 'back end'.
    
    lazy-evaluation of the getter ensures that a minimum number
    of objects are instantiated.
    """

    def __init__(self,morphology):
        #these will all have to be updated if a connection is made
        #to another morphology
        self.__morphology=morphology
        self.__morphology_start_index=0
        self.__morphology_end_index=len(self.__morphology.connectivity)-1
        #register the nodecollection
        #disabled for now
#        self.__morphology.register(self)
                
    def __getitem__(self,i):
        index=i+self.__morphology_start_index
        return self.__morphology[index]
        
    def __len__(self):
        return self.end_index-self.start_index
        
    def in_morphology(self,component):
        """True if the node is a member of the morphology"""
        return self.__morphology.in_morphology(component)
        
        
class Segment(NodeCollection):
    def __init__(self):
        pass


class Cylinder(Segment):
    def __init__(self):
        pass


class Section(object):

    """
    Note - section type should be the type
    of the distal node    
    """

    """
    In the process of implementing NEURON-like sections.

    These will also have their own connect() etc methods
    but will be more complicated than nodes as they
    have distal and proximal components.

    NEURON-type implies the possibility of a discontinuity
    as far as I can infer.
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
        raise NotImplementedError, 'Cannot reset section length'

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

    def connect(self,section,position=None):
        """        
        Position is not implemented until we
        decide exactly what it means, right now
        1 means distal and anything else means
        proximal.

        Currently a lot of this simply won't work
        because a node needs to be a root for the
        connect() method to work. We need a method
        in the MorphologyArray class to make
        transform the array and make any node into
        the root of that array.

        Things actually get tricky with sections
        because the proximal node(of the child needs
        to become the distal node of the parent)

        I think we need to have the possibility to insert
        a node between two nodes. this will allow the
        cool possibility of making a connection anywhere
        along another section. However it will involve
        some thinking to decide exactly how to implement
        this
        """
