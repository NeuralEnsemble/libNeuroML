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

r"""
Prototype for object model backend for the libNeuroML project

AUTHORS:

- Mike Vella: initial version
- Mike Hull - Large parts of Backend and SWCLoader
"""
import math
import numpy as np

class Network(object):
    def __init__(self):
        pass


class Morphology(object):
    def __init__(self,whole_segment_group):
        self.__whole_segment_group=segment_group

        
class Cell(object):
    def __init__(self,morphology=None,biophysical_properties=None,
               notes=None):

        self.morphology=morphology
        self.biophysical_properties=biophysical_properties
        self.notes=notes

  
class Backend(object):
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
    other element an element is attached. So for instance,
    connectivity[3] is an integer with the index of the section
    it refers to in the Backend

    -note on Nodes::
    a Node class is provided (see further down) however this
    does not result in a tree-based object model. Rather, the section
    objects manipulate the Backend backend in a way that 
    is invisible to the user. The user may still use the 
    Backend class, depending on their needs.

    Backend[i] returns the Node object relating to
    element i

    Because segments exist in memory independently of the,
    Backend, a Backend must keep a register
    of all the segments which handle its elements. These
    are updated when their information changes via a Backend
    operation such as the indices changing when a connection
    to a new Backend is made and indices all change.
    """

    def __init__(self,vertices,connectivity,node_types=None,
                name=None,physical_mask=None,fractions_along=None):

        self.connectivity = np.array(connectivity)
        self.vertices = np.array(vertices)

        if physical_mask != None:
            self._physical_mask=np.array(physical_mask)
        else:
            self._physical_mask=np.zeros(len(connectivity),dtype='bool')
        if node_types != None:
            self.node_types=np.array(node_types)
        else:
            self.node_types=np.zeros(len(connectivity),
                                        dtype='int32')

        if fractions_along != None:
            self.fractions_along = np.array(fractions_along)
        else:
            self.fractions_along=np.zeros(len(connectivity),
                                         dtype='int32')


        assert(self.valid_morphology,'invalid_morphology')

        self.observer = ComponentObserver()

    @property
    def valid_morphology(self):
        M = self.vertices.shape[0]
        N = self.connectivity.shape[0]
        P = self.node_types.shape[0]
        return(N == M == P)

    @property
    def root_index(self):
        return np.where(self.connectivity == -1)[0][0]
    
    @property
    def root_vertex(self):
        return self.vertices[self.root_index]    

    @property
    def root_node(self):
        index=self.root_index
        return self[index]

    @property
    def physical_indices(self):
        """returns indices of vertices which are physical"""
        return np.where(self._physical_mask == 0)[0]
        
    def children(self,index):
        """Returns an array with indexes of children"""
        return np.where(self.connectivity == index)

    def to_root(self,index):
        """
        Changes the connectivity matrix
        so that the node at index becomes the root
        """

        old_root_index = self.root_index
        new_root_index = index        
        #do a tree traversal:
        parent_index = self.connectivity[index]
        grandparent_index=self.connectivity[parent_index]
        while index!=old_root_index:
            self.connectivity[parent_index]=index
            index = parent_index
            parent_index = grandparent_index
            grandparent_index = self.connectivity[parent_index]
        self.connectivity[new_root_index] = -1

    def parent_id(self,index):
        """Return the parent index for the given index"""
        return self.connectivity[index]

    def vertex(self,index):
       """Return vertex corresponding to index in morphology"""
       return self.vertices[index]

    def __getitem__(self,i):
        node = Node(vertex = [self.vertices[i]],node_type=[self.node_types[i]])
        #prepare and register the node:
        node._index = i
        node._backend = self
        self.observer.observe(node)
        return node

    def __len__(self):
        return len(self.connectivity)
        
    #I would like to move the following two methods out of here
    #and into respective component classes
    def pop(self,index):
        """
        Deletes a node from the Backend, its children become
        children of the deleted node's parent.
        """    

        self.vertices = np.delete(self.vertices,index)
        self.node_types = np.delete(self.node_types,index)
        self.connectivity = np.delete(self.connectivity,index)

        #TO DO:
        #there is a more efficient way to implement this using np.where(self.connectivity>=index)
        k = 0
        for i in self.connectivity:
            if i >= index:
                self.connectivity[k] = i - 1
            k += 1
        pass

    def insert(self,index,x):
        """
        Inserts a node between a node and its parent at
        x between them. Where x ranges from 0 to 1, 0 being
        the location of the child and 1 the location of the
        parent.

        ..TO-DO: vertex of new node needs to be calculated through
        linear interpolation.

        Also,perhaps this should rather be inserted at the root level.
        methods which modify the arrays should do so from outside
        this should behave like a container as much as is reasonable
        """

        assert index != 0, 'Cannot insert on root node - It has no parent'

        parent_id = self.parent_id(index)
        parent_node = self[parent_id]        
        #TO DO - calculate the vertex from the parent and child and x, 
        new_node = Node()
        old_node = self[index]
        new_node.attach(parent_node)
        old_node.parent_id = new_node.index

class ComponentObserver(object):
    """
    Keeps a record of which components reference a morphology
    and updates them with new information when needed.
    #make it such that if the arg is = none they all get updated
    """

    def __init__(self):
        self.components = np.array([])
      
    def observe(self,component):
        self.components = np.append(self.components,component)
     
    def deobserve(self):
        i = np.where(self.components == component)[0][0]
        np.delete(self.components,i)
        
    def index_update(self,position,increment):
        for component in self.components:
            component._index_update(position,increment)

    def backend_update(self,backend):
        for component in self.components:
            component._backend = backend

    #The following four methods may not be a smart way to do this
    def segment_observed(self,i):
       for component in self.components:
           try:
               if component.distal._index == i:
                   return True
           except AttributeError, e:
               pass
       return False

    def node_observed(self,i):
       for component in self.components:
           try:
               if component._index == i:
                   return True
           except AttributeError, e:
               pass
       return False

    def node(self,i):
        """
        Returns the node reference if it's observed, false otherwise
        """
        for component in self.components:
            if component._index == i and type(component) == Node:
                return component
        raise Exception('No such node')

    def segment(self,i):
        """
        Returns the segment reference if it's observed, false otherwise
        """
        for component in self.components:
            'checking...'
            if component._index == i and type(component) == Segment:
                return component
        raise Exception('No such segment')

class MorphologyComponent(object):
    
    def __init__(self):
        self._backend = None

    def attach(self):
        raise NotImplementedError

    def _index_update(self,position,increment):
        raise NotImplementedError,'This component requires an index updater'

    def backend_update(self):
        raise NotImplementedError

    def in_morphology(self,component):
        """True if the node is a member of the morphology"""
        return component in self._backend.observer.components

class Node(MorphologyComponent):
    """
    The idea of the Node class is to provide a user with a natural
    way of manipulating compartments while still utilising an array-
    based backend. The user does not have to use Node objects,
    it is provided in particular for users who create models 
    with a small number of compartments.

    A node can be instantiated independently of a morphology, however
    such a node genernates its own morphology when it is instantiated.

        A=Node()
        B=Node()

    Will create two morphology objects and two node objects
    call the morphology objects A_morph and B_morph
    
    When A.attach(B) is executed, the pattern is

    child.attach(parent). Hence A now becomes part of the
    B_morph object (registerd to its observer) and the 
    A_morph object is destroyed (its reference count is 
    dropped to zero and it is handled by the Python 
    garbage collector).

    The idea of this "hidden" complexity is that it 
    combines the power of a more natural object-oriented 
    way of manipulating small numbers of compartments with an
    array-based backend.
    """

    def __init__(self,vertex=[0.0,0.0,0.0,0.0],node_type=None):

        self._index = 0
        self.node_type = node_type

        #make the morphology and register this section to it
        connectivity=np.array([-1],dtype = 'int32')

        backend=Backend(vertices = [vertex],
                                        connectivity = connectivity,
                                        node_types = node_type)

        self._backend = backend
        self._backend.observer.observe(self)

    def _index_update(self,position,increment):
        if self._index >= position:
            self._index += increment

    @property
    def morphology(self):
        """
        Return a node collection
        """
        return NodeCollection(self._backend)

    @property
    def parent(self):
        return self._backend[self.__parent_id]

    @property
    def fraction_along(self):
        fraction_along=self.fractions_along[self._index]
        return fraction_along

    @fraction_along.setter
    def fraction_along(self,fraction_along):
        self._backend.fractions_along[self._index]=fraction_along
      
    @morphology.setter
    def morphology(self,morphology):
        raise NotImplementedError,"this probably won't be allowed..."

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
        return self.vertex[3]

    @property
    def vertex(self):
        return self._backend.vertex(self._index)

    @property
    def __parent_id(self):
        return self._backend.parent_id(self._index)

    @__parent_id.setter #ought not be here, why have a setter on this?
    def __parent_id(self,index):
        self.__morphology.connectivity[self._index]=index

    @property
    def __is_root(self):
        """
        Returns True if section is root
        """
        return self.__parent_id == -1

    def attach(self,child):
        """
        Attach this node to a new child
        """        

        assert self.in_morphology(child) == False, 'Parent node already in morphology!'        

        self._morphadopt(child_morphology = child._backend)

#    def attach(self,parent):
#        """
#        attach this node to a new parent

#        This is done by attaching the child morphology 
#        to the parent morphology and delting the child morphology
#        """

#        #ensure this node isn't already in the same morphology as parent:
#        assert self.in_morphology(parent) == False, 'Parent node already in morphology!'        

#        #this was decided against in 25/06/12 June UCL meeting
#        #node needs to be root of its backend to attach
#        #if not self.__is_root: self._backend.to_root(self._index)
#        #instead replaced with:
    
#        assert(self.__is_root,'attaching node must be root')
#
#        #everything should now be handled including the observer's tasks
#        parent._morphadopt(child_morphology = self._backend)

    def shift_attach(self,parent):
        """
        attach this node to a new parent

        This is done by attaching the child morphology 
        to the parent morphology and delting the child morphology
        """
        #translate and attach:
        self.translate_morphology(parent.vertex[0:3])
        self.attach(parent)

    def translate_morphology(self,origin):
        """
        Translate the morphology to a new origin, with node
        at the origin.
        """

        translation_vector=self.vertex[0:3]-origin
        self.morphology.vertices[:,0:3]-=translation_vector

    def _morphadopt(self,child_morphology):
        """
        Attach another morphology to this one.
        """

        self._backend.vertices = np.append(self._backend.vertices,child_morphology.vertices,axis=0)

        #increment and append connectivity
        num_parent_nodes = len(self._backend.connectivity)
        new_connectivity = np.copy(child_morphology.connectivity)
        new_connectivity += num_parent_nodes
        new_connectivity[child_morphology.root_index] = self._index
        self._backend.connectivity = np.append(self._backend.connectivity,
                                    new_connectivity,axis = 0)

        #add new node types to morphology
        self._backend.node_types=np.append(self._backend.node_types,
                                    child_morphology.node_types,axis = 0)

        #tell child observer what to update
        child_morphology.observer.index_update(0,num_parent_nodes)
        child_morphology.observer.backend_update(self._backend)

        #tell parent observer to observe instantiated components of child:
        for component in child_morphology.observer.components:
            self._backend.observer.observe(component)
      
class MorphologyCollection(MorphologyComponent):
    """
    Subclasses are iterable visitors, more documentation
    on this to follow.    
    """
    def __init__(self):
        pass

    def _index_update(self,position,increment):
        raise NotImplementedError,'This collection requires an index updater'

    @property
    def root_segment(self):
        """
        Returns the root segment for the morphology
        """
        root_node=self._backend.root_node
        return Segment(root_node)


class NodeCollection(MorphologyCollection):
    """
    An iterable visitor, part of or all of a morphology
    all the nodes are attached.
    
    Morphology should not be iterable.
    
    using nodecollection is important in order to guarantee that
    there is only one copy of all the vertex and connectivity
    information at a given time, hence the 'back end'.
    
    lazy-evaluation of the getter ensures that a minimum number
    of objects are instantiated.
    """

    def __init__(self,morphology):
        self._backend = morphology
        self._morphology_start_index = 0
        self._morphology_end_index = len(self._backend.connectivity)-1
        self._backend.observer.observe(self)

    def __getitem__(self,i):
        index = i+self._morphology_start_index

        if self._backend.observer.node_observed(i):
            return self._backend.observer.node(i)
        else:
            return self._backend[index]
        
    def __len__(self):
        return self._morphology_end_index-self._morphology_start_index
        
    def _index_update(self,position,increment):
        #WARNING:This module is still insufficiently tested
        if position>self._morphology_start_index and position<morphology_end_index:
            raise NotImplementedError,"insertions not allowed in NodeCollection domain!"

        if position>self._morphology_end_index:
            pass

        else:
            self._morphology_start_index += increment
            self._morphology_end_index += increment
        
    def _backend_update(self,backend):
        self._backend=backend
  
    @property
    def connectivity(self):
        return self._backend.connectivity[self._morphology_start_index:self._morphology_end_index+1]

    @property
    def vertices(self):
        return self._backend.vertices[self._morphology_start_index:self._morphology_end_index+1]
    

class SegmentGroup(MorphologyCollection):
    """
    Iterable container of segments
    """
    def __init__(self,morphology):
        self._backend=morphology
        self._morphology_segment_indices = self._backend.physical_indices
        self._backend.observer.observe(self)

        #this is a bit of a hack, need a more elegant solution:
        self._index=None

    def _index_update(self,position,increment):
        #is there a more efficient way to do this?
        i=0
        for index in self._morphology_segment_indices:
            if index >= position:
                self._morphology_segment_indices[i] += increment
            i += 1

    def __getitem__(self,i):
        segment_index=self._morphology_segment_indices[i]
        if self._backend.observer.segment_observed(segment_index):
            return self._backend.observer.segment(segment_index)
        else:
            distal_node=self._backend[segment_index]
            return Segment(distal_node=distal_node)
        
    def __len__(self):
        return self._morphology_end_index-self._morphology_start_index
        
    def _backend_update(self,backend):
        self._backend = backend
  
    @property
    def connectivity(self):
        return self._backend.connectivity[self._morphology_start_index:self._morphology_end_index+1]

    @property
    def vertices(self):
        return self._backend.vertices[self._morphology_start_index:self._morphology_end_index+1]

    @property
    def morphology(self):
        return SegmentGroup(self._backend)

 
class Segment(MorphologyCollection):
    """
    In the process of implementing, this class will
    provide the same functionality as NEURON sections.

    Segments will also have their own attach() etc methods
    but will be more complicated than nodes as they
    have distal and proximal components.

    """

    def __init__(self,length=100,proximal_diameter=10,distal_diameter=None,
                segment_type=None,name=None,
                distal_node=None):
   
        if distal_node != None:
            self._from_node(distal_node)

        else:
            prox = np.array([0.0,0.0,0.0,proximal_diameter])
            dist = np.array([0.0,0.0,length,distal_diameter])
            self.proximal = Node(prox,node_type = segment_type)
            self.distal = Node(dist,node_type = segment_type)
            self.distal.attach(self.proximal)

        if distal_diameter == None:distal_diameter = proximal_diameter
        
        self.segment_type = segment_type
        self.name = name

        self._backend = self.proximal._backend
        self._backend.observer.observe(self)

    def _from_node(self,distal_node):
        #now need to check with observer if segment has been
        #instantiated, if it has I think throw an error for now?
        self.distal = distal_node
        self.proximal = distal_node.parent
        
    def _index_update(self,*args):
        """
        Should be no need for this method as nodes are updated
        themselves by the observer
        """
        pass

    def insert(self,kinetic_component):
        kinetic_component._index = self._index
        self._backend.observer.observe(kinetic_component)

    @property
    def _index(self):
        #at the moment using dist, this needs to be changed to prox for the whole class
        return self.proximal._index

    @property
    def proximal_diameter(self):
        return self.proximal.radius

    @property
    def distal_diameter(self):
        return self.proximal.radius

    @property
    def length(self):
        displacement = self.proximal.vertex - self.distal.vertex        
        return math.sqrt(sum(displacement ** 2))
    
    @length.setter
    def length(self,value):
        raise NotImplementedError, 'Cannot reset section length'

    @property
    def index(self):
        return (self.proximal,self.distal)

    @property
    def morphology(self):
        return self.distal.morphology

    @property
    def slant_height(self):
        r = self.proximalimal_diameter
        R = self.distalal_diameter
        s = math.sqrt((r - R) ** 2 + self.length ** 2)
        return s

    @property
    def lateral_area(self):
        lsa = math.pi * (self.proximalimal_diameter + self.distalal_diameter) * self.slant_height
        return lsa

    @property
    def total_area(self):
        lsa = self.lateral_area
        end_areas = math.pi * (self.proximalimal_diameter ** 2 + self.distalal_diameter ** 2)
        return lsa+end_areas

    @property
    def parent(self):
       #this isn't accounting for virtual segments...
       parent_node=self.distal.parent 
       grandparent_node=parent_node.parent
       return Segment(dist=grandparent_node)

    @property
    def parent_id(self):
        #also needs to account for existence of virtual segments
        #currently it's assuming the extreme presence ie virtual segment
        #exists between every segment
        parent_node=self.distal.parent
        grandparent_node=parent_node.parent
        return grandparent_node._index

    @property
    def volume(self):
        r = self.proximalimal_diameter
        R = self.distalal_diameter
        V = (math.pi * self.length / 3.0) * (R ** 2 + r ** 2 + R * r)
        return V

    def attach(self,segment_group,fraction_along=0.0):
        """        
        Position is not implemented until we
        decide exactly what it means, right now
        1 means distal and anything else means
        proximal.

        Currently a lot of this simply won't work
        because a node needs to be a root for the
        attach() method to work. We need a method
        in the Backend class to make
        transform the array and make any node into
        the root of that array.

        I think we need to have the possibility to insert
        a node between two nodes. This will allow the
        cool possibility of making a attachion anywhere
        along another section. However it will involve
        some thinking to decide exactly how to implement
        this as it might mess up NodeCollections.
        """
        #this could be handled by a COR, first try a cell, then a morphology etc,
        #or perhaps we can think of something smarter?
        root_segment=segment_group.root_segment
        self.distal.attach(root_segment.proximal)
        self.distal.fraction_along=fraction_along

class Cylinder(Segment):
    """
    A special case of segment where proximal_diameter = distal_diameter...TBC
    """
    def __init__(self):
        pass
