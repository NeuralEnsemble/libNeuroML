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
        if class_names is None:
            self.class_names = ('.*', )
        else:
            self.class_names = class_names
        if class_names_compiled is None:
            self.class_names_compiled = re.compile(self.class_names)
        else:
            self.class_names_compiled = class_names_compiled
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
        if self.class_names_compiled.search(class_name):
            return True
        else:
            return False
    def get_interpolated_source(self, values_dict):
        """Get the method source code, interpolating values from values_dict
        into it.  The source returned by this method is inserted into
        the generated class.
        """
        source = self.source % values_dict
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
        
    def __str__(self):
        
        return "Connection "+str(self.id)+": "+str(self.get_pre_cell_id())+" -> "+str(self.get_post_cell_id())
        
    ''',
    class_names=("Connection")
    )
  
METHOD_SPECS+=(connection_cell_ids,)
    
connection_wd_cell_ids = MethodSpec(name='connection_wd_cell_ids',
    source='''\
        
    def __str__(self):
        
        return "Connection "+str(self.id)+": "+str(self.get_pre_cell_id())+" -> "+str(self.get_post_cell_id())+ \
            ", weight: "+str(self.weight)+", delay: "+str(self.delay)
        
    ''',
    class_names=("ConnectionWD")
    )
  
METHOD_SPECS+=(connection_wd_cell_ids,)


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
        
        return self.segment_id if self.segment_id else 0

    def get_fraction_along(self):
        
        return self.fraction_along if self.fraction_along else 0.5
        
    ''',
    class_names=("Input")
    )
  
METHOD_SPECS+=(input_cell_ids,)


nml_doc_summary = MethodSpec(name='summary',
    source='''\

    def summary(self):
        print("*******************************************************")
        print("* NeuroMLDocument: "+self.id)
        for network in self.networks:
            print("*  Network: "+network.id)
            for pop in network.populations:
                print("*   Population: "+pop.id+" with "+str(pop.size)+" components of type "+pop.component)
            for proj in network.projections:
                print("*   Projection: "+proj.id+" from "+proj.presynaptic_population+" to "+proj.postsynaptic_population)
                if len(proj.connections)>0:
                    print("*     "+str(len(proj.connections))+" connections: "+str(proj.connections[0]))
                if len(proj.connection_wds)>0:
                    print("*     "+str(len(proj.connection_wds))+" connections (wd): "+str(proj.connection_wds[0]))
        
        print("*******************************************************")
        
        
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
        print("Id "+id+" not found. All ids: "+str(all_ids))
        return None
    ''',
    class_names=("NeuroMLDocument")
    )
  
METHOD_SPECS+=(nml_doc_summary,)

    
inserts  = {}

inserts['Network'] = '''
         
        import numpy
        
        netGroup = h5file.createGroup(h5Group, 'network')
        netGroup._f_setAttr("id", self.id)
        netGroup._f_setAttr("notes", self.notes)
       
        for pop in self.populations:
            pop.exportHdf5(h5file, netGroup)
            
        if len(self.synaptic_connections) > 0:
            raise Exception("<synapticConnection> not yet supported in HDF5 export")
        if len(self.explicit_inputs) > 0:
            raise Exception("<explicitInput> not yet supported in HDF5 export")

        for proj in self.projections:
            proj.exportHdf5(h5file, netGroup)
            
        for il in self.input_lists:
            il.exportHdf5(h5file, netGroup)
        
'''

inserts['Population'] = '''
         
        import numpy
        
        popGroup = h5file.createGroup(h5Group, 'population_'+self.id)
        popGroup._f_setAttr("id", self.id)
        popGroup._f_setAttr("component", self.component)
        
        if len(self.instances)>0:

            colCount = 4
            a = numpy.ones([len(self.instances), colCount], numpy.float32)

            count=0
            for instance in self.instances:
              a[count,0] = instance.id
              a[count,1] = instance.location.x
              a[count,2] = instance.location.y
              a[count,3] = instance.location.z

              count=count+1
        
            popGroup._f_setAttr("size", count)
            popGroup._f_setAttr("type", "populationList")

            h5file.createArray(popGroup, self.id, a, "Locations of cells in "+ self.id)
            
        else:
            popGroup._f_setAttr("size", self.size)
        
        
'''

inserts['Projection'] = '''
         
        import numpy
        
        projGroup = h5file.createGroup(h5Group, 'projection_'+self.id)
        projGroup._f_setAttr("id", self.id)
        projGroup._f_setAttr("presynapticPopulation", self.presynaptic_population)
        projGroup._f_setAttr("postsynapticPopulation", self.postsynaptic_population)
        projGroup._f_setAttr("synapse", self.synapse)
        
        print("Exporting "+str(len(self.connections))+" connections, "+str(len(self.connection_wds))+" connections with weight")
        
        connection_wds = len(self.connection_wds) > 0
        
        cols = 7
        extra_cols = {}
        
        if connection_wds:
            cols = 9
            extra_cols["column_7"] = "weight"
            extra_cols["column_8"] = "delay"
        
        #TODO: optimise ...for conn in self.connections:
        #    if
        
        a = numpy.ones([len(self.connections)+len(self.connection_wds), cols], numpy.float32)
        
        
        count=0
        
        for connection in self.connections:
          a[count,0] = connection.id
          a[count,1] = connection.get_pre_cell_id()
          a[count,2] = connection.get_post_cell_id()  
          a[count,3] = connection.pre_segment_id  
          a[count,4] = connection.post_segment_id  
          a[count,5] = connection.pre_fraction_along 
          a[count,6] = connection.post_fraction_along          
          count=count+1
          
        for connection in self.connection_wds:
          a[count,0] = connection.id
          a[count,1] = connection.get_pre_cell_id()
          a[count,2] = connection.get_post_cell_id()  
          a[count,3] = connection.pre_segment_id  
          a[count,4] = connection.post_segment_id  
          a[count,5] = connection.pre_fraction_along 
          a[count,6] = connection.post_fraction_along        
          a[count,7] = connection.weight  
          if 'ms' in connection.delay:
            delay = float(connection.delay[:-2].strip())/1000.0
          elif 's' in connection.delay:
            delay = float(connection.delay[:-1].strip())
          elif 'us' in connection.delay:
            delay = float(connection.delay[:-2].strip())/1e6
            
          a[count,8] = delay          
          count=count+1
        
            
        array = h5file.createArray(projGroup, self.id, a, "Connections of cells in "+ self.id)
        
        array._f_setAttr("column_0", "id")
        array._f_setAttr("column_1", "pre_cell_id")
        array._f_setAttr("column_2", "post_cell_id")
        array._f_setAttr("column_3", "pre_segment_id")
        array._f_setAttr("column_4", "post_segment_id")
        array._f_setAttr("column_5", "pre_fraction_along")
        array._f_setAttr("column_6", "post_fraction_along")
        
        for col in extra_cols.keys():
            array._f_setAttr(col,extra_cols[col])
            
        
        
'''


inserts['InputList'] = '''
         
        import numpy
        
        ilGroup = h5file.createGroup(h5Group, 'input_list_'+self.id)
        ilGroup._f_setAttr("id", self.id)
        ilGroup._f_setAttr("component", self.component)
        ilGroup._f_setAttr("population", self.populations)
        
        colCount = 2
        a = numpy.ones([len(self.input), colCount], numpy.float32)
        
        count=0
        for input in self.input:
            a[count,0] = input.id
            a[count,1] = input.get_target_cell_id()
            count+=1
            
        h5file.createArray(ilGroup, self.id, a, "Locations of inputs in "+ self.id)
        
'''


             
for insert in inserts.keys():
    ms = MethodSpec(name='exportHdf5',
    source='''\

    def exportHdf5(self, h5file, h5Group):
        print("Exporting %s: "+str(self.id)+" as HDF5")
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
