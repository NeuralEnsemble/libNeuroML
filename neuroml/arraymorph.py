r"""
Prototype for object model backend for the libNeuroML project
"""


import numpy as np
import neuroml


neuro_lex_ids = {
    'axon': "GO:0030424",
    'dend': "GO:0030425",
    'soma': "GO:0043025",
}


def get_seg_group_by_id(sg_id, morph):
    # type (str, Cell) -> SegmentGroup
    """Return the SegmentGroup object for the specified segment group id.

    :param sg_id: id of segment group to find
    :type sg_id: str
    :param cell: cell to look for segment group in
    :type cell: Cell
    :returns: SegmentGroup object of specified ID or None if not found

    """
    if not sg_id or not morph:
        print("Please specify both a segment group id and a Morphology")
        return None

    for sg in morph.segment_groups:
        if sg.id == sg_id:
            return sg

    return None


class ArrayMorphology(neuroml.Morphology):
    """Core of the array-based object model backend.

    Provides the core arrays - vertices,connectivity etc.
    node_types.

    The connectivity array is a list of indices pointing to which
    other element an element is attached. So for instance,
    connectivity[3] is an integer with the index of the section
    it refers to in the Backend

    - EXAMPLE:

        Vertices[3] and connectivity[3] refer to the vertex
        and connectivity of the same node.

    .. note::

       The root section by convention has connectivity == -1.

    """

    def __init__(
        self,
        vertices=[],
        connectivity=[],
        id=None,
        node_types=None,
        name=None,
        physical_mask=None,
        fractions_along=None,
    ):

        super(ArrayMorphology, self).__init__()

        self.connectivity = np.array(connectivity)
        self.vertices = np.array(vertices)

        if id is None:
            self.id = name
        else:
            self.id = id
        self.name = name

        if np.any(physical_mask):
            self.physical_mask = np.array(physical_mask)
        else:
            self.physical_mask = np.zeros(len(connectivity), dtype="bool")

        if np.any(node_types):
            self.node_types = np.array(node_types)
        else:
            self.node_types = np.zeros(len(connectivity), dtype="int32")

        if np.any(fractions_along):
            self.fractions_along = np.array(fractions_along)
        else:
            self.fractions_along = np.zeros(len(connectivity), dtype="int32")

        # it will need a reference to its parent?
        self.segments = SegmentList(self)

        assert self.valid_morphology, "invalid_morphology"

    @property
    def valid_morphology(self):
        all_nodes = self.__all_nodes_satisfied
        all_vertices = self.__all_vertices_present
        return all_nodes and all_vertices

    @property
    def __all_vertices_present(self):
        try:
            all_vertices_present = self.vertices.shape[1] == 4
        except:
            all_vertices_present = False

        num_vertices = len(self.vertices)

        return all_vertices_present or num_vertices == 0

    @property
    def valid_ids(self):
        valid_flag = True

        for internal_id in self.segments.instantiated_segments.keys():
            external_id = self.segments.instantiated_segments[internal_id].id
            valid_flag = (internal_id == external_id) * valid_flag

        return valid_flag

    @property
    def __all_nodes_satisfied(self):
        m = self.vertices.shape[0]
        n = self.connectivity.shape[0]
        p = self.node_types.shape[0]

        all_nodes_satisfied = m == n == p
        return all_nodes_satisfied

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
        physical_indices = np.where(self.physical_mask == 0)[0]
        return physical_indices

    def children(self, index):
        """Returns an array with indexes of children"""
        return np.where(self.connectivity == index)

    def to_root(self, index):
        """
        Changes the connectivity matrix
        so that the node at index becomes the root
        """

        old_root_index = self.root_index
        new_root_index = index
        # do a tree traversal:
        parent_index = self.connectivity[index]
        grandparent_index = self.connectivity[parent_index]
        while index != old_root_index:
            self.connectivity[parent_index] = index
            index = parent_index
            parent_index = grandparent_index
            grandparent_index = self.connectivity[parent_index]
        self.connectivity[new_root_index] = -1

    def parent_id(self, index):
        """Return the parent index for the given index"""
        return self.connectivity[index]

    def vertex(self, index):
        """Return vertex corresponding to index in morphology"""
        return self.vertices[index]

    def __len__(self):
        return len(self.connectivity)

    def pop(self, index):
        """
        TODO:This is failing tests (understandably) - need to fix!
        Deletes a node from the morphology, its children become
        children of the deleted node's parent.
        """

        self.vertices = np.delete(self.vertices, index)
        self.node_types = np.delete(self.node_types, index)
        self.connectivity = np.delete(self.connectivity, index)

        k = 0
        for i in self.connectivity:
            if i >= index:
                self.connectivity[k] = i - 1
            k += 1
        pass

    def to_neuroml_morphology(self, id="", add_color_prop=False):

        morphology = neuroml.Morphology()
        if id:
            morphology.id = id
        else:
            morphology.id = self.id

        seg_group_all = neuroml.SegmentGroup(id='all')
        seg_group_soma = neuroml.SegmentGroup(id='soma_group',
                                              neuro_lex_id=neuro_lex_ids["soma"],
                                              notes="Default soma segment group for the cell")
        seg_group_axon = neuroml.SegmentGroup(id='axon_group',
                                              neuro_lex_id=neuro_lex_ids["axon"],
                                              notes="Default axon segment group for the cell")
        seg_group_dend = neuroml.SegmentGroup(id='dendrite_group',
                                              neuro_lex_id=neuro_lex_ids["dend"],
                                              notes="Default dendrite segment group for the cell")

        if add_color_prop:
            seg_group_soma.properties.append(neuroml.Property(tag="color", value="0.8 0 0"))
            seg_group_axon.properties.append(neuroml.Property(tag="color", value="0 0.8 0"))
            seg_group_dend.properties.append(neuroml.Property(tag="color", value="0 0 0.8"))

        morphology.segment_groups.append(seg_group_all)
        morphology.segment_groups.append(seg_group_soma)
        morphology.segment_groups.append(seg_group_axon)
        morphology.segment_groups.append(seg_group_dend)

        # need to traverse the tree:
        for index in range(self.num_vertices):
            seg = self.segment_from_vertex_index(index, morphology)
            morphology.segments.append(seg)

        self.group_segments(morphology)

        return morphology

    def segment_from_vertex_index(self, index, morphology):
        parent_index = self.connectivity[index]

        node_x = self.vertices[index][0]
        node_y = self.vertices[index][1]
        node_z = self.vertices[index][2]
        node_d = self.vertices[index][3]

        parent_x = self.vertices[parent_index][0]
        parent_y = self.vertices[parent_index][1]
        parent_z = self.vertices[parent_index][2]
        parent_d = self.vertices[parent_index][3]


        p = neuroml.Point3DWithDiam(x=node_x, y=node_y, z=node_z, diameter=node_d)

        d = neuroml.Point3DWithDiam(x=parent_x, y=parent_y, 
                                    z=parent_z, diameter=parent_d)

        seg = neuroml.Segment(proximal=p, distal=d, id=index)
        if parent_index != -1:
            parent = neuroml.SegmentParent(segments=parent_index)
            seg.parent = parent

        return seg

    def group_segments(self, morphology):

        non_branching_lex_id = 'sao864921383'

        N = len(self.connectivity)
        ind_root = np.where(self.connectivity == -1)[0]
        assert(len(ind_root) == 1)
        assert(not np.any(np.arange(N) == self.connectivity))
        ind_root = ind_root[0]

        nodes, counts = np.unique(self.connectivity, return_counts=True)
        nodes = nodes[counts > 1]

        parent_trunks = np.arange(N)
        # parent_trunks are the children of parent_nodes.
        # They are the trunk of non-branching sections
        for ind, parent_node in enumerate(self.connectivity):
            if ind == ind_root:
                continue
            while parent_node not in nodes:
                # Go one step back
                parent_trunks[ind] = parent_node
                parent_node = self.connectivity[parent_node]

        seg_prefixes = {1: "soma", 2: "axon", 3: "dend", 4: "apical"}
        default_groups = {1: get_seg_group_by_id("soma_group", morphology),
                          2: get_seg_group_by_id("axon_group", morphology),
                          3: get_seg_group_by_id("dendrite_group", morphology),
                          4: get_seg_group_by_id("dendrite_group", morphology),
                          }

        trunks = np.unique(parent_trunks)
        for trunk in trunks:
            if self.node_types[trunk] in seg_prefixes:
                trunk_type = seg_prefixes[self.node_types[trunk]]
            else:
                trunk_type = "other"

            group_id = f"{trunk_type}_{trunk}"
            seg_group = neuroml.SegmentGroup(id=group_id,
                                             neuro_lex_id=non_branching_lex_id)
            for ind in np.arange(N)[parent_trunks == trunk]:
                seg_group.members.append(neuroml.Member(segments=morphology.segments[ind].id))

            # Add the segment group to the morphology
            morphology.segment_groups.insert(0, seg_group)

            # Include the segment group in the corresponding anatomical group
            default_group = default_groups[self.node_types[trunk]]
            default_group.includes.append(neuroml.Include(segment_groups=group_id))

            # Add to the all group
            seg_group_all = get_seg_group_by_id("all", morphology)
            seg_group_all.includes.append(neuroml.Include(segment_groups=group_id))




class SegmentList(object):
    """
    This class is a proxy, it returns a segment either
    from the arraymorph or if it has already been instantiated
    it returns the relevant segment.
    """

    def __init__(self, arraymorph):
        self.arraymorph = arraymorph
        self.instantiated_segments = {}

    def __vertex_index_from_segment_index__(self, index):
        """
        The existence of a physical mask means that segment and
        and vertex indices fall out of sync. This function returns the
        index of the proximal vertex in the vertices array of the arraymorph
        which corresponds to the segment index.
        """

        physical_mask = self.arraymorph.physical_mask
        segment_distal_vertex_indexes = np.where(physical_mask == False)[0] + 1

        return segment_distal_vertex_indexes[index]

    def __len__(self):
        """
        Override the __len__ magic method to give total numer of
        segments which is number of vertices - 1 and minus all
        floating segments.
        """

        num_vertices = self.arraymorph.num_vertices
        num_floating = np.sum(self.arraymorph.physical_mask)
        num_segments = num_vertices - num_floating - 1
        if num_segments < 0:
            num_segments = 0

        return int(num_segments)

    def __iadd__(self, segment_list):
        for segment in segment_list:
            self.append(segment)
        return self

    def __getitem__(self, segment_index):

        if segment_index in self.instantiated_segments:
            neuroml_segment = self.instantiated_segments[segment_index]
        else:
            vertex_index = self.__vertex_index_from_segment_index__(segment_index)
            neuroml_segment = self.arraymorph.segment_from_vertex_index(vertex_index)
            self.instantiated_segments[segment_index] = neuroml_segment
        return neuroml_segment

    def __setitem__(self, index, user_set_segment):
        self.instantiated_segments[index] = user_set_segment

    def append(self, segment):
        """
        Adds a new segment

        TODO: Correct connectivity is currently being ignored -
        The new segment is always connected to the root node.
        """
        dist_vertex_index = len(self.arraymorph.vertices)
        prox_vertex_index = dist_vertex_index + 1

        prox_x = segment.proximal.x
        prox_y = segment.proximal.y
        prox_z = segment.proximal.z
        prox_diam = segment.proximal.diameter

        dist_x = segment.distal.x
        dist_y = segment.distal.y
        dist_z = segment.distal.z
        distal_diam = segment.distal.diameter

        prox_vertex = [prox_x, prox_y, prox_z, prox_diam]
        dist_vertex = [dist_x, dist_y, dist_z, distal_diam]

        if len(self.arraymorph.vertices) > 0:
            self.arraymorph.vertices = np.append(
                self.arraymorph.vertices, [dist_vertex, prox_vertex], axis=0
            )
        else:
            self.arraymorph.vertices = np.array([dist_vertex, prox_vertex])

        self.arraymorph.connectivity = np.append(
            self.arraymorph.connectivity, [-1, dist_vertex_index]
        )

        if len(self.arraymorph.physical_mask) == 0:
            self.arraymorph.physical_mask = np.array([0, 0])
        else:
            self.arraymorph.physical_mask = np.append(
                self.arraymorph.physical_mask, [1, 0]
            )

        segment_index = len(self) - 1
        self.instantiated_segments[segment_index] = segment
