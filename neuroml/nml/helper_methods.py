import re
import sys


#
# You must include the following class definition at the top of
#   your method specification file.
#
class MethodSpec(object):
    def __init__(self, name="", source="", class_names="", class_names_compiled=None):
        """MethodSpec -- A specification of a method.
        Member variables:
            name -- The method name
            source -- The source code for the method.  Must be
                indented to fit in a class definition.
            class_names -- A regular expression that must match the
                class names in which the method is to be inserted.
            class_names_compiled -- The compiled class names.
                generateDS.py will do this compile for you.
        """
        self.name = name
        self.source = source
        self.class_names = class_names
        """
        if class_names is None:
            self.class_names = ('.*', )
        else:
        if class_names_compiled is None:
            self.class_names_compiled = re.compile(self.class_names)
        else:
            self.class_names_compiled = class_names_compiled"""

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_source(self):
        return self.source

    def set_source(self, source):
        self.source = source

    def get_class_names(self):
        return self.class_names

    def set_class_names(self, class_names):
        self.class_names = class_names
        self.class_names_compiled = re.compile(class_names)

    def get_class_names_compiled(self):
        return self.class_names_compiled

    def set_class_names_compiled(self, class_names_compiled):
        self.class_names_compiled = class_names_compiled

    def match_name(self, class_name):
        """Match against the name of the class currently being generated.
        If this method returns True, the method will be inserted in
          the generated class.
        """

        if self.class_names == class_name or (
            isinstance(self.class_names, list) and class_name in self.class_names
        ):
            return True
        else:
            return False

    def get_interpolated_source(self, values_dict):
        """Get the method source code, interpolating values from values_dict
        into it.  The source returned by this method is inserted into
        the generated class.
        """
        source = self.source % values_dict
        source = source.replace("PERCENTAGE", "%")
        return source

    def show(self):
        print("specification:")
        print("    name: %s" % (self.name,))
        print(self.source)
        print("    class_names: %s" % (self.class_names,))
        print("    names pat  : %s" % (self.class_names_compiled.pattern,))


#
# Provide one or more method specification such as the following.
# Notes:
# - Each generated class contains a class variable _member_data_items.
#   This variable contains a list of instances of class _MemberSpec.
#   See the definition of class _MemberSpec near the top of the
#   generated superclass file and also section "User Methods" in
#   the documentation, as well as the examples below.

num_segments = MethodSpec(
    name="num_segments",
    source='''\
    @property
    def num_segments(self):
        """Get the number of segments included in this cell morphology.

        :returns: number of segments
        :rtype: int
        """
        return len(self.segments)
''',
    class_names=("Morphology"),
)


length = MethodSpec(
    name="length",
    source='''\
    @property
    def length(self):
        """Get the length of the segment.

        :returns: length of the segment
        :rtype: float
        """

        if self.proximal==None:
            raise Exception('Cannot get length of segment '+str(self.id)+' using the length property, since no proximal point is set on it (the proximal point comes from the parent segment). Use the method get_segment_length(segment_id) on the cell instead.')

        prox_x = self.proximal.x
        prox_y = self.proximal.y
        prox_z = self.proximal.z

        dist_x = self.distal.x
        dist_y = self.distal.y
        dist_z = self.distal.z

        length = ((prox_x-dist_x)**2 + (prox_y-dist_y)**2 + (prox_z-dist_z)**2)**(0.5)

        return length

    def __str__(self):

        return "<Segment|"+str(self.id)+("|"+self.name if self.name is not None else '') + ">"

    def __repr__(self):

        return str(self)

''',
    class_names=("Segment"),
)

volume = MethodSpec(
    name="volume",
    source='''\
    @property
    def volume(self):
        """Get the volume of the segment.

        :returns: volume of segment
        :rtype: float
        """
        if self.proximal==None:
            raise Exception('Cannot get volume of segment '+str(self.id)+' using the volume property, since no proximal point is set on it (the proximal point comes from the parent segment). Use the method get_segment_volume(segment_id) on the cell instead.')

        prox_rad = self.proximal.diameter/2.0
        dist_rad = self.distal.diameter/2.0

        if self.proximal.x == self.distal.x and \
           self.proximal.y == self.distal.y and \
           self.proximal.z == self.distal.z:

           if prox_rad!=dist_rad:
                raise Exception('Cannot get volume of segment '+str(self.id)+'. The (x,y,z) coordinates of the proximal and distal points match (i.e. it is a sphere), but the diameters of these points are different, making the volume calculation ambiguous.')

           return 4.0/3 * pi * prox_rad**3

        length = self.length

        volume = (pi/3)*length*(prox_rad**2+dist_rad**2+prox_rad*dist_rad)

        return volume
    ''',
    class_names=("Segment"),
)


surface_area = MethodSpec(
    name="surface_area",
    source='''\

    @property
    def surface_area(self):
        """Get the surface area of the segment.

        :returns: surface area of segment
        :rtype: float
        """
        if self.proximal==None:
            raise Exception('Cannot get surface area of segment '+str(self.id)+' using the surface_area property, since no proximal point is set on it (the proximal point comes from the parent segment). Use the method get_segment_surface_area(segment_id) on the cell instead.')

        prox_rad = self.proximal.diameter/2.0
        dist_rad = self.distal.diameter/2.0

        if self.proximal.x == self.distal.x and \
           self.proximal.y == self.distal.y and \
           self.proximal.z == self.distal.z:

           if prox_rad!=dist_rad:
                raise Exception('Cannot get surface area of segment '+str(self.id)+'. The (x,y,z) coordinates of the proximal and distal points match (i.e. it is a sphere), but the diameters of these points are different, making the surface area calculation ambiguous.')

           return 4.0 * pi * prox_rad**2

        length = self.length

        surface_area = pi*(prox_rad+dist_rad)*sqrt((prox_rad-dist_rad)**2+length**2)

        return surface_area
    ''',
    class_names=("Segment"),
)

#
# Provide a list of your method specifications.
#   This list of specifications must be named METHOD_SPECS.
#
METHOD_SPECS = (length, volume, surface_area, num_segments)


seg_grp = MethodSpec(
    name="SegmentGroup",
    source="""\


    def __str__(self):

        return "SegmentGroup: "+str(self.id)+", "+str(len(self.members))+" member(s), "+str(len(self.includes))+" included group(s)"

    def __repr__(self):

        return str(self)

""",
    class_names=("SegmentGroup"),
)

METHOD_SPECS += (seg_grp,)

seg_grp = MethodSpec(
    name="Point3DWithDiam",
    source='''\

    def __str__(self):

        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+"), diam "+str(self.diameter)+"um"

    def __repr__(self):

        return str(self)

    def distance_to(self, other_3d_point) -> float:
        """Find the distance between this point and another.

        :param other_3d_point: other 3D point to calculate distance to
        :type other_3d_point: Point3DWithDiam
        :returns: distance between the two points
        :rtype: float
        """
        a_x = self.x
        a_y = self.y
        a_z = self.z

        b_x = other_3d_point.x
        b_y = other_3d_point.y
        b_z = other_3d_point.z

        distance = ((a_x-b_x)**2 + (a_y-b_y)**2 + (a_z-b_z)**2)**(0.5)
        return distance

''',
    class_names=("Point3DWithDiam"),
)

METHOD_SPECS += (seg_grp,)


connection_cell_ids = MethodSpec(
    name="connection_cell_ids",
    source='''\

    def _get_cell_id(self, id_string: str) -> int:
        if '[' in id_string:
            return int(id_string.split('[')[1].split(']')[0])
        else:
            return int(id_string.split('/')[2])

    def get_pre_cell_id(self) -> str:
        """Get the ID of the pre-synaptic cell

        :returns: ID of pre-synaptic cell
        :rtype: str
        """

        return self._get_cell_id(self.pre_cell_id)

    def get_post_cell_id(self) -> str:
        """Get the ID of the post-synaptic cell

        :returns: ID of post-synaptic cell
        :rtype: str
        """

        return self._get_cell_id(self.post_cell_id)

    def get_pre_segment_id(self) -> str:
        """Get the ID of the pre-synpatic segment

        :returns: ID of pre-synaptic segment.
        :rtype: str
        """

        return int(self.pre_segment_id)

    def get_post_segment_id(self) -> str:
        """Get the ID of the post-synpatic segment

        :returns: ID of post-synaptic segment.
        :rtype: str
        """

        return int(self.post_segment_id)

    def get_pre_fraction_along(self):
        """Get pre-synaptic fraction along information"""

        return float(self.pre_fraction_along)

    def get_post_fraction_along(self):
        """Get post-synaptic fraction along information"""

        return float(self.post_fraction_along)


    def get_pre_info(self):
        """Get pre-synaptic information summary"""

        return str(self.get_pre_cell_id())+(':'+str(self.get_pre_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_pre_fraction_along()+')' if self.get_pre_segment_id()!=0 or self.get_pre_fraction_along()!=0.5 else '')

    def get_post_info(self):
        """Get post-synaptic information summary"""

        return str(self.get_post_cell_id())+(':'+str(self.get_post_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_post_fraction_along()+')' if self.get_post_segment_id()!=0 or self.get_post_fraction_along()!=0.5 else '')

    def __str__(self):

        return "Connection "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())

    ''',
    class_names=(["Connection", "ConnectionWD"]),
)

METHOD_SPECS += (connection_cell_ids,)

connection_wd_cell_ids = MethodSpec(
    name="connection_wd_cell_ids",
    source='''\

    def __str__(self):

        return "Connection "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", weight: "+'PERCENTAGEf' PERCENTAGE (float(self.weight))+", delay: "+'PERCENTAGE.5f' PERCENTAGE (self.get_delay_in_ms())+" ms"

    def get_delay_in_ms(self) -> float:
        """Get connection delay in milli seconds

        :returns: connection delay in milli seconds
        :rtype: float
        """
        if 'ms' in self.delay:
            return float(self.delay[:-2].strip())
        elif 's' in self.delay:
            return float(self.delay[:-1].strip())*1000.0

    ''',
    class_names=("ConnectionWD"),
)

METHOD_SPECS += (connection_wd_cell_ids,)

elec_connection_instance_cell_ids = MethodSpec(
    name="elec_connection_instance_cell_ids",
    source="""\

    def _get_cell_id(self, id_string):
        if '[' in id_string:
            return int(id_string.split('[')[1].split(']')[0])
        else:
            return int(id_string.split('/')[2])

    def __str__(self):

        return "Electrical Connection (Instance based) "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", synapse: "+str(self.synapse)


    """,
    class_names=("ElectricalConnectionInstance"),
)

METHOD_SPECS += (elec_connection_instance_cell_ids,)

elec_connection_instance_w = MethodSpec(
    name="elec_connection_instance_w",
    source='''\

    def get_weight(self) -> float:
        """Get the weight of the connection

        If a weight is not set (or is set to None), returns the default value
        of 1.0.

        :returns: weight of connection or 1.0 if not set
        :rtype: float
        """

        return float(self.weight) if self.weight!=None else 1.0

    def __str__(self):

        return "Electrical Connection (Instance based & weight) "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", synapse: "+str(self.synapse) + ", weight: "+'PERCENTAGE.6f'PERCENTAGEself.get_weight()

    ''',
    class_names=("ElectricalConnectionInstanceW"),
)

METHOD_SPECS += (elec_connection_instance_w,)

elec_connection_cell_ids = MethodSpec(
    name="elec_connection_cell_ids",
    source='''\

    def _get_cell_id(self, id_string: str) -> int:
            return int(float(id_string))

    def get_pre_cell_id(self) -> float:
        """Get the ID of the pre-synaptic cell

        :returns: ID of pre-synaptic cell
        :rtype: str
        """

        return self._get_cell_id(self.pre_cell)

    def get_post_cell_id(self) -> str:
        """Get the ID of the post-synaptic cell

        :returns: ID of post-synaptic cell
        :rtype: str
        """

        return self._get_cell_id(self.post_cell)

    def get_pre_segment_id(self) -> str:
        """Get the ID of the pre-synpatic segment

        :returns: ID of pre-synaptic segment.
        :rtype: str
        """

        return int(self.pre_segment)

    def get_post_segment_id(self) -> str:
        """Get the ID of the post-synpatic segment

        :returns: ID of post-synaptic segment.
        :rtype: str
        """

        return int(self.post_segment)

    def get_pre_fraction_along(self):
        """Get pre-synaptic fraction along information"""

        return float(self.pre_fraction_along)

    def get_post_fraction_along(self):
        """Get post-synaptic fraction along information"""

        return float(self.post_fraction_along)


    def get_pre_info(self):
        """Get pre-synaptic information summary"""

        return str(self.get_pre_cell_id())+(':'+str(self.get_pre_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_pre_fraction_along()+')' if self.get_pre_segment_id()!=0 or self.get_pre_fraction_along()!=0.5 else '')

    def get_post_info(self):
        """Get post-synaptic information summary"""

        return str(self.get_post_cell_id())+(':'+str(self.get_post_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_post_fraction_along()+')' if self.get_post_segment_id()!=0 or self.get_post_fraction_along()!=0.5 else '')


    def __str__(self):

        return "Electrical Connection "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", synapse: "+str(self.synapse)


    ''',
    class_names=("ElectricalConnection"),
)

METHOD_SPECS += (elec_connection_cell_ids,)

cont_connection_instance_cell_ids = MethodSpec(
    name="cont_connection_instance_cell_ids",
    source="""\

    def _get_cell_id(self, id_string):
        if '[' in id_string:
            return int(id_string.split('[')[1].split(']')[0])
        else:
            return int(id_string.split('/')[2])


    def __str__(self):

        return "Continuous Connection (Instance based) "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", pre comp: "+str(self.pre_component)+", post comp: "+str(self.post_component)


    """,
    class_names=("ContinuousConnectionInstance"),
)

METHOD_SPECS += (cont_connection_instance_cell_ids,)

cont_connection_instance_w = MethodSpec(
    name="cont_connection_instance_w",
    source='''\

    def get_weight(self):
        """Get weight.

        If weight is not set, the default value of 1.0 is returned.
        """

        return float(self.weight) if self.weight!=None else 1.0

    def __str__(self):

        return "Continuous Connection (Instance based & weight) "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", pre comp: "+str(self.pre_component)+", post comp: "+str(self.post_component)+", weight: "+'PERCENTAGE.6f'PERCENTAGEself.get_weight()


    ''',
    class_names=("ContinuousConnectionInstanceW"),
)

METHOD_SPECS += (cont_connection_instance_w,)

cont_connection_cell_ids = MethodSpec(
    name="cont_connection_cell_ids",
    source='''\

    def _get_cell_id(self, id_string):
            return int(float(id_string))


    def get_pre_cell_id(self) -> str:
        """Get the ID of the pre-synaptic cell

        :returns: ID of pre-synaptic cell
        :rtype: str
        """

        return self._get_cell_id(self.pre_cell)

    def get_post_cell_id(self) -> str:
        """Get the ID of the post-synaptic cell

        :returns: ID of post-synaptic cell
        :rtype: str
        """

        return self._get_cell_id(self.post_cell)

    def get_pre_segment_id(self) -> str:
        """Get the ID of the pre-synpatic segment

        :returns: ID of pre-synaptic segment.
        :rtype: str
        """

        return int(self.pre_segment)

    def get_post_segment_id(self) -> str:
        """Get the ID of the post-synpatic segment

        :returns: ID of post-synaptic segment.
        :rtype: str
        """

        return int(self.post_segment)

    def get_pre_fraction_along(self):
        """Get pre-synaptic fraction along information"""

        return float(self.pre_fraction_along)

    def get_post_fraction_along(self):
        """Get post-synaptic fraction along information"""

        return float(self.post_fraction_along)


    def get_pre_info(self):
        """Get pre-synaptic information summary"""

        return str(self.get_pre_cell_id())+(':'+str(self.get_pre_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_pre_fraction_along()+')' if self.get_pre_segment_id()!=0 or self.get_pre_fraction_along()!=0.5 else '')

    def get_post_info(self):
        """Get post-synaptic information summary"""

        return str(self.get_post_cell_id())+(':'+str(self.get_post_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_post_fraction_along()+')' if self.get_post_segment_id()!=0 or self.get_post_fraction_along()!=0.5 else '')


    def __str__(self):

        return "Continuous Connection "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", pre comp: "+str(self.pre_component)+", post comp: "+str(self.post_component)


    ''',
    class_names=("ContinuousConnection"),
)

METHOD_SPECS += (cont_connection_cell_ids,)


instance = MethodSpec(
    name="instance",
    source="""\

    def __str__(self):

        return "Instance "+str(self.id)+ (" at location: "+str(self.location) if self.location else "")

    def __repr__(self):

        return str(self)

""",
    class_names=("Instance"),
)
METHOD_SPECS += (instance,)


location = MethodSpec(
    name="location",
    source="""\

    def _format(self,value):

        if int(value)==value:
            return str(int(value))
        else:
            return 'PERCENTAGE.4f' PERCENTAGE value

    def __str__(self):

        return "("+ self._format(self.x) +", "+ self._format(self.y) +", "+ self._format(self.z) +")"

    def __repr__(self):

        return str(self)

""",
    class_names=("Location"),
)
METHOD_SPECS += (location,)


input_cell_ids = MethodSpec(
    name="input_cell_ids",
    source='''\

    def _get_cell_id(self, id_string):
        if '[' in id_string:
            return int(id_string.split('[')[1].split(']')[0])
        else:
            return int(id_string.split('/')[2])

    def get_target_cell_id(self):
        """Get ID of target cell.  """

        return self._get_cell_id(self.target)

    def get_segment_id(self):
        """Get the ID of the segment.

        Returns 0 if segment_id was not set.
        """
        return int(self.segment_id) if self.segment_id else 0

    def get_fraction_along(self):
        """Get fraction along.

        Returns 0.5 is fraction_along was not set.
        """

        return float(self.fraction_along) if self.fraction_along else 0.5

    def __str__(self):

        return "Input "+str(self.id)+": "+str(self.get_target_cell_id())+":"+str(self.get_segment_id())+"("+'PERCENTAGE.6f'PERCENTAGEself.get_fraction_along()+")"

    ''',
    class_names=(["Input", "ExplicitInput"]),
)

METHOD_SPECS += (input_cell_ids,)


input_w = MethodSpec(
    name="input_w",
    source='''\

    def get_weight(self):
        """Get weight.

        If weight is not set, the default value of 1.0 is returned.
        """

        return float(self.weight) if self.weight!=None else 1.0

    def __str__(self):

        return "Input (weight) "+str(self.id)+": "+str(self.get_target_cell_id())+":"+str(self.get_segment_id())+"("+'PERCENTAGE.6f'PERCENTAGEself.get_fraction_along()+"), weight: "+'PERCENTAGE.6f'PERCENTAGEself.get_weight()

    ''',
    class_names=(["InputW"]),
)

METHOD_SPECS += (input_w,)


nml_doc_summary = MethodSpec(
    name="summary",
    source='''\


    def summary(self, show_includes=True, show_non_network=True):
        """Get a pretty-printed summary of the complete NeuroMLDocument.

        This includes information on the various Components included in the
        NeuroMLDocument: networks, cells, projections, synapses, and so on.
        """


        info = "*******************************************************\\n"
        info+="* NeuroMLDocument: "+self.id+"\\n*\\n"
        post = ""
        membs = inspect.getmembers(self)
        for memb in membs:
            if isinstance(memb[1], list) and len(memb[1])>0 and not memb[0].endswith('_') and not memb[0] == 'networks':
                if (memb[0] == 'includes' and show_includes) or (not memb[0] == 'includes' and show_non_network):
                    post = "*\\n"
                    info+="*  "+str(memb[1][0].__class__.__name__)+": "
                    listed = []
                    for entry in memb[1]:
                        if hasattr(entry,'id'):
                            listed.append(str(entry.id))
                        elif hasattr(entry,'name'):
                            listed.append(str(entry.name))
                        elif hasattr(entry,'href'):
                            listed.append(str(entry.href))
                        elif hasattr(entry,'tag'):
                            listed.append(str(entry.tag)+" = "+str(entry.value))
                    info+= str(sorted(listed))+"\\n"
        info+= post

        for network in self.networks:
            info+="*  Network: "+network.id
            if network.temperature:
                info+=" (temperature: "+network.temperature+")"
            info+="\\n*\\n"
            tot_pop =0
            tot_cells = 0
            pop_info = ""
            for pop in sorted(network.populations, key=lambda x: x.id):
                pop_info+="*     "+str(pop)+"\\n"
                tot_pop+=1
                tot_cells+=pop.get_size()
                if len(pop.instances)>0:
                    loc = pop.instances[0].location
                    pop_info+="*       Locations: ["+str(loc)+", ...]\\n"
                if len(pop.properties)>0:
                    pop_info+="*       Properties: "
                    for p in pop.properties:
                        pop_info+=(str(p.tag)+'='+str(p.value)+'; ')
                    pop_info+="\\n"

            info+="*   "+str(tot_cells)+" cells in "+str(tot_pop)+" populations \\n"+pop_info+"*\\n"


            tot_proj =0
            tot_conns = 0

            proj_info = ""
            for proj in sorted(network.projections, key=lambda x: x.id):
                proj_info+="*     "+str(proj)+"\\n"
                tot_proj+=1
                tot_conns+=len(proj.connections)
                tot_conns+=len(proj.connection_wds)
                if len(proj.connections)>0:
                    proj_info+="*       "+str(len(proj.connections))+" connections: [("+str(proj.connections[0])+"), ...]\\n"
                if len(proj.connection_wds)>0:
                    proj_info+="*       "+str(len(proj.connection_wds))+" connections (wd): [("+str(proj.connection_wds[0])+"), ...]\\n"

            for proj in sorted(network.electrical_projections, key=lambda x: x.id):
                proj_info+="*     Electrical projection: "+proj.id+" from "+proj.presynaptic_population+" to "+proj.postsynaptic_population+"\\n"
                tot_proj+=1
                tot_conns+=len(proj.electrical_connections)
                tot_conns+=len(proj.electrical_connection_instances)
                tot_conns+=len(proj.electrical_connection_instance_ws)
                if len(proj.electrical_connections)>0:
                    proj_info+="*       "+str(len(proj.electrical_connections))+" connections: [("+str(proj.electrical_connections[0])+"), ...]\\n"
                if len(proj.electrical_connection_instances)>0:
                    proj_info+="*       "+str(len(proj.electrical_connection_instances))+" connections: [("+str(proj.electrical_connection_instances[0])+"), ...]\\n"
                if len(proj.electrical_connection_instance_ws)>0:
                    proj_info+="*       "+str(len(proj.electrical_connection_instance_ws))+" connections: [("+str(proj.electrical_connection_instance_ws[0])+"), ...]\\n"

            for proj in sorted(network.continuous_projections, key=lambda x: x.id):
                proj_info+="*     Continuous projection: "+proj.id+" from "+proj.presynaptic_population+" to "+proj.postsynaptic_population+"\\n"
                tot_proj+=1
                tot_conns+=len(proj.continuous_connections)
                tot_conns+=len(proj.continuous_connection_instances)
                tot_conns+=len(proj.continuous_connection_instance_ws)
                if len(proj.continuous_connections)>0:
                    proj_info+="*       "+str(len(proj.continuous_connections))+" connections: [("+str(proj.continuous_connections[0])+"), ...]\\n"
                if len(proj.continuous_connection_instances)>0:
                    proj_info+="*       "+str(len(proj.continuous_connection_instances))+" connections: [("+str(proj.continuous_connection_instances[0])+"), ...]\\n"
                if len(proj.continuous_connection_instance_ws)>0:
                    proj_info+="*       "+str(len(proj.continuous_connection_instance_ws))+" connections (w): [("+str(proj.continuous_connection_instance_ws[0])+"), ...]\\n"

            info+="*   "+str(tot_conns)+" connections in "+str(tot_proj)+" projections \\n"+proj_info+"*\\n"

            if len(network.synaptic_connections)>0:
                info+="*   "+str(len(network.synaptic_connections))+" explicit synaptic connections (outside of projections)\\n"
                for sc in network.synaptic_connections:
                    info+="*     "+str(sc)+"\\n"
                info+="*\\n"

            tot_input_lists = 0
            tot_inputs = 0
            input_info = ""
            for il in sorted(network.input_lists, key=lambda x: x.id):
                input_info+="*     "+str(il)+"\\n"
                tot_input_lists += 1
                if len(il.input)>0:
                    input_info+="*       "+str(len(il.input))+" inputs: [("+str(il.input[0])+"), ...]\\n"
                    tot_inputs+=len(il.input)
                if len(il.input_ws)>0:
                    input_info+="*       "+str(len(il.input_ws))+" inputs: [("+str(il.input_ws[0])+"), ...]\\n"
                    tot_inputs+=len(il.input_ws)

            info+="*   "+str(tot_inputs)+" inputs in "+str(tot_input_lists)+" input lists \\n"+input_info+"*\\n"

            if len(network.explicit_inputs)>0:
                info+="*   "+str(len(network.explicit_inputs))+" explicit inputs (outside of input lists)\\n"
                for el in network.explicit_inputs:
                    info+="*     "+str(el)+"\\n"
                info+="*\\n"


        info+="*******************************************************"

        return info

    warn_count = 0

    def get_by_id(self, id: str) -> typing.Optional[typing.Any]:
        """Get a component by specifying its ID.

        :param id: id of Component to get
        :type id: str
        :returns: Component with given ID or None if no Component with provided ID was found
        """
        if len(id)==0:
            callframe = inspect.getouterframes(inspect.currentframe(), 2)
            print('Method: '+ callframe[1][3] + ' is asking for an element with no id...')

            return None
        all_ids = []
        for ms in self.member_data_items_:
            mlist = getattr(self, ms.get_name())
            # TODO: debug why this is required
            if mlist is None:
                continue
            for m in mlist:
                if hasattr(m,"id"):
                    if m.id == id:
                        return m
                    else:
                        all_ids.append(m.id)
        if self.warn_count<10:
            neuroml.print_("Id "+id+" not found in <neuroml> element. All ids: "+str(sorted(all_ids)))
            self.warn_count+=1
        elif self.warn_count==10:
            neuroml.print_(" - Suppressing further warnings about id not found...")
        return None

    def append(self, element):
        """Append an element

        :param element: element to append
        :type element: Object
        """
        self.add(element)

    ''',
    class_names=("NeuroMLDocument"),
)

METHOD_SPECS += (nml_doc_summary,)

network_get_by_id = MethodSpec(
    name="get_by_id",
    source='''\

    warn_count = 0
    def get_by_id(self, id: str) -> typing.Optional[typing.Any]:
        """Get a component by its ID

        :param id: ID of component to find
        :type id: str
        :returns:  component with specified ID or None if no component with specified ID found
        """
        all_ids = []
        for ms in self.member_data_items_:
            mlist = getattr(self, ms.get_name())
            # TODO: debug why this is required
            if mlist is None:
                continue
            for m in mlist:
                if hasattr(m,"id"):
                    if m.id == id:
                        return m
                    else:
                        all_ids.append(m.id)
        if self.warn_count<10:
            neuroml.print_("Id "+id+" not found in <network> element. All ids: "+str(sorted(all_ids)))
            self.warn_count+=1
        elif self.warn_count==10:
            neuroml.print_(" - Suppressing further warnings about id not found...")
        return None


    def __str__(self):

        return "Network "+str(self.id)+" with "+str(len(self.populations))+" population(s)"

    ''',
    class_names=("Network"),
)

METHOD_SPECS += (network_get_by_id,)


cell_methods = MethodSpec(
    name="cell_methods",
    source='''\

    # Get segment object by its id
    def get_segment(self, segment_id: int) -> Segment:
        """Get segment object by its id

        :param segment_id: ID of segment
        :return: segment

        :raises ValueError: if the segment is not found in the cell
        """

        for segment in self.morphology.segments:
            if segment.id == segment_id:
                return segment

        raise ValueError("Segment with id "+str(segment_id)+" not found in cell "+str(self.id))

    def get_segments_by_substring(self, substring: str) -> typing.Dict[str, Segment]:
        """Get a dictionary of segment IDs and the segment matching the specified substring

        :param substring: substring to match
        :type substring: str
        :return: dictionary with segment ID as key, and segment as value
        :raises Exception: if no segments are found

        """
        segments = {}
        if substring:
            for segment in self.morphology.segments:
                if substring in segment.id:
                    segments[segment.id] = segment
        if len(segments) == 0:
            raise Exception("Segments with id matching "+str(substring)+" not found in cell "+str(self.id))
        return segments


    # Get the proximal point of a segment, even the proximal field is None and
    # so the proximal point is on the parent (at a point set by fraction_along)
    def get_actual_proximal(self, segment_id: str):
        """Get the proximal point of a segment.

        If the proximal for the segment is set to None, calculate the proximal
        on the parent using fraction_along and return it.

        :param segment_id: ID of segment
        :return: proximal point
        """

        segment = self.get_segment(segment_id)
        if segment.proximal:
            return segment.proximal

        parent = self.get_segment(segment.parent.segments)
        fract = float(segment.parent.fraction_along)
        if fract==1:
            return parent.distal
        elif fract==0:
            return self.get_actual_proximal(segment.parent.segments)
        else:
            pd = parent.distal
            pp = self.get_actual_proximal(segment.parent.segments)
            # pp + f(pd - pp) = (1 - f)pp + f*pd
            p = Point3DWithDiam(x=(1-fract)*pp.x+fract*pd.x, y=(1-fract)*pp.y+fract*pd.y, z=(1-fract)*pp.z+fract*pd.z)
            p.diameter = (1-fract)*pp.diameter+fract*pd.diameter

            return p

    def get_segment_length(self, segment_id: str) -> float:
        """Get the length of the segment.

        :param segment_id: ID of segment
        :return: length of segment
        """

        segment = self.get_segment(segment_id)
        if segment.proximal:
            return segment.length
        else:
            prox = self.get_actual_proximal(segment_id)

            length = segment.distal.distance_to(prox)

            return length

    def get_segment_surface_area(self, segment_id: str) -> float:
        """Get the surface area of the segment.

        :param segment_id: ID of the segment
        :return: surface area of segment
        """

        segment = self.get_segment(segment_id)
        if segment.proximal:
            return segment.surface_area
        else:
            prox = self.get_actual_proximal(segment_id)

            temp_seg = Segment(distal=segment.distal, proximal=prox)

            return temp_seg.surface_area

    def get_segment_volume(self, segment_id: str) -> float:
        """Get volume of segment

        :param segment_id: ID of the segment
        :return: volume of the segment
        """
        segment = self.get_segment(segment_id)
        if segment.proximal:
            return segment.volume
        else:
            prox = self.get_actual_proximal(segment_id)

            temp_seg = Segment(distal=segment.distal, proximal=prox)

            return temp_seg.volume

    def get_segment_ids_vs_segments(self) -> typing.Dict[str, Segment]:
        """Get a dictionary of segment IDs and the segments in the cell.

        :return: dictionary with segment ID as key, and segment as value
        """

        segments = {}
        for segment in self.morphology.segments:
            segments[segment.id] = segment

        return segments

    def get_all_segments_in_group(self,
                                  segment_group: typing.Union[str, SegmentGroup],
                                  assume_all_means_all: bool = True) -> typing.List[int]:
        """Get all the segments in a segment group of the cell.

        :param segment_group: segment group id (str) or object (SegmentGroup) to get all segments of
        :param assume_all_means_all: return all segments if the "all" segment
            group wasn't explicitly defined
        :return: list of segment ids
        :rtype: list[int]

        :raises Exception: if no segment group is found in the cell.
        """

        if isinstance(segment_group, str):
            for sg in self.morphology.segment_groups:
                if sg.id == segment_group:
                    segment_group = sg
            if isinstance(segment_group, str):

                if assume_all_means_all and segment_group=='all': # i.e. wasn't explicitly defined, but assume it means all segments
                    return [seg.id for seg in self.morphology.segments]

                raise Exception('No segment group '+segment_group+ ' found in cell '+self.id)

        all_segs = []

        for member in segment_group.members:
            if not member.segments in all_segs:
                all_segs.append(member.segments)


        for include in segment_group.includes:
            segs_here = self.get_all_segments_in_group(include.segment_groups)
            for s in segs_here:
                if not s in all_segs:
                    all_segs.append(s)

        return all_segs


    def get_ordered_segments_in_groups(self,
                                       group_list: typing.List[str],
                                       check_parentage: bool = False,
                                       include_cumulative_lengths: bool = False,
                                       include_path_lengths: bool = False,
                                       path_length_metric: str = "Path Length from root" # Only option supported
                                       ) -> typing.Any:
        """
        Get ordered list of segments in specified groups, with additional
        information.

        Note that this method orders segments by id, so the assumption is that
        all segment with id `N + m` will be a descendent of segment with id `N`
        in the segment group.

        :param group_list: a group id or list of group ids to get segments from
        :type group_list: str or list(str)
        :param check_parentage: verify parentage
        :type check_parentage: bool
        :param include_cumulative_lengths: also include cummulative length of
            each segment from root
        :type include_cumulative_lengths: bool
        :param include_path_lengths: also include path lengths from segment
            group's root segment to proximal and distal points of each segment
        :type include_path_lengths: bool
        :param path_length_metric: metric to use for path length ("Path Length
            from root" is currently the only supported option, and the default)
        :type path_length_metric: str

        :returns: depending on provided arguments:

                - if no additional options are provided, returns a dictionary
                  with segment group ids as keys, and lists of ordered segments
                  in those segment groups as values (`ord_segs`)
                - if only `include_path_lengths` is set, returns a tuple:
                  `[ord_segs, path_lengths_to_proximal ,
                  path_lengths_to_distal]`
                - if only `include_cumulative_lengths` is set, returns a tuple:
                  `[ord_segs, cumulative_lengths]`
                - if both `include_path_lengths` and
                  `include_cumulative_lengths` are set, returns a tuple:
                  `[ord_segs, cumulative_lengths, path_lengths_to_proximal ,
                  path_lengths_to_distal]`

        :raises: Exception if check_parentage is True and parentage cannot be verified
        """

        unord_segs = {}
        other_segs = {}

        # convert to list if a single segment group ID has been provided
        if isinstance(group_list, str):
            group_list = [group_list]

        # populate the dict to ensure that the order of segment groups is
        # maintained in the returned result
        for sgid in group_list:
            unord_segs[sgid] = None

        # get a dict of all segments in the cell, with their ids as keys
        segments = self.get_segment_ids_vs_segments()

        # get list of segments in all segment groups
        # and store this information in two dicts:
        # - unord_segs: for segment groups in group_list
        # - other_segs: for segment groups not in group_list
        for sg in self.morphology.segment_groups:
            # get all segments in a segment group
            all_segs_here = self.get_all_segments_in_group(sg)

            if sg.id in group_list:
                unord_segs[sg.id] = [segments[s] for s in all_segs_here]
            else:
                other_segs[sg.id] = [segments[s] for s in all_segs_here]

        ord_segs = {}

        # sort unord_segs by id to get an ordered list in ord_segs
        for key, segs in unord_segs.items():
            if segs is not None:
                if len(segs)==1 or len(segs)==0:
                    ord_segs[key]=segs
                else:
                    ord_segs[key]=sorted(segs,key=attrgetter('id'),reverse=False)

        if check_parentage:
            # check parent ordering

            for key in ord_segs.keys():
                existing_ids = []
                for s in ord_segs[key]:
                    if s.id != ord_segs[key][0].id:
                        if not s.parent or not s.parent.segments in existing_ids:
                            raise Exception("Problem with finding parent of seg: "+str(s)+" in list: "+str(ord_segs))
                    existing_ids.append(s.id)


        if include_cumulative_lengths or include_path_lengths:
            cumulative_lengths = {}
            path_lengths_to_proximal = {}
            path_lengths_to_distal = {}

            for key in ord_segs.keys():
                cumulative_lengths[key] = []
                path_lengths_to_proximal[key] = {}
                path_lengths_to_distal[key] = {}

                tot_len = 0
                for seg in ord_segs[key]:

                    length = self.get_segment_length(seg.id)

                    if not seg.parent or not seg.parent.segments in path_lengths_to_distal[key]:

                        path_lengths_to_proximal[key][seg.id] = 0
                        last_seg = seg
                        par_seg_element = seg.parent
                        while par_seg_element!=None:

                            par_seg = segments[par_seg_element.segments]
                            par_length = self.get_segment_length(par_seg.id)

                            fract = float(last_seg.parent.fraction_along)
                            path_lengths_to_proximal[key][seg.id] += par_length*fract

                            last_seg = par_seg
                            par_seg_element = par_seg.parent


                    else:
                        pd = path_lengths_to_distal[key][seg.parent.segments]
                        pp = path_lengths_to_proximal[key][seg.parent.segments]
                        fract = float(seg.parent.fraction_along)

                        path_lengths_to_proximal[key][seg.id] = pp + (pd - pp)*fract

                    path_lengths_to_distal[key][seg.id] = path_lengths_to_proximal[key][seg.id] + length

                    tot_len += length
                    cumulative_lengths[key].append(tot_len)


        if include_path_lengths and not include_cumulative_lengths:

            return ord_segs, path_lengths_to_proximal, path_lengths_to_distal

        if include_cumulative_lengths and not include_path_lengths:

            return ord_segs, cumulative_lengths

        if include_cumulative_lengths and include_path_lengths:

            return ord_segs, cumulative_lengths, path_lengths_to_proximal, path_lengths_to_distal

        return ord_segs

    def get_segment_group(self, sg_id: str) -> SegmentGroup:
        """Return the SegmentGroup object for the specified segment group id.

        :param sg_id: id of segment group to find
        :type sg_id: str
        :returns: SegmentGroup object of specified ID
        :raises ValueError: if segment group is not found in cell
        """
        if sg_id:
            for sg in self.morphology.segment_groups:
                if sg.id == sg_id:
                    return sg

        raise ValueError("Segment group with id "+str(sg_id)+" not found in cell "+str(self.id))

    def get_segment_groups_by_substring(self, substring: str, unbranched: bool = False) -> typing.Dict[str, SegmentGroup]:
        """Get a dictionary of segment group IDs and the segment groups matching the specified substring

        :param substring: substring to match, an empty string "" matches all
            groups
        :type substring: str
        :param unbranced: toggle selecting unbranched segment groups
        :type unbranched: bool
        :return: dictionary with segment group ID as key, and segment group as value
        :raises ValueError: if no matching segment groups are found in cell
        """
        sgs = {}
        for sg in self.morphology.segment_groups:
            if substring == "" or substring in sg.id:
                if unbranched is True:
                    if sg.neuro_lex_id == neuroml.neuro_lex_ids.neuro_lex_ids["section"]:
                        sgs[sg.id] = sg
                else:
                    sgs[sg.id] = sg
        if len(sgs) == 0:
            raise ValueError("Segment group with id matching "+str(substring)+" not found in cell "+str(self.id))
        return sgs


    def summary(self, morph=True, biophys=True):
        """Print cell summary.

        Shows the number of segments and segment groups, and information on the
        biophysical properties of the cell. See the `morphinfo` and
        `biophysinfo` methods for more details.

        :param morph: toggle showing/hiding morphology information
        :type morph: bool
        :param biophys: toggle showing/hiding biophysology information
        :type biophys: bool
        :returns: None
        """

        print(f"*********** Summary ({self.id}) ************")
        print("* Notes: "+str(self.notes))
        print()

        if morph:
            print(f"*********** Morphology summary ({self.id}) ************")
            self.morphinfo()
            print("*******************************************************")
            print("Tip: use morphinfo(True) to see more detailed information.")

        if biophys:
            print(f"*********** Biophys summary ({self.id}) ************")
            self.biophysinfo()
            print("*******************************************************")


    def morphinfo(self, segment_detail=False):
        """Show info on morphology of the cell.
        By default, since cells can have large numbers of segments and segment
        groups, it only provides metrics on the total numbers. To see details,
        pass `segment_detail=True`.

        See also: `get_segment_group_info`.

        :param segment_detail: toggle whether to show detailed information on
            segment groups and their segments
        :type segment_detail: bool
        :returns: None

        """
        print("* Segments: "+str(len(self.morphology.segments)))
        print("* SegmentGroups: "+str(len(self.morphology.segment_groups)))

        if segment_detail:
            for sg in self.morphology.segment_groups:
                self.get_segment_group_info(sg.id)


    def biophysinfo(self):
        """Get information on the biophysical properties of the cell.
        :returns: None

        """
        bp = None
        mp = None
        ip = None
        if self.__class__.__name__ == "Cell":
            bp = self.biophysical_properties
            mp = bp.membrane_properties
            ip = bp.intracellular_properties
        elif self.__class__.__name__ == "Cell2CaPools":
            bp = self.biophysical_properties2_ca_pools
            mp = bp.membrane_properties2_ca_pools
            ip = bp.intracellular_properties2_ca_pools

        membp = mp.info(show_contents=True, return_format="dict")
        # check if there are any membrane properties
        for prop, val in membp.items():
            if len(val['members']) > 0:
                print(f"* Membrane properties")
                break

        for prop, val in membp.items():
            ctype = val['type']
            # objects
            ms = val['members']
            if len(ms) > 0:
                print(f"\t* {ctype}:")
                for am in ms:
                    inf = am.info(show_contents=True, return_format="dict")
                    for p, v in inf.items():
                        print(f"\t\t* {p}: {v['members']}")

                    print()

        intp = ip.info(show_contents=True, return_format="dict")
        for prop, val in intp.items():
            if len(val['members']) > 0:
                print(f"* Intracellular properties")
                break

        for prop, val in intp.items():
            ctype = val['type']
            # objects
            ms = val['members']
            if len(ms) > 0:
                print(f"\t* {ctype}:")
                for am in ms:
                    inf = am.info(show_contents=True, return_format="dict")
                    for p, v in inf.items():
                        print(f"\t\t* {p}: {v['members']}")

                    print()

    def get_segment_group_info(self, group_id):
        """Get information about a segment group

        :param group_id: id of segment group
        :type group_id: int
        :returns: None

        """
        print(f"* Segment group: {group_id}:")
        segs = self.get_all_segments_in_group(segment_group=group_id)
        for s in segs:
            sinfo = self.get_segment(s)
            print(f"\t * {s} (Parent: {sinfo.parent.segments if sinfo.parent else '-'}; {self.get_actual_proximal(s)} -> {sinfo.distal})")

    def add_segment(
        self,
        prox,
        dist,
        seg_id=None,
        name=None,
        parent=None,
        fraction_along=1.0,
        group_id=None,
        use_convention=True,
        seg_type=None,
        reorder_segment_groups=True,
        optimise_segment_groups=True

    ):
        """Add a segment to the cell, to the provided segment group, creating
        it if required.

        :param prox: proximal segment information
        :type prox: list with 4 float entries: [x, y, z, diameter]
        :param dist: dist segment information
        :type dist: list with 4 float entries: [x, y, z, diameter]
        :param seg_id: explicit ID to set for segment
            When not provided, the function will automatically add an ID based
            on the number of segments already included in the cell. It is best
            to either always set an explicit ID or let the function set it
            automatically, but not to mix the two. A `ValueError` is raised if
            a segment with the provided ID already exists
        :type seg_id: str
        :param name: name of segment
            If a name is given, it is used.
            If no name is given, but a segment group is provided, the segment
            is named: "Seg<number>_<group name>" where <number> is the number
            of the segment in the segment group. (to be read as "segment
            <number> in <group>"; the group name should indicate the type here)
            If no name is given, and no segment group is provided, the segment
            is simply named: "Seg<segment id>".
        :type name: str
        :seg_type: type of segment ("axon", "dendrite", "soma")
            If `use_convention` is `True`, and a `group_id` is provided, the
            segment group will also be added to the default segment groups if
            it has not been previously added. If `group_id` is `None`, the
            segment will be added to the default groups instead.

            If `use_convention` is `False`, this is unused.
        :type seg_type: str
        :param parent: parent segment object
        :type parent: Segment
        :param fraction_along: where the new segment is connected to the parent (0: distal point, 1: proximal point)
        :type fraction_along: float
        :param group_id: id of segment group to add the segment to
            If a segment group with this id does not exist, a new segment group
            will be created.

            The suggested convention is: `axon_`, `soma_`, `dend_` for axonal,
            somatic, and dendritic segment groups respectively.

            Note that a newly created segment group will not be marked as an
            unbranched segment group. If you wish to add a segment to an
            unbranched segment group, please create one using
            `add_unbranched_segment_group` and then add segments to it.
        :type group_id: str
        :param use_convention: whether the segment or its group should be added
            to the global segment groups. The `seg_type` notes what global
            group this segment or its segment group should also be added to.
        :type use_convention: bool
        :param reorder_segment_groups: whether the groups should be reordered
            to put the default segment groups last after the segment has been
            added.
            This is required for a valid NeuroML file because segment groups
            included in the default groups should be declared before they are
            used in the default groups. When adding lots of segments, one may
            want to only reorder at the end of the process instead of after
            each segment is added.

            This is only relevant if `use_convention=True`.
        :type reorder_segment_groups: bool
        :param optimise_segment_groups: toggle whether segment groups should be
            optimised after operation
        :type optimise_segment_groups: bool
        :returns: the created segment
        :rtype: Segment
        :raises ValueError: if `seg_id` is provided and a segment with this ID
            already exists

        """
        try:
            if prox:
                p = self.component_factory(
                    "Point3DWithDiam", x=prox[0], y=prox[1], z=prox[2], diameter=prox[3]
                )
            else:
                p = None
        except IndexError as e:
            print("{}: prox must be a list of 4 elements".format(e))
        try:
            d = self.component_factory(
                "Point3DWithDiam", x=dist[0], y=dist[1], z=dist[2], diameter=dist[3]
            )
        except IndexError as e:
            print("{}: dist must be a list of 4 elements".format(e))

        segid = len(self.morphology.segments)
        if segid > 0 and parent is None:
            raise Exception(
                "There are currently more than one segments in the cell, but one is being added without specifying a parent segment"
            )

        sp = (
            self.component_factory(
                "SegmentParent", segments=parent.id, fraction_along=fraction_along
            )
            if parent
            else None
        )

        if seg_id:
            try:
                seg = None
                seg = self.get_segment(seg_id)
                if seg:
                    raise ValueError(f"A segment with provided id {seg_id} already exists")
            except ValueError:
                # a segment with this ID does not already exist
                pass
        else:
            seg_id = segid

        segment = self.component_factory("Segment", id=seg_id, proximal=p, distal=d, parent=sp)

        seg_group = None
        if group_id:
            seg_group_default = None

            # cell.get_segment_group throws an exception of the segment group
            # does not exist
            try:
                seg_group = self.get_segment_group(group_id)
            except ValueError as e:
                print("Warning: {}".format(e))
                print(f"Warning: creating Segment Group with id {group_id}")
                seg_group = self.add_segment_group(
                    group_id=group_id
                )
            seg_group.members.append(Member(segments=segment.id))

        if use_convention:
            if not seg_type:
                raise ValueError("Please provide a seg_type")
            if seg_type == "axon":
                [seg_group_all, seg_group_default] = self.setup_default_segment_groups(use_convention=True, default_groups=["all", "axon_group"])
            elif seg_type == "soma":
                [seg_group_all, seg_group_default] = self.setup_default_segment_groups(use_convention=True, default_groups=["all", "soma_group"])
            elif seg_type == "dendrite":
                [seg_group_all, seg_group_default] = self.setup_default_segment_groups(use_convention=True, default_groups=["all", "dendrite_group"])
            else:
                raise ValueError(f"Invalid segment type provided: {seg_type}")

            # Now add the segment group that contains this segment if it exists
            # to the global groups. If a segment group does not exist for this
            # segment, add the segment itself to the global groups

            # Do not use add here, we do not need it's extra features (and
            # their performance costs)
            # De-duplicate/optimise later if required
            if seg_group and seg_group.id != seg_group_default.id:
                seg_group_default.includes.append(Include(segment_groups=seg_group.id))
                seg_group_all.includes.append(Include(segment_groups=seg_group.id))
            else:
                seg_group_default.members.append(Member(segments=segment.id))
                seg_group_all.members.append(Member(segments=segment.id))

            if reorder_segment_groups:
                self.reorder_segment_groups()

        if name:
            segment.name = name
        else:
            # set a default name based on the group membership if group
            # provided
            if group_id:
                # seg_group will exist by now: either it already existed or it
                # was created above
                segments_in_group = len(seg_group.members)
                segment_name = f"Seg{segments_in_group - 1}_{group_id}"
            else:
                # if it doesn't belong to a group, use the type to indicate
                # what kind of segment this is
                segment_name = f"Seg{seg_id}"
            segment.name = segment_name

        self.morphology.segments.append(segment)

        if optimise_segment_groups:
            self.optimise_segment_groups()

        return segment

    def add_segment_group(self, group_id, neuro_lex_id=None, notes=None):
        """Add a new general segment group.

        The segments included in this group do not need to be contiguous. This
        segment group will not be automatically marked as a section using the
        required NeuroLex ID.

        If a segment group with provided ID already exists, it will not be
        overwritten.

        :param group_id: ID of segment group
        :type group_id: str
        :param neuro_lex_id: NeuroLex ID to use for segment group
        :type neuro_lex_id: str
        :param notes: Notes text to add
        :type notes: str
        :returns: new segment group
        :rtype: SegmentGroup

        """
        seg_group = None
        try:
            seg_group = self.get_segment_group(group_id)
        except ValueError:
            seg_group = self.morphology.add(
                "SegmentGroup", id=group_id,
                neuro_lex_id=neuro_lex_id,
                notes=notes, validate=False
            )
        else:
            print(f"Warning: Segment group {seg_group.id} already exists.")

        return seg_group


    def add_unbranched_segment_group(self, group_id, notes=None):
        """Add a new unbranched segment group.

        This is similar to the `add_segment_group` method, but this segment
        group will be used to store contiguous segments, which form an
        unbranched section of a cell. It adds the NeuroLex ID for a neuronal
        branch to the segment group.

        :param group_id: ID of segment group
        :type group_id: str
        :param notes: notes to add
        :type notes: str
        :returns: new segment group
        :rtype: SegmentGroup

        """
        seg_group = self.add_segment_group(
            group_id=group_id, neuro_lex_id=neuroml.neuro_lex_ids.neuro_lex_ids["section"],
            notes=notes
        )
        return seg_group


    def reorder_segment_groups(self):
        """Move default segment groups to the end.

        This is required so that the segment groups included in the default
        groups are defined before they are used.

        :returns: None

        """
        seg_groups = self.morphology.segment_groups
        for group in ["soma_group", "axon_group", "dendrite_group", "all"]:
            try:
                sg = self.get_segment_group(group)
                seg_groups.append(seg_groups.pop(seg_groups.index(sg)))
            except ValueError:
                pass


    def optimise_segment_groups(self):
        """Optimise all segment groups in the cell.

        This will:

        - deduplicate members and includes in segment groups
        - remove members that have already been included using a segment group

        """
        for seg_group in self.morphology.segment_groups:
            self.optimise_segment_group(seg_group.id)

    def optimise_segment_group(self, seg_group_id):
        """Optimise segment group with id `seg_group_id`.

        :param seg_group_id: id of segment group to optimise
        :type seg_group_id: str

        """
        seg_group = self.get_segment_group(seg_group_id)
        # de-duplicate members and includes
        # cannot use list(set(list)) because the hash values for NeuroML
        # classes with identical values is also different

        members = seg_group.members
        new_members = []
        for i in members:
            if i not in new_members:
                new_members.append(i)
        members = new_members
        seg_group.members = list(members)

        includes = seg_group.includes
        new_includes = []
        for i in includes:
            if i not in new_includes:
                new_includes.append(i)
        includes = set(new_includes)
        # sorted
        seg_group.includes = natsort.natsorted(includes, key=lambda x:x.segment_groups)

        # remove members that are included by included segment groups
        if len(includes) > 0 and len(members) > 0:
            new_members = []
            for inc in includes:
                all_segment_ids_in_group = set(self.get_all_segments_in_group(inc.segment_groups))
                for i in members:
                    if i.segments not in all_segment_ids_in_group:
                        new_members.append(i)
            # sorted
            seg_group.members = natsort.natsorted(new_members, key=lambda x: x.segments)


    def set_spike_thresh(self, v, group_id="all"):
        """Set the spike threshold of the cell.

        :param v: value to set for spike threshold with units
        :type v: str
        :param group_id: id of segment group to modify
        :type group_id: str
        """
        self.add_membrane_property(
            "SpikeThresh", value=v, segment_groups=group_id
        )


    def set_init_memb_potential(self, v, group_id="all"):
        """Set the initial membrane potential of the cell.

        :param v: value to set for membrane potential with units
        :type v: str
        :param group_id: id of segment group to modify
        :type group_id: str
        """
        self.add_membrane_property(
            "InitMembPotential", value=v, segment_groups=group_id
        )


    def set_resistivity(self, resistivity, group_id="all") -> None:
        """Set the resistivity of the cell

        :type resistivity: str
        :param group_id: segment group to modify
        :type group_id: str
        """
        self.add_intracellular_property(
            "Resistivity", value=resistivity, segment_groups=group_id
        )


    def set_specific_capacitance(
        self, spec_cap, group_id="all"
    ):
        """Set the specific capacitance for the cell.

        :param spec_cap: value of specific capacitance with units
        :type spec_cap: str
        :param group_id: segment group to modify
        :type group_id: str
        """
        self.add_membrane_property(
            "SpecificCapacitance", value=spec_cap, segment_groups=group_id
        )


    def add_intracellular_property(self, property_name, **kwargs):
        """Generic function to add an intracellular property to the cell.

        For a full list of membrane properties, see:
        https://docs.neuroml.org/Userdocs/Schemas/Cells.html?#intracellularproperties

        :param property_name: name of intracellular property to add
        :type property_name: str
        :param kwargs: named arguments for intracellular property to be added
        :type kwargs: Any
        :returns: added property

        """
        self.setup_nml_cell(use_convention=False)
        prop = self.biophysical_properties.intracellular_properties.add(property_name, **kwargs)
        return prop


    def add_membrane_property(self, property_name, **kwargs):
        """Generic function to add a membrane property to the cell.

        For a full list of membrane properties, see:
        https://docs.neuroml.org/Userdocs/Schemas/Cells.html?#membraneproperties

        Please also see specific functions in this module, which are designed to be
        easier to use than this generic function.

        :param property_name: name or class of membrane property to add
        :type property_name: str or class
        :param kwargs: named arguments for membrane property to be added
        :type kwargs: Any
        :returns: added property

        """
        self.setup_nml_cell(use_convention=False)
        prop = self.biophysical_properties.membrane_properties.add(property_name, validate=False, **kwargs)
        return prop


    def add_channel_density_v(
        self,
        channel_density_type,
        nml_cell_doc,
        ion_chan_def_file="",
        **kwargs
    ):
        """Generic function to add channel density components to a Cell.

        :param channel_density_type: name or class of channel density type to add.
            See https://docs.neuroml.org/Userdocs/Schemas/Cells.html for the
            complete list.
        :type channel_density_type: str or class
        :param nml_cell_doc: cell NeuroML document to which channel density is to be added
        :type nml_cell_doc: NeuroMLDocument
        :param ion_chan_def_file: path to NeuroML2 file defining the ion channel, if empty, it assumes the channel is defined in the same file
        :type ion_chan_def_file: str
        :param kwargs: named arguments for required channel density type
        :type kwargs: Any
        :returns: added channel density
        """

        cd = self.add_membrane_property(channel_density_type, **kwargs)

        if len(ion_chan_def_file) > 0:
            if (
                self.component_factory("IncludeType", href=ion_chan_def_file)
                not in nml_cell_doc.includes
            ):
                nml_cell_doc.add("IncludeType", href=ion_chan_def_file)

        return cd


    def add_channel_density(
        self,
        nml_cell_doc,
        cd_id,
        ion_channel,
        cond_density,
        erev="0.0 mV",
        group_id="all",
        ion="non_specific",
        ion_chan_def_file="",
    ):
        """Add channel density.

        :param nml_cell_doc: cell NeuroML document to which channel density is to be added
        :type nml_cell_doc: NeuroMLDocument
        :param cd_id: id for channel density
        :type cd_id: str
        :param ion_channel: name of ion channel
        :type ion_channel: str
        :param cond_density: value of conductance density with units
        :type cond_density: str
        :param erev: value of reversal potential with units
        :type erev: str
        :param group_id: segment groups to add to
        :type group_id: str
        :param ion: name of ion
        :type ion: str
        :param ion_chan_def_file: path to NeuroML2 file defining the ion channel, if empty, it assumes the channel is defined in the same file
        :type ion_chan_def_file: str
        :returns: added channel density
        :rtype: ChannelDensity
        """
        cd = self.add_membrane_property(
            "ChannelDensity",
            id=cd_id,
            segment_groups=group_id,
            ion=ion,
            ion_channel=ion_channel,
            erev=erev,
            cond_density=cond_density,
        )

        if len(ion_chan_def_file) > 0:
            if (
                self.component_factory("IncludeType", href=ion_chan_def_file)
                not in nml_cell_doc.includes
            ):
                nml_cell_doc.add("IncludeType", href=ion_chan_def_file)

        return cd

    def setup_nml_cell(self, use_convention=True, overwrite=False, default_groups=["all", "soma_group"]):
        """Correctly initialise a NeuroML cell.

        To be called after a new component has been created to initialise the
        cell with these properties:

        - Morphology: id="morphology"
        - BiophysicalProperties: id="biophys":

          - MembraneProperties
          - IntracellularProperties

        If `use_convention` is True, it also creates the provided
        `default_groups` SegmentGroups for convenience. By default, it creates
        the "all", and "soma_group" groups since each cell must at least have a
        soma.

        When dendritic and axonal segments are added, the `add_segment`
        function will create `dendrite_group` and `axon_group` groups as
        required.

        Note that since this cell does not currently include a segment in its
        morphology, it is *not* a valid NeuroML construct. Use the `add_segment`
        and `add_unbranched_segments` functions to add segments and branches.
        They will also populate the default segment groups.

        :param id: id of the cell
        :type id: str
        :param use_convention: whether helper segment groups should be created using the default convention
        :type use_convention: bool
        :param overwrite: overwrite existing components
        :type overwrite: bool
        :param default_groups: list of default segment groups to create
        :type default_groups: list of strings
        :returns: None
        :rtype: None

        """
        # do not validate yet, because segments are required
        self.add("Morphology", id="morphology", validate=False, force=overwrite)

        # add does not overwrite existing values
        self.add("BiophysicalProperties", id="biophys", validate=False, force=overwrite)
        self.biophysical_properties.add("IntracellularProperties", validate=False, force=overwrite)
        self.biophysical_properties.add("MembraneProperties", validate=False, force=overwrite)

        self.setup_default_segment_groups(use_convention, default_groups)


    def setup_default_segment_groups(self, use_convention=True, default_groups=["all", "soma_group"]):
        """Create default segment groups for the cell.

        If `use_convention` is True, it also creates the provided
        `default_groups` SegmentGroups for convenience. By default, it creates
        the "all", and "soma_group" groups since each cell must at least have a
        soma. Allowed values are: "all", "soma_group", "axon_group", "dendrite_group".

        :param use_convention: whether helper segment groups should be created using the default convention
        :type use_convention: bool
        :param default_groups: list of default segment groups to create
        :type default_groups: list of strings
        :returns: list of created segment groups (or empty list if none created)
        :rtype: list
        """
        new_groups = []
        if use_convention:
            for grp in default_groups:
                neuro_lex_id = None
                notes = None

                if grp == "soma_group":
                    neuro_lex_id=neuroml.neuro_lex_ids.neuro_lex_ids["soma"]
                    notes="Default soma segment group for the cell"
                elif grp == "axon_group":
                    neuro_lex_id=neuroml.neuro_lex_ids.neuro_lex_ids["axon"]
                    notes="Default axon segment group for the cell"
                elif grp == "dendrite_group":
                    neuro_lex_id=neuroml.neuro_lex_ids.neuro_lex_ids["dend"]
                    notes="Default dendrite segment group for the cell"
                elif grp == "all":
                    neuro_lex_id=None
                    notes="Default segment group for all segments in the cell"
                else:
                    print(f"Error: only 'all', 'soma_group', 'dendrite_group', and 'axon_group' are supported. Received {grp}")
                    return []

                seg_group = self.add_segment_group(group_id=grp, neuro_lex_id=neuro_lex_id, notes=notes)
                new_groups.append(seg_group)

            self.reorder_segment_groups()

        return new_groups

    def add_unbranched_segments(
        self,
        points,
        parent=None,
        fraction_along=1.0,
        group_id=None,
        use_convention=True,
        seg_type=None,
        reorder_segment_groups=True,
        optimise_segment_groups=True
    ):
        """Add an unbranched list of segments to the cell.

        The list of points will include the first proximal point where this
        should be joined to the cell, followed by a list of distal points:

        ::

            |-----|-----|-----|------|.....---|
            p1    d1    d2    d3     d4       d N-1

        So, a list of N points will create a list of N-1 segments

        The list of points will be of the form::

            [[x1, y1, z1, d1], [x2, y2, z2, d2] ...]

        Please ensure that the first point, p1, is correctly set to ensure that
        this segment list is correctly connected to the rest of the cell.

        :param points: 3D points to create the segments
        :type points: list of [x, y, z, d] points
        :param parent: parent segment where first segment of list is to be attached
        :type parent: SegmentParent
        :param fraction_along: where the new segment list is connected to the parent (0: distal point, 1: proximal point)
            Note that the second and following segments will all be added at the
            distal point of the previous segment
        :type fraction_along: float
        :param group_id: segment group to add the segment to
            if a segment group does not already exist, it will be created
        :type group_id: SegmentGroup
        :param use_convention: whether helper segment groups should be created using the default convention
            See the documentation of the `add_segment` method for more information
            on the convention
        :type use_convention: bool
        :param seg_type: type of segments ("axon", "soma", "dendrite")
        :type seg_type: str
        :param reorder_segment_groups: whether the groups should be reordered
            to put the default segment groups last after the segment has been
            added.
            This is required for a valid NeuroML file because segment groups
            included in the default groups should be declared before they are
            used in the default groups. When adding lots of segments, one may
            want to only reorder at the end of the process instead of after
            each segment is added.

            This is only relevant if `use_convention=True`.
        :type reorder_segment_groups: bool
        :param optimise_segment_groups: toggle whether segment groups should be
            optimised after operation
        :type optimise_segment_groups: bool
        :returns: the segment group containing this new list of segments
        :rtype: SegmentGroup

        """
        prox = points[0]
        dist = points[1]

        seg_group = self.add_unbranched_segment_group(group_id=group_id)

        # first segment
        seg = self.add_segment(prox=prox, dist=dist, name=None, parent=parent,
                               fraction_along=fraction_along, group_id=group_id,
                               use_convention=use_convention,
                               seg_type=seg_type,
                               reorder_segment_groups=False)

        # rest of the segments
        prox = dist
        for pt in points[2:]:
            dist = pt
            seg = self.add_segment(prox=prox, dist=dist, name=None, parent=seg,
                                   fraction_along=1.0, group_id=group_id,
                                   use_convention=use_convention,
                                   seg_type=seg_type,
                                   reorder_segment_groups=False)
            prox = dist

        if reorder_segment_groups:
            self.reorder_segment_groups()

        if optimise_segment_groups:
            self.optimise_segment_groups()

        return self.get_segment_group(group_id)

    def create_unbranched_segment_group_branches(self, root_segment_id: int, use_convention: bool=True, reorder_segment_groups=True, optimise_segment_groups=True):
        """Organise the segments of the cell into new segment groups that each
        form a single contiguous unbranched cell branch.

        Note that the first segment (root segment) of a branch must have a proximal
        point that connects it to the rest of the neuronal morphology. If, when
        constructing these branches, a root segment is found that does not include
        a proximal point, one will be added using the `get_actual_proximal` method.

        No other changes will be made to any segments, or to any pre-existing
        segment groups.

        :param root_segment_id: id of segment considered the root of the tree,
            generally the first soma segment
        :type root_segment_id: int
        :param use_convention: toggle using NeuroML convention for segment groups
        :type use_convention: bool
        :param reorder_segment_groups: whether the groups should be reordered
            to put the default segment groups last after the segment has been
            added.
            This is required for a valid NeuroML file because segment groups
            included in the default groups should be declared before they are
            used in the default groups. When adding lots of segments, one may
            want to only reorder at the end of the process instead of after
            each segment is added.

            This is only relevant if `use_convention=True`.
        :type reorder_segment_groups: bool
        :param optimise_segment_groups: toggle whether segment groups should be
            optimised after operation
        :type optimise_segment_groups: bool
        :returns: modified cell with new section groups
        :rtype: neuroml.Cell

        """
        # don't recompute if already exists
        # get morphology tree
        morph_tree = getattr(self, "adjacency_list", None)
        if morph_tree is None:
            morph_tree = self.get_segment_adjacency_list()

        # initialise root segment and first segment group
        seg = self.get_segment(root_segment_id)
        group_name = f"seg_group_{len(self.morphology.segment_groups) - 1}_seg_{seg.id}"
        new_seg_group = self.add_unbranched_segment_group(group_name)

        # run recursive function
        self.__sectionise(root_segment_id, new_seg_group, morph_tree)

        if reorder_segment_groups:
            self.reorder_segment_groups()

        if optimise_segment_groups:
            self.optimise_segment_groups()



    def __sectionise(self, root_segment_id, seg_group, morph_tree):
        """Main recursive sectionising method.

        :param root_segment_id: id of root of branch
        :type root_segment_id: int
        :returns: TODO

        """
        # print(f"Processing element: {root_segment_id}")

        try:
            children = morph_tree[root_segment_id]
            # keep going while there's only one child
            # no need to use recursion here---hits Python's recursion limits in
            # long segment groups
            # - if there are no children, it'll go to the except block
            # - if there are more than one children, it'll go to the next
            # conditional
            while len(children) == 1:
                seg_group.add("Member", segments=root_segment_id)
                root_segment_id = children[0]
                children = morph_tree[root_segment_id]
            # if there are more than one children, we've reached the end of this
            # segment group but not of the branch. New segment groups need to start
            # from here.
            if len(children) > 1:
                # this becomes the last segment of the current segment group
                seg_group.add("Member", segments=root_segment_id)

                # each child will start a new segment group
                for child in children:
                    seg = self.get_segment(child)
                    # Ensure that a proximal point is set.
                    # This is required for the first segment of unbranched segment
                    # groups
                    seg.proximal = self.get_actual_proximal(seg.id)
                    group_name = f"seg_group_{len(self.morphology.segment_groups) - 1}_seg_{seg.id}"
                    new_seg_group = self.add_unbranched_segment_group(group_name)

                    self.__sectionise(child, new_seg_group, morph_tree)
        # if there are no children, it's a leaf node, so we just add to the current
        # seg_group and do nothing else
        except KeyError:
            seg_group.add("Member", segments=root_segment_id)


    def get_segment_adjacency_list(self):
        """Get the adjacency list of all segments in the cell morphology.
        Returns a dict where each key is a parent segment, and the value is the
        list of its children segments.

        Segment without children (leaf segments) are not included as parents in the
        adjacency list.

        This method also stores the computed adjacency list in
        `self.adjacency_list` for future use by other methods.

        `self.adjacency_list` is populated each time this method is run, to
        ensure that users can regenerate it after making modifications to the
        cell morphology. If the morphology has not changed, one only needs to
        populate it once and then re-use it as required.

        :returns: dict with parent segment ids as keys and ids of their children as values
        :rtype: dict[int, list[int]]

        """
        # create data structure holding list of children for each segment
        child_lists = {}
        for segment in self.morphology.segments:
            try:
                parent = segment.parent.segments
                if parent not in child_lists:
                    child_lists[parent] = []
                child_lists[parent].append(segment.id)
            except AttributeError:
                print(f"Warning: Segment: {segment} has no parent")

        self.adjacency_list = child_lists
        return child_lists

    def get_graph(self):
        """Get a networkx DiGraph of the morphology of the cell with distances
        between the proximal point of a parent and the point where a child
        connects to it as the weights of the edges of the graph.

        Please see https://networkx.org/documentation/stable/reference
        for information on networkx routines that can be used on this graph.

        This method also stores the graph in the `self.cell_graph` attribute
        for future use.

        :returns: networkx.Graph

        """
        cell_graph = nx.DiGraph()

        # don't recompute if already exists
        adlist = getattr(self, "adjacency_list", None)
        if adlist is None:
            adlist = self.get_segment_adjacency_list()

        for parid, childrenids in adlist.items():

            par_length = self.get_segment_length(parid)

            for cid in childrenids:
                child = self.get_segment(cid)

                fract = float(child.parent.fraction_along)
                len_to_proximal = par_length*fract

                cell_graph.add_edge(parid, cid, weight=len_to_proximal)

        self.cell_graph = cell_graph
        return cell_graph

    def get_distance(self, dest, source = 0):
        """Get path length between between two segments on a cell.

        Uses `networkx.dijkstra_path_length` to compute the shortest
        path between source and dest

        :param from: id of segment to get distance from
        :type from: int
        :param to: id of segment to get distance to
        :type to: int
        :returns: float
        """
        graph = getattr(self, "cell_graph", None)
        if graph is None:
            graph = self.get_graph()
        return nx.dijkstra_path_length(graph, source, dest)

    def get_all_distances_from_segment(self, seg_id = 0):
        """Get distances of all segments from the segment with id seg_id.

        Useful to get distances of segments from the soma.

        Uses networkx.single_source_dijkstra on the cell graph, without a
        target.

        :param seg_id: id of segment to get distances from
        :type seg_id: int
        :returns: pair of dictionaries for distance, path
            The return value is a tuple of two dictionaries keyed by target
            nodes. The first dictionary stores distance to each target node.
            The second stores the path to each target node.

        """
        graph = getattr(self, "cell_graph", None)
        if graph is None:
            graph = self.get_graph()
        return(nx.single_source_dijkstra(graph, source=seg_id))

    def get_segments_at_distance(self, distance, src_seg = 0):
        """Get all segments at distance from the provided `src_seg`.

        For each segment, it returns the fraction along the segment that the
        provided distance is at. For example, if segment N is 500 units long,
        and the `distance` cut-off is at 200, the fraction along is: 200/500.

        :param src_seg: id of segment to get distances from
        :type src_seg: int
        :param distance: distance to get segments at
        :type distance: float
        :returns: dict with segment ids as keys, and fraction along at which
            the cut off is as values

        """
        graph = getattr(self, "cell_graph", None)
        if graph is None:
            graph = self.get_graph()
        # returns all segments that are less than `distance` away.
        (target_dict, path_dict) = (nx.single_source_dijkstra(graph, source=src_seg, cutoff=distance))

        segs_frac_alongs = {}

        for tgt, dist in target_dict.items():
            try:
                frac_along = ((distance - dist) / self.get_segment_length(tgt))
            except ZeroDivisionError:
                # ignore zero length segments
                print(f"Warning: encountered zero length segment: {tgt}")
                continue

            if frac_along > 1.0:
                # not in this segment
                continue
            else:
                segs_frac_alongs[tgt] = frac_along

        return segs_frac_alongs


    def get_branching_points(self):
        """Get segments where the cell morphology branches.

        That is, the out-degree of the segment is > 1

        :returns: list of segment ids

        """
        graph = getattr(self, "cell_graph", None)
        if graph is None:
            graph = self.get_graph()

        segs = [n for (n, d) in graph.out_degree if d > 1]
        return segs


    def get_extremeties(self):
        """Get segments that are at the ends/tips of the neuronal morphology,
        with their distances from the soma.

        :returns: dict of segment ids and their distances from cell root as values

        """
        graph = getattr(self, "cell_graph", None)
        if graph is None:
            graph = self.get_graph()
        segs = [n for (n, d) in graph.out_degree if d == 0]

        res = {}
        for s in segs:
            res[s] = self.get_distance(s)
        return res


    def get_segment_location_info(self, seg_id):
        """Get location information about a particular segment.

        :param seg_id: id of segment to get information for
        :type seg_id: int
        :returns: a dictionary with various metrics about the segment

            - length of segment
            - distance from cell root
            - distance from nearest branching point
            - name of unbranched segment group segment belongs to (if any)
            - id of root segment of the unbranched segment group
            - distance from the segment group root segment

        """
        soma_id = self.get_morphology_root()
        distance_from_soma = self.get_distance(seg_id, source=soma_id)
        in_sg = None
        sg_segs = None
        sg_root = None
        distance_from_sg_root = None
        distance_from_bpt = None

        # get the unbranched segment group that this segment is in
        for sg in self.morphology.segment_groups:
            if sg.neuro_lex_id == neuroml.neuro_lex_ids.neuro_lex_ids["section"]:
                sg_segs = self.get_all_segments_in_group(sg)
                if seg_id in sg_segs:
                    in_sg = sg

                    # break out of loop
                    break

        graph = getattr(self, "cell_graph", None)
        if graph is None:
            graph = self.get_graph()

        # find first ancestral branching point
        # (a segment with more than one child)
        current = seg_id
        sg_root = current
        parent = list(graph.predecessors(current))[0]
        children = list(graph.successors(parent))

        while len(children) == 1:
            # the root of the segment group may not be at a
            # branching point: an unbranched cell branch can consist of
            # multiple unbranched segment groups
            if in_sg is not None:
                if current in sg_segs:
                    sg_root = current

            current = parent
            parent = list(graph.predecessors(current))[0]
            children = list(graph.successors(parent))

        distance_from_bpt = self.get_distance(seg_id, source=current)

        res = {}
        res['id'] = seg_id
        res['length'] = self.get_segment_length(seg_id)
        res['distance_from_cell_root'] = distance_from_soma
        res['distance_from_nearest_branching_point'] = distance_from_bpt

        # at unbranched segment root
        if in_sg is not None:
            res['in_unbranched_segment_group'] = in_sg.id
            res['unbranched_segment_group_root'] = sg_root
            distance_from_sg_root = self.get_distance(seg_id, source=sg_root)
            res['distance_from_segment_group_root'] = distance_from_sg_root

        return res


    def get_morphology_root(self):
        """Return the root of the complete cell morphology.

        This is usually the first segment of the soma, and there should only be
        one such segment.

        :returns: id of the root segment

        """
        # check if convention was followed and segment id 0 is root (has no
        # parents)
        try:
            root_seg = self.get_segment(0)
            if root_seg.parent is None:
                return 0
        except ValueError:
            pass

        graph = getattr(self, "cell_graph", None)
        if graph is None:
            graph = self.get_graph()
        segs = [n for (n, d) in graph.in_degree if d == 0]
        # there should only be one segment with 0 indegree
        assert len(segs) == 1
        return segs[0]

    ''',
    class_names=("Cell"),
)

METHOD_SPECS += (cell_methods,)


inserts = {}

inserts["Network"] = """


        netGroup = h5file.create_group(h5Group, 'network')
        netGroup._f_setattr("id", self.id)
        netGroup._f_setattr("notes", self.notes)
        if self.temperature:
            netGroup._f_setattr("temperature", self.temperature)


        for pop in self.populations:
            pop.exportHdf5(h5file, netGroup)

        if len(self.synaptic_connections) > 0:
            raise Exception("<synapticConnection> not yet supported in HDF5 export")
        if len(self.explicit_inputs) > 0:
            raise Exception("<explicitInput> not yet supported in HDF5 export")

        for proj in self.projections:
            proj.exportHdf5(h5file, netGroup)

        for eproj in self.electrical_projections:
            eproj.exportHdf5(h5file, netGroup)

        for cproj in self.continuous_projections:
            cproj.exportHdf5(h5file, netGroup)

        for il in self.input_lists:
            il.exportHdf5(h5file, netGroup)

"""

inserts["Population"] = """

        popGroup = h5file.create_group(h5Group, 'population_'+self.id)
        popGroup._f_setattr("id", self.id)
        popGroup._f_setattr("component", self.component)
        for p in self.properties:
            popGroup._f_setattr("property:"+p.tag, p.value)


        if len(self.instances)>0:

            colCount = 3
            a = numpy.zeros([len(self.instances), colCount], numpy.float32)

            count=0
            for instance in self.instances:
              a[count,0] = instance.location.x
              a[count,1] = instance.location.y
              a[count,2] = instance.location.z

              count=count+1

            popGroup._f_setattr("size", count)
            popGroup._f_setattr("type", "populationList")

            array = h5file.create_carray(popGroup, self.id, obj=a, title="Locations of cells in "+ self.id)
            array._f_setattr("column_0", "x")
            array._f_setattr("column_1", "y")
            array._f_setattr("column_2", "z")

        else:
            popGroup._f_setattr("size", self.size)

    def get_size(self):
        return len(self.instances) if len(self.instances)>0 else (self.size if self.size else 0)

    def __str__(self):

        return "Population: "+str(self.id)+" with "+str( self.get_size() )+" components of type "+(self.component if self.component else "???")

"""

inserts["Projection"] = """

        projGroup = h5file.create_group(h5Group, 'projection_'+self.id)
        projGroup._f_setattr("id", self.id)
        projGroup._f_setattr("type", "projection")
        projGroup._f_setattr("presynapticPopulation", self.presynaptic_population)
        projGroup._f_setattr("postsynapticPopulation", self.postsynaptic_population)
        projGroup._f_setattr("synapse", self.synapse)

        #print("Exporting "+str(len(self.connections))+" connections, "+str(len(self.connection_wds))+" connections with weight")

        connection_wds = len(self.connection_wds) > 0

        cols = 2

        extra_cols = {}

        include_segment_fraction = neuroml.utils.has_segment_fraction_info(self.connections) or neuroml.utils.has_segment_fraction_info(self.connection_wds)

        if include_segment_fraction:
            extra_cols["column_"+str(cols)] = "pre_segment_id"
            extra_cols["column_"+str(cols+1)] = "post_segment_id"
            extra_cols["column_"+str(cols+2)] = "pre_fraction_along"
            extra_cols["column_"+str(cols+3)] = "post_fraction_along"
            cols +=4


        if connection_wds:
            extra_cols["column_"+str(cols)] = "weight"
            extra_cols["column_"+str(cols+1)] = "delay"
            cols+=2

        a = numpy.zeros([len(self.connections)+len(self.connection_wds), cols], numpy.float32)

        count=0

        for connection in self.connections:
          ####a[count,0] = connection.id
          a[count,0] = connection.get_pre_cell_id()
          a[count,1] = connection.get_post_cell_id()
          if include_segment_fraction:
            a[count,2] = connection.pre_segment_id
            a[count,3] = connection.post_segment_id
            a[count,4] = connection.pre_fraction_along
            a[count,5] = connection.post_fraction_along
          count=count+1

        for connection in self.connection_wds:
          ###a[count,0] = connection.id
          a[count,0] = connection.get_pre_cell_id()
          a[count,1] = connection.get_post_cell_id()

          if include_segment_fraction:
            a[count,2] = connection.pre_segment_id
            a[count,3] = connection.post_segment_id
            a[count,4] = connection.pre_fraction_along
            a[count,5] = connection.post_fraction_along

          a[count,cols-2] = connection.weight
          if 'ms' in connection.delay:
            delay = float(connection.delay[:-2].strip())
          elif 's' in connection.delay:
            delay = float(connection.delay[:-1].strip())*1000.
          elif 'us' in connection.delay:
            delay = float(connection.delay[:-2].strip())/1e3

          a[count,cols-1] = delay
          count=count+1

        if len(a)>0:
            array = h5file.create_carray(projGroup, self.id, obj=a, title="Connections of cells in "+ self.id)

            ###array._f_setattr("column_0", "id")
            array._f_setattr("column_0", "pre_cell_id")
            array._f_setattr("column_1", "post_cell_id")

            for col in extra_cols.keys():
                array._f_setattr(col,extra_cols[col])


    def __str__(self):
        return "Projection: "+self.id+" from "+self.presynaptic_population+" to "+self.postsynaptic_population+", synapse: "+self.synapse



"""

inserts["ElectricalProjection"] = """

        projGroup = h5file.create_group(h5Group, 'projection_'+self.id)
        projGroup._f_setattr("id", self.id)
        projGroup._f_setattr("type", "electricalProjection")
        projGroup._f_setattr("presynapticPopulation", self.presynaptic_population)
        projGroup._f_setattr("postsynapticPopulation", self.postsynaptic_population)

        syn = self.electrical_connections[0].synapse if len(self.electrical_connections)>0 else \
                    self.electrical_connection_instances[0].synapse if len(self.electrical_connection_instances)>0 else self.electrical_connection_instance_ws[0].synapse
        projGroup._f_setattr("synapse", syn )

        cols = 7
        extra_cols = {}

        num_tot = len(self.electrical_connections)+len(self.electrical_connection_instances)+len(self.electrical_connection_instance_ws)
        if len(self.electrical_connection_instance_ws)>0:
            extra_cols["column_"+str(cols)] = "weight"
            cols+=1

        #print("Exporting "+str(num_tot)+" electrical connections")
        a = numpy.zeros([num_tot, cols], numpy.float32)

        count=0

        # TODO: optimise for single compartment cells, i.e. where no pre_segment/post_fraction_along etc.
        for connection in self.electrical_connections:
          a[count,0] = connection.id
          a[count,1] = connection.get_pre_cell_id()
          a[count,2] = connection.get_post_cell_id()
          a[count,3] = connection.pre_segment
          a[count,4] = connection.post_segment
          a[count,5] = connection.pre_fraction_along
          a[count,6] = connection.post_fraction_along
          count=count+1

        for connection in self.electrical_connection_instances:
          a[count,0] = connection.id
          a[count,1] = connection.get_pre_cell_id()
          a[count,2] = connection.get_post_cell_id()
          a[count,3] = connection.pre_segment
          a[count,4] = connection.post_segment
          a[count,5] = connection.pre_fraction_along
          a[count,6] = connection.post_fraction_along
          count=count+1

        for connection in self.electrical_connection_instance_ws:
          a[count,0] = connection.id
          a[count,1] = connection.get_pre_cell_id()
          a[count,2] = connection.get_post_cell_id()
          a[count,3] = connection.pre_segment
          a[count,4] = connection.post_segment
          a[count,5] = connection.pre_fraction_along
          a[count,6] = connection.post_fraction_along
          a[count,7] = connection.get_weight()
          count=count+1

        array = h5file.create_carray(projGroup, self.id, obj=a, title="Connections of cells in "+ self.id)

        array._f_setattr("column_0", "id")
        array._f_setattr("column_1", "pre_cell_id")
        array._f_setattr("column_2", "post_cell_id")
        array._f_setattr("column_3", "pre_segment_id")
        array._f_setattr("column_4", "post_segment_id")
        array._f_setattr("column_5", "pre_fraction_along")
        array._f_setattr("column_6", "post_fraction_along")

        for col in extra_cols.keys():
            array._f_setattr(col,extra_cols[col])

"""


inserts["ContinuousProjection"] = """

        projGroup = h5file.create_group(h5Group, 'projection_'+self.id)
        projGroup._f_setattr("id", self.id)
        projGroup._f_setattr("type", "continuousProjection")
        projGroup._f_setattr("presynapticPopulation", self.presynaptic_population)
        projGroup._f_setattr("postsynapticPopulation", self.postsynaptic_population)

        pre_comp = self.continuous_connections[0].pre_component if len(self.continuous_connections)>0 else \
                            self.continuous_connection_instances[0].pre_component if len(self.continuous_connection_instances)>0 else self.continuous_connection_instance_ws[0].pre_component
        projGroup._f_setattr("preComponent", pre_comp )
        post_comp = self.continuous_connections[0].post_component if len(self.continuous_connections)>0 else \
                            self.continuous_connection_instances[0].post_component if len(self.continuous_connection_instances)>0 else self.continuous_connection_instance_ws[0].post_component
        projGroup._f_setattr("postComponent", post_comp )

        cols = 7
        extra_cols = {}

        num_tot = len(self.continuous_connections)+len(self.continuous_connection_instances)+len(self.continuous_connection_instance_ws)

        if len(self.continuous_connection_instance_ws)>0:
            extra_cols["column_"+str(cols)] = 'weight'
            cols+=1

        #print("Exporting "+str(num_tot)+" continuous connections")
        a = numpy.zeros([num_tot, cols], numpy.float32)

        count=0

        # TODO: optimise for single compartment cells, i.e. where no pre_segment/post_fraction_along etc.
        for connection in self.continuous_connections:
          a[count,0] = connection.id
          a[count,1] = connection.get_pre_cell_id()
          a[count,2] = connection.get_post_cell_id()
          a[count,3] = connection.pre_segment
          a[count,4] = connection.post_segment
          a[count,5] = connection.pre_fraction_along
          a[count,6] = connection.post_fraction_along
          count=count+1

        for connection in self.continuous_connection_instances:
          a[count,0] = connection.id
          a[count,1] = connection.get_pre_cell_id()
          a[count,2] = connection.get_post_cell_id()
          a[count,3] = connection.pre_segment
          a[count,4] = connection.post_segment
          a[count,5] = connection.pre_fraction_along
          a[count,6] = connection.post_fraction_along
          count=count+1


        for connection in self.continuous_connection_instance_ws:
          a[count,0] = connection.id
          a[count,1] = connection.get_pre_cell_id()
          a[count,2] = connection.get_post_cell_id()
          a[count,3] = connection.pre_segment
          a[count,4] = connection.post_segment
          a[count,5] = connection.pre_fraction_along
          a[count,6] = connection.post_fraction_along
          a[count,7] = connection.weight
          count=count+1


        array = h5file.create_carray(projGroup, self.id, obj=a, title="Connections of cells in "+ self.id)

        array._f_setattr("column_0", "id")
        array._f_setattr("column_1", "pre_cell_id")
        array._f_setattr("column_2", "post_cell_id")
        array._f_setattr("column_3", "pre_segment_id")
        array._f_setattr("column_4", "post_segment_id")
        array._f_setattr("column_5", "pre_fraction_along")
        array._f_setattr("column_6", "post_fraction_along")
        for k in extra_cols:
            array._f_setattr(k, extra_cols[k])


"""


inserts["InputList"] = """

        ilGroup = h5file.create_group(h5Group, 'inputList_'+self.id)
        ilGroup._f_setattr("id", self.id)
        ilGroup._f_setattr("component", self.component)
        ilGroup._f_setattr("population", self.populations)

        cols = 4

        extra_cols = {}

        num_tot = len(self.input)+len(self.input_ws)

        if len(self.input_ws)>0:
            extra_cols["column_"+str(cols)] = 'weight'
            cols+=1

        #print("Exporting "+str(num_tot)+" inputs")
        a = numpy.zeros([num_tot, cols], numpy.float32)

        count=0

        for input in self.input:
            a[count,0] = input.id
            a[count,1] = input.get_target_cell_id()
            a[count,2] = input.get_segment_id()
            a[count,3] = input.get_fraction_along()
            count+=1

        for input in self.input_ws:
            a[count,0] = input.id
            a[count,1] = input.get_target_cell_id()
            a[count,2] = input.get_segment_id()
            a[count,3] = input.get_fraction_along()
            a[count,4] = input.get_weight()
            count+=1

        array = h5file.create_carray(ilGroup, self.id, obj=a, title="Locations of inputs in "+ self.id)

        array._f_setattr("column_0", "id")
        array._f_setattr("column_1", "target_cell_id")
        array._f_setattr("column_2", "segment_id")
        array._f_setattr("column_3", "fraction_along")
        for k in extra_cols:
            array._f_setattr(k, extra_cols[k])

    def __str__(self):

        return "Input list: "+self.id+" to "+self.populations+", component "+self.component

"""


for insert in inserts.keys():
    ms = MethodSpec(
        name="exportHdf5",
        source='''\

    def exportHdf5(self, h5file, h5Group):
        """Export to HDF5 file.

        :param h5file: HDF5 file handler
        :type h5file: file object
        :param h5Group: the tables Group object to write
        :type h5Group: tables.Group

        """
        #print("Exporting %s: "+str(self.id)+" as HDF5")
        %s
    '''
        % (insert, inserts[insert]),
        class_names=(insert),
    )
    METHOD_SPECS += (ms,)


synaptic_connections = MethodSpec(
    name="synaptic_connections",
    source='''\

    def _get_cell_id(self,ref):
        """Get cell ID"""
        if '[' in ref:
            return int(ref.split('[')[1].split(']')[0])
        else:
            return int(ref.split('/')[2])

    def _get_population(self,ref):
        """Get population"""
        if '[' in ref:
            return ref.split('[')[0]
        else:
            return ref.split('/')[0]

    def __str__(self):

        dest = self.destination if self.destination else 'unspecified'
        return "Synaptic connection from "+str(self._get_population(self.from_))+"(cell "+str(self._get_cell_id(self.from_))+ \
            ") -> "+str(self._get_population(self.to))+"(cell "+str(self._get_cell_id(self.to))+"), syn: "+self.synapse+", destination: "+dest


    ''',
    class_names=("SynapticConnection"),
)

METHOD_SPECS += (synaptic_connections,)

explicit_inputs = MethodSpec(
    name="explicit_inputs",
    source='''\

    def get_target_cell_id(self,):
        """Get target cell ID"""
        if '[' in self.target:
            return int(self.target.split('[')[1].split(']')[0])
        else:
            return int(self.target.split('/')[2])

    def get_target_population(self,):
        """Get target population."""
        if '[' in self.target:
            return self.target.split('[')[0]
        else:
            return self.target.split('/')[0]

    def __str__(self):

        dest = self.destination if self.destination else 'unspecified'
        return "Explicit Input of type "+str(self.input)+" to "+self.get_target_population()+"(cell "+str(self.get_target_cell_id())+ \
            "), destination: "+dest


    ''',
    class_names=("ExplicitInput"),
)

METHOD_SPECS += (explicit_inputs,)


def test():
    for spec in METHOD_SPECS:
        spec.show()


def main():
    test()


if __name__ == "__main__":
    main()
