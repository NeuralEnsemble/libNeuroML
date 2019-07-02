import sys
import re

#
# You must include the following class definition at the top of
#   your method specification file.
#
class MethodSpec(object):
    def __init__(self, name='', source='', class_names='',
            class_names_compiled=None):
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
        '''
        if class_names is None:
            self.class_names = ('.*', )
        else:
        if class_names_compiled is None:
            self.class_names_compiled = re.compile(self.class_names)
        else:
            self.class_names_compiled = class_names_compiled'''
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
        
        if self.class_names == class_name or (isinstance(self.class_names,list) and class_name in self.class_names):
            return True
        else:
            return False
    def get_interpolated_source(self, values_dict):
        """Get the method source code, interpolating values from values_dict
        into it.  The source returned by this method is inserted into
        the generated class.
        """
        source = self.source % values_dict
        source = source.replace('PERCENTAGE','%')
        return source
    def show(self):
        print('specification:')
        print('    name: %s' % (self.name, ))
        print(self.source)
        print('    class_names: %s' % (self.class_names, ))
        print('    names pat  : %s' % (self.class_names_compiled.pattern, ))


#
# Provide one or more method specification such as the following.
# Notes:
# - Each generated class contains a class variable _member_data_items.
#   This variable contains a list of instances of class _MemberSpec.
#   See the definition of class _MemberSpec near the top of the
#   generated superclass file and also section "User Methods" in
#   the documentation, as well as the examples below.

num_segments = MethodSpec(name='num_segments',
    source='''\
    @property
    def num_segments(self):
        return len(self.segments)
''',
    class_names=("Morphology")
    )


length = MethodSpec(name='length',
    source='''\
    @property
    def length(self):
        prox_x = self.proximal.x
        prox_y = self.proximal.y
        prox_z = self.proximal.z

        dist_x = self.distal.x
        dist_y = self.distal.y
        dist_z = self.distal.z

        length = ((prox_x-dist_x)**2 + (prox_y-dist_y)**2 + (prox_z-dist_z)**2)**(0.5)

        return length
        
    def __str__(self):
        
        return "<Segment|"+str(self.id)+"|"+self.name+">"
        
    def __repr__(self):
    
        return str(self)
    
''',
    class_names=("Segment")
    )
    
volume = MethodSpec(name='volume',
    source='''\
    @property
    def volume(self):
        from math import pi

        prox_rad = self.proximal.diameter/2.0
        dist_rad = self.distal.diameter/2.0
        length = self.length

        volume = (pi/3)*length*(prox_rad**2+dist_rad**2+prox_rad*dist_rad)

        return volume
    ''',
    class_names=("Segment")
    )


surface_area = MethodSpec(name='surface_area',
    source='''\

    @property
    def surface_area(self):
        from math import pi
        from math import sqrt

        prox_rad = self.proximal.diameter/2.0
        dist_rad = self.distal.diameter/2.0
        length = self.length

        surface_area = pi*(prox_rad+dist_rad)*sqrt((prox_rad-dist_rad)**2+length**2)
        
        return surface_area
    ''',
    class_names=("Segment")
    )

#
# Provide a list of your method specifications.
#   This list of specifications must be named METHOD_SPECS.
#
METHOD_SPECS=(length,
              volume,
              surface_area,
              num_segments,
             )
             
             
    
seg_grp = MethodSpec(name='SegmentGroup',
    source='''\

        
    def __str__(self):
        
        return "SegmentGroup: "+str(self.id)+", "+str(len(self.members))+" member(s), "+str(len(self.includes))+" included group(s)"
        
    def __repr__(self):
    
        return str(self)
    
''',
    class_names=("SegmentGroup")
    )

METHOD_SPECS+=(seg_grp,)

connection_cell_ids = MethodSpec(name='connection_cell_ids',
    source='''\

    def _get_cell_id(self, id_string):
        if '[' in id_string:
            return int(id_string.split('[')[1].split(']')[0])
        else:
            return int(id_string.split('/')[2])

    def get_pre_cell_id(self):
        
        return self._get_cell_id(self.pre_cell_id)
        
    def get_post_cell_id(self):
        
        return self._get_cell_id(self.post_cell_id)

    def get_pre_segment_id(self):
        
        return int(self.pre_segment_id)
        
    def get_post_segment_id(self):
        
        return int(self.post_segment_id)

    def get_pre_fraction_along(self):
        
        return float(self.pre_fraction_along)
        
    def get_post_fraction_along(self):
        
        return float(self.post_fraction_along)
        
        
    def get_pre_info(self):
        
        return str(self.get_pre_cell_id())+(':'+str(self.get_pre_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_pre_fraction_along()+')' if self.get_pre_segment_id()!=0 or self.get_pre_fraction_along()!=0.5 else '')
        
    def get_post_info(self):
        
        return str(self.get_post_cell_id())+(':'+str(self.get_post_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_post_fraction_along()+')' if self.get_post_segment_id()!=0 or self.get_post_fraction_along()!=0.5 else '')
        
    def __str__(self):
        
        return "Connection "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())
        
    ''',
    class_names=(["Connection","ConnectionWD"])
    )
  
METHOD_SPECS+=(connection_cell_ids,)
    
connection_wd_cell_ids = MethodSpec(name='connection_wd_cell_ids',
    source='''\
        
    def __str__(self):
        
        return "Connection "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", weight: "+'PERCENTAGEf' PERCENTAGE (float(self.weight))+", delay: "+'PERCENTAGE.5f' PERCENTAGE (self.get_delay_in_ms())+" ms"
            
    def get_delay_in_ms(self):
        if 'ms' in self.delay:
            return float(self.delay[:-2].strip())
        elif 's' in self.delay:
            return float(self.delay[:-1].strip())*1000.0
        
    ''',
    class_names=("ConnectionWD")
    )
  
METHOD_SPECS+=(connection_wd_cell_ids,)

elec_connection_instance_cell_ids = MethodSpec(name='elec_connection_instance_cell_ids',
    source='''\
        
    def _get_cell_id(self, id_string):
        if '[' in id_string:
            return int(id_string.split('[')[1].split(']')[0])
        else:
            return int(id_string.split('/')[2])
        
    def __str__(self):
        
        return "Electrical Connection (Instance based) "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", synapse: "+str(self.synapse)
            
        
    ''',
    class_names=("ElectricalConnectionInstance")
    )
  
METHOD_SPECS+=(elec_connection_instance_cell_ids,)

elec_connection_instance_w = MethodSpec(name='elec_connection_instance_w',
    source='''\
        
    def get_weight(self):
        
        return float(self.weight) if self.weight!=None else 1.0
        
    def __str__(self):
        
        return "Electrical Connection (Instance based & weight) "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", synapse: "+str(self.synapse) + ", weight: "+'PERCENTAGE.6f'PERCENTAGEself.get_weight()
            
    ''',
    class_names=("ElectricalConnectionInstanceW")
    )
  
METHOD_SPECS+=(elec_connection_instance_w,)

elec_connection_cell_ids = MethodSpec(name='elec_connection_cell_ids',
    source='''\
        
    def _get_cell_id(self, id_string):
            return int(float(id_string))
            
    def get_pre_cell_id(self):
        
        return self._get_cell_id(self.pre_cell)
        
    def get_post_cell_id(self):
        
        return self._get_cell_id(self.post_cell)
        
    def get_pre_segment_id(self):
        
        return int(self.pre_segment)
        
    def get_post_segment_id(self):
        
        return int(self.post_segment)

    def get_pre_fraction_along(self):
        
        return float(self.pre_fraction_along)
        
    def get_post_fraction_along(self):
        
        return float(self.post_fraction_along)
        
        
    def get_pre_info(self):
        
        return str(self.get_pre_cell_id())+(':'+str(self.get_pre_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_pre_fraction_along()+')' if self.get_pre_segment_id()!=0 or self.get_pre_fraction_along()!=0.5 else '')
        
    def get_post_info(self):
        
        return str(self.get_post_cell_id())+(':'+str(self.get_post_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_post_fraction_along()+')' if self.get_post_segment_id()!=0 or self.get_post_fraction_along()!=0.5 else '')
        
        
    def __str__(self):
        
        return "Electrical Connection "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", synapse: "+str(self.synapse)
            
        
    ''',
    class_names=("ElectricalConnection")
    )
  
METHOD_SPECS+=(elec_connection_cell_ids,)

cont_connection_instance_cell_ids = MethodSpec(name='cont_connection_instance_cell_ids',
    source='''\
        
    def _get_cell_id(self, id_string):
        if '[' in id_string:
            return int(id_string.split('[')[1].split(']')[0])
        else:
            return int(id_string.split('/')[2])
           
        
    def __str__(self):
        
        return "Continuous Connection (Instance based) "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", pre comp: "+str(self.pre_component)+", post comp: "+str(self.post_component)
            
        
    ''',
    class_names=("ContinuousConnectionInstance")
    )
  
METHOD_SPECS+=(cont_connection_instance_cell_ids,)

cont_connection_instance_w = MethodSpec(name='cont_connection_instance_w',
    source='''\
        
    def get_weight(self):
        
        return float(self.weight) if self.weight!=None else 1.0
        
    def __str__(self):
        
        return "Continuous Connection (Instance based & weight) "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", pre comp: "+str(self.pre_component)+", post comp: "+str(self.post_component)+", weight: "+'PERCENTAGE.6f'PERCENTAGEself.get_weight()
            
        
    ''',
    class_names=("ContinuousConnectionInstanceW")
    )
  
METHOD_SPECS+=(cont_connection_instance_w,)

cont_connection_cell_ids = MethodSpec(name='cont_connection_cell_ids',
    source='''\
        
    def _get_cell_id(self, id_string):
            return int(float(id_string))
            
 
    def get_pre_cell_id(self):
        
        return self._get_cell_id(self.pre_cell)
        
    def get_post_cell_id(self):
        
        return self._get_cell_id(self.post_cell)
        
    def get_pre_segment_id(self):
        
        return int(self.pre_segment)
        
    def get_post_segment_id(self):
        
        return int(self.post_segment)

    def get_pre_fraction_along(self):
        
        return float(self.pre_fraction_along)
        
    def get_post_fraction_along(self):
        
        return float(self.post_fraction_along)
        
        
    def get_pre_info(self):
        
        return str(self.get_pre_cell_id())+(':'+str(self.get_pre_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_pre_fraction_along()+')' if self.get_pre_segment_id()!=0 or self.get_pre_fraction_along()!=0.5 else '')
        
    def get_post_info(self):
        
        return str(self.get_post_cell_id())+(':'+str(self.get_post_segment_id())+'('+ 'PERCENTAGE.5f'PERCENTAGEself.get_post_fraction_along()+')' if self.get_post_segment_id()!=0 or self.get_post_fraction_along()!=0.5 else '')
        
        
    def __str__(self):
        
        return "Continuous Connection "+str(self.id)+": "+str(self.get_pre_info())+" -> "+str(self.get_post_info())+ \
            ", pre comp: "+str(self.pre_component)+", post comp: "+str(self.post_component)
            
        
    ''',
    class_names=("ContinuousConnection")
    )
  
METHOD_SPECS+=(cont_connection_cell_ids,)


instance = MethodSpec(name='instance',
    source='''\

        
    def __str__(self):
        
        return "Instance "+str(self.id)+ (" at location: "+str(self.location) if self.location else "")
        
    def __repr__(self):
    
        return str(self)
    
''',
    class_names=("Instance")
    )
METHOD_SPECS+=(instance,)


location = MethodSpec(name='location',
    source='''\

    def _format(self,value):
    
        if int(value)==value:
            return str(int(value))
        else:
            return 'PERCENTAGE.4f' PERCENTAGE value
        
    def __str__(self):
        
        return "("+ self._format(self.x) +", "+ self._format(self.y) +", "+ self._format(self.z) +")"
        
    def __repr__(self):
    
        return str(self)
    
''',
    class_names=("Location")
    )
METHOD_SPECS+=(location,)




input_cell_ids = MethodSpec(name='input_cell_ids',
    source='''\

    def _get_cell_id(self, id_string):
        if '[' in id_string:
            return int(id_string.split('[')[1].split(']')[0])
        else:
            return int(id_string.split('/')[2])

    def get_target_cell_id(self):
        
        return self._get_cell_id(self.target)

    def get_segment_id(self):
        
        return int(self.segment_id) if self.segment_id else 0

    def get_fraction_along(self):
        
        return float(self.fraction_along) if self.fraction_along else 0.5
        
    def __str__(self):
        
        return "Input "+str(self.id)+": "+str(self.get_target_cell_id())+":"+str(self.get_segment_id())+"("+'PERCENTAGE.6f'PERCENTAGEself.get_fraction_along()+")"
        
    ''',
    class_names=(["Input","ExplicitInput"])
    )
  
METHOD_SPECS+=(input_cell_ids,)


input_w = MethodSpec(name='input_w',
    source='''\
    
    def get_weight(self):
        
        return float(self.weight) if self.weight!=None else 1.0

    def __str__(self):
        
        return "Input (weight) "+str(self.id)+": "+str(self.get_target_cell_id())+":"+str(self.get_segment_id())+"("+'PERCENTAGE.6f'PERCENTAGEself.get_fraction_along()+"), weight: "+'PERCENTAGE.6f'PERCENTAGEself.get_weight()
        
    ''',
    class_names=(["InputW"])
    )
  
METHOD_SPECS+=(input_w,)


nml_doc_summary = MethodSpec(name='summary',
    source='''\

    
    def summary(self, show_includes=True, show_non_network=True):
    
        import inspect
        
        info = "*******************************************************\\n"
        info+="* NeuroMLDocument: "+self.id+"\\n*\\n"
        post = ""
        membs = inspect.getmembers(self)
        for memb in membs:
            if isinstance(memb[1], list) and len(memb[1])>0 and not memb[0].endswith('_') and not memb[0] == 'networks':
                if (memb[0] == 'includes' and show_includes) or (not memb[0] == 'includes' and show_non_network):
                    post = "*\\n"
                    info+="*   "+str(memb[1][0].__class__.__name__)+": "
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
                    
        
        info+="*******************************************************"
        
        return info
        
    warn_count = 0
        
    def get_by_id(self,id):
        if len(id)==0:
            import inspect
            callframe = inspect.getouterframes(inspect.currentframe(), 2)
            print('Method: '+ callframe[1][3] + ' is asking for an element with no id...')
            
            return None
        all_ids = []
        for ms in self.member_data_items_:
            mlist = self.__getattribute__(ms.name)
            for m in mlist:
                if hasattr(m,"id"):
                    if m.id == id:
                        return m
                    else:
                        all_ids.append(m.id)
        from neuroml.loaders import print_
        if self.warn_count<10:
            print_("Id "+id+" not found in <neuroml> element. All ids: "+str(sorted(all_ids)))
            self.warn_count+=1
        elif self.warn_count==10:
            print_(" - Suppressing further warnings about id not found...")
        return None
        
    def append(self,element):
        from neuroml.utils import append_to_element
        append_to_element(self,element)
        
    ''',
    class_names=("NeuroMLDocument")
    )
  
METHOD_SPECS+=(nml_doc_summary,)

network_get_by_id = MethodSpec(name='get_by_id',
    source='''\

    warn_count = 0
    def get_by_id(self,id):
        all_ids = []
        for ms in self.member_data_items_:
            mlist = self.__getattribute__(ms.name)
            for m in mlist:
                if hasattr(m,"id"):
                    if m.id == id:
                        return m
                    else:
                        all_ids.append(m.id)
        from neuroml.loaders import print_
        if self.warn_count<10:
            print_("Id "+id+" not found in <network> element. All ids: "+str(sorted(all_ids)))
            self.warn_count+=1
        elif self.warn_count==10:
            print_(" - Suppressing further warnings about id not found...")
        return None
        
        
    def __str__(self):
        
        return "Network "+str(self.id)+" with "+str(len(self.populations))+" population(s)"
        
    ''',
    class_names=("Network")
    )
  
METHOD_SPECS+=(network_get_by_id,)


cell_methods = MethodSpec(name='cell_methods',
    source='''\



    def get_segment_ids_vs_segments(self):

        segments = {}
        for segment in self.morphology.segments:
            segments[segment.id] = segment

        return segments
        
    def get_all_segments_in_group(self,
                                  segment_group):
                                  
        if isinstance(segment_group, str):
            for sg in self.morphology.segment_groups:
                if sg.id == segment_group:
                    segment_group = sg
                
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
                                       group_list, 
                                       check_parentage=False, 
                                       include_cumulative_lengths=False, 
                                       include_path_lengths=False, 
                                       path_length_metric="Path Length from root"): # Only option supported

        unord_segs = {}
        other_segs = {}
        
        if isinstance(group_list, str):
            group_list = [group_list]

        segments = self.get_segment_ids_vs_segments()

        for sg in self.morphology.segment_groups:
            all_segs_here = self.get_all_segments_in_group(sg)
            
            if sg.id in group_list:
                unord_segs[sg.id] = [segments[s] for s in all_segs_here]
            else:
                other_segs[sg.id] = [segments[s] for s in all_segs_here]

        ord_segs = {}     

        from operator import attrgetter
        for key in unord_segs.keys():          
            segs = unord_segs[key]
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
            import math
            
            cumulative_lengths = {}
            path_lengths_to_proximal = {}
            path_lengths_to_distal = {}
            
            for key in ord_segs.keys():   
                cumulative_lengths[key] = []
                path_lengths_to_proximal[key] = {}
                path_lengths_to_distal[key] = {}
                
                tot_len = 0
                for seg in ord_segs[key]:     
                    d = seg.distal
                    p = seg.proximal
                    if not p:
                        parent_seg = segments[seg.parent.segments]
                        p = parent_seg.distal
                    length = math.sqrt( (d.x-p.x)**2 + (d.y-p.y)**2 + (d.z-p.z)**2 )
                    
                    if not seg.parent or not seg.parent.segments in path_lengths_to_distal[key]:
                    
                        path_lengths_to_proximal[key][seg.id] = 0
                        last_seg = seg
                        par_seg_element = seg.parent
                        while par_seg_element!=None:
                        
                            par_seg = segments[par_seg_element.segments]
                            d = par_seg.distal
                            p = par_seg.proximal
                            
                            if not p:
                                par_seg_parent_seg = segments[par_seg.parent.segments]
                                p = par_seg_parent_seg.distal
                                
                            par_length = math.sqrt( (d.x-p.x)**2 + (d.y-p.y)**2 + (d.z-p.z)**2 )
                            
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
        
        
                
    def summary(self):
        print("*******************************************************")
        print("* Cell: "+str(self.id))
        print("* Notes: "+str(self.notes))
        print("* Segments: "+str(len(self.morphology.segments)))
        print("* SegmentGroups: "+str(len(self.morphology.segment_groups)))
        
        
        print("*******************************************************")
        
    ''',
    class_names=("Cell")
    )
  
METHOD_SPECS+=(cell_methods,)

    
inserts  = {}

inserts['Network'] = '''
         
        import numpy
        
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
        
'''

inserts['Population'] = '''
         
        import numpy
        
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
        
'''

inserts['Projection'] = '''
         
        import numpy
        
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
        
        from neuroml.utils import has_segment_fraction_info
        
        include_segment_fraction = has_segment_fraction_info(self.connections) or has_segment_fraction_info(self.connection_wds)
        
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
            
        
        
'''

inserts['ElectricalProjection'] = '''
         
        import numpy
        
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
        
'''



inserts['ContinuousProjection'] = '''
         
        import numpy
        
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
            
        
'''


inserts['InputList'] = '''
         
        import numpy
        
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
        
'''


             
for insert in inserts.keys():
    ms = MethodSpec(name='exportHdf5',
    source='''\

    def exportHdf5(self, h5file, h5Group):
        #print("Exporting %s: "+str(self.id)+" as HDF5")
        %s
    '''%(insert,inserts[insert]),
    class_names=(insert)
    )
    METHOD_SPECS+=(ms,)


def test():
    for spec in METHOD_SPECS:
        spec.show()

def main():
    test()


if __name__ == '__main__':
    main()
