r"""
Prototype for object model backend for the libNeuroML project
"""

import math
import numpy as np
import neuroml

class Morphology(object):
    """Core of the array-based object model backend.

    Provides the core arrays - vertices,connectivity and node_types.        
    The connectivity array is a list of indices pointing to which
    other element an element is attached. So for instance,
    connectivity[3] is an integer with the index of the section
    it refers to in the Backend

    - EXAMPLE:

        Vertices[3] and connectivity[3] refer to the vertex 
        and connectivity of the same node.

    .. note::

       The root section by convention has connectivity == -1.

    .. note::

        A Node class is provided (see further down) however this
        does not result in a tree-based object model. Rather, 
        the section objects manipulate the Backend backend in 
        a way that is invisible to the user. The user may 
        still use the Backend class, depending on their needs.

    .. note::

        Backend[i] returns the Node object relating to
        element i.

    .. note::

        Because segments exist in memory independently of the,
        Backend, a Backend must keep a register
        of all the segments which handle its elements. These
        are updated when their information changes via a Backend
        operation such as the indices changing when a connection
        to a new Backend is made and indices all change.
    """

    def __init__(self,vertices,
                 connectivity,
                 node_types=None,
                 name=None,
                 physical_mask=None,
                 fractions_along=None):

        self.connectivity = np.array(connectivity)
        self.vertices = np.array(vertices)

        if physical_mask != None:
            raise NotImplementedError #temporary, until this functionality is implemented
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


        assert self.valid_morphology,'invalid_morphology'

    @property
    def valid_morphology(self):
        m = self.vertices.shape[0]
        n = self.connectivity.shape[0]
        p = self.node_types.shape[0]

        all_nodes_satisfied = m == n == p

        try:
            all_vertices_present = self.vertices.shape[1] == 4
        except:
            all_vertices_present = False

        return(all_nodes_satisfied and all_vertices_present)

    @property
    def root_index(self):
        return np.where(self.connectivity == -1)[0][0]    

    @property
    def root_vertex(self):
        return self.vertices[self.root_index]    

    @property
    def num_vertices(self):
        return len(self.vertices)

    @property
    def physical_indices(self):
        """returns indices of vertices which are physical"""
        physical_indices = np.where(self._physical_mask == 0)[0]
        return physical_indices
        
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

    def __len__(self):
        return len(self.connectivity)
        
    def pop(self,index):
        """
        TODO:This is failing tests (understandably) - need to fix!
        Deletes a node from the morphology, its children become
        children of the deleted node's parent.
        """    

        self.vertices = np.delete(self.vertices,index)
        self.node_types = np.delete(self.node_types,index)
        self.connectivity = np.delete(self.connectivity,index)

        k = 0
        for i in self.connectivity:
            if i >= index:
                self.connectivity[k] = i - 1
            k += 1
        pass

    def to_neuroml_morphology(self,id=""):

        morphology = neuroml.Morphology()
        morphology.id = id

        #need to traverse the tree:
        for index in range(self.num_vertices):
            if self.connectivity[index] != -1:
                parent_index = self.connectivity[index]

                node_x = self.vertices[index][0]
                node_y = self.vertices[index][1]
                node_z = self.vertices[index][2]
                node_d = self.vertices[index][3]
                
                parent_x = self.vertices[parent_index][0]
                parent_y = self.vertices[parent_index][1]
                parent_z = self.vertices[parent_index][2]
                parent_d = self.vertices[parent_index][3]                

                d = neuroml.Point3DWithDiam(x=node_x,
                                            y=node_y,
                                            z=node_z,
                                            diameter=node_d)

                p = neuroml.Point3DWithDiam(x=parent_x,
                                            y=parent_y,
                                            z=parent_z,
                                            diameter=parent_d)

                
                seg = neuroml.Segment(proximal=p,
                                      distal=d,
                                      id=index)
                if index <=1:
                    parent = neuroml.SegmentParent(segments=index-1)

                morphology.segments.append(seg)

        return morphology
