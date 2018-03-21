'''
Work in progress..

'''

import neuroml
import numpy as np


class NetworkContainer(neuroml.Network):
    
    pass
    #def __getattr__(self,name):
    #    print('Requesting in NC: %s'%name)
    

class OptimizedList(object):
    
    array = None
    cursor = 0
    
    def __init__(self, array=None,indices={}):
        self.array = array
        self.indices = indices
        #print("Created %s with %s"% (self,indices))
        
        
    def _get_index_or_add(self,name,default_index):
        if not name in self.indices:
            self.indices[name] = default_index
            return default_index
        else:
            return self.indices[name]
        
    def _get_value(self,i,name,default_value):
        if not name in self.indices:
            return default_value
        else:
            return self.array[i][self.indices[name]]
        
    def _add_index_information(self,hdf5_array):
        for name in self.indices.keys():
            
            n="column_%i"%self.indices[name]
            #print("Adding attribute to H5 array: %s = %s"%(n,name))
            hdf5_array._f_setattr(n, name)
        
    def __len__(self):
        length = self.array.shape[0] if isinstance(self.array,np.ndarray) else 0
        #print('Getting length (%s) of %s'%(length,self.__class__.__name__,))
        return length
    
    def __iter__(self):
        self.cursor = 0
        return self
    
    def __next__(self):
        if self.cursor == len(self):
            raise StopIteration
        else:
            instance = self.__getitem__(self.cursor)
            self.cursor +=1
            return instance

    def next(self):
        return self.__next__()
    
    def __iadd__(self,i_list):
        for i in i_list:
            self.append(i)
        return self
    
    def __delitem__(self, index):
        
        raise NotImplementedError("__delitem__ is not implemented (yet) in HDF5 based optimized list")

    def __setitem__(self,index,instance):
        
        raise NotImplementedError("__setitem__() is not implemented (yet) in HDF5 based instance list")
    
    def __str__(self):
        
        return "%s (optimized) with %s entries"%(self.__class__.__name__,len(self))
        
    
class InstanceList(OptimizedList):


    def __getitem__(self,index):

        if len(self.array[index])==4:
            id = self.array[index][self._get_index_or_add('id',0)]
            #print('    Getting instance %s in %s (%s)'%(index,self,id))
            assert(id==index)
        else:
            id = index
        
        instance = neuroml.Instance(id=id)
        instance.location = neuroml.Location(self.array[index][self._get_index_or_add('x',1)],
                                             self.array[index][self._get_index_or_add('y',2)],
                                             self.array[index][self._get_index_or_add('z',3)])
        
        return instance
        
        
    def append(self,instance):
        
        #print('Adding instance: %s'%instance)
        l = instance.location
        i = np.array([[instance.id,l.x,l.y,l.z]], np.float32)
        if len(self)==0:
            self.array = i
        else:
            self.array = np.concatenate((self.array, i))
            
    def add_instance(self,id,x,y,z):
        
        i = np.array([[id,x,y,z]], np.float32)
        if len(self)==0:
            self.array = i
        else:
            self.array = np.concatenate((self.array, i))
            
        
        
    
class PopulationContainer(neuroml.Population):

    
    def __init__(self, neuro_lex_id=None, id=None, metaid=None, notes=None, properties=None, annotation=None, component=None, size=None, type=None, extracellular_properties=None, layout=None, instances=None):
        super(self.__class__, self).__init__(neuro_lex_id=neuro_lex_id, id=id, metaid=metaid, notes=notes, properties=properties, annotation=annotation, component=component, size=size, type=type, extracellular_properties=extracellular_properties, layout=layout, instances=instances)
    
        self.instances = InstanceList()
        
        #print("PopulationContainer created")
    
    def __str__(self):
        
        return "Population (optimized): "+str(self.id)+" with "+str( self.get_size() )+" components of type "+(self.component if self.component else "???")
        
    def exportHdf5(self, h5file, h5Group):
        #print("Exporting %s as HDF5..."%self)
        
        popGroup = h5file.create_group(h5Group, 'population_'+self.id)
        popGroup._f_setattr("id", self.id)
        popGroup._f_setattr("component", self.component)
        
        for p in self.properties:
            popGroup._f_setattr("property:%s"%p.tag, p)
            
        if len(self.instances)>0:

            popGroup._f_setattr("size", len(self.instances))
            popGroup._f_setattr("type", "populationList")

            h5array = h5file.create_carray(popGroup, self.id, obj=self.instances.array, title="Locations of cells in "+ self.id)
            
            self.instances._add_index_information(h5array)
            
        else:
            popGroup._f_setattr("size", self.size)
            
            
class ProjectionContainer(neuroml.Projection):
    
    def __init__(self, neuro_lex_id=None, id=None, presynaptic_population=None, postsynaptic_population=None, synapse=None, connections=None, connection_wds=None):
        
        super(self.__class__, self).__init__(neuro_lex_id=neuro_lex_id, id=id, presynaptic_population=presynaptic_population,postsynaptic_population=postsynaptic_population,synapse=synapse,connections=connections,connection_wds=connection_wds)
    
        assert(connections==None)
        assert(connection_wds==None)
        self.connections = ConnectionList()
        self.connection_wds = ConnectionList()
        self.connections.presynaptic_population = presynaptic_population
        self.connections.postsynaptic_population = postsynaptic_population
        
        
    def __str__(self):
        return "Projection (optimized): "+self.id+" from "+self.presynaptic_population+" to "+self.postsynaptic_population+", synapse: "+self.synapse
        
            
    def exportHdf5(self, h5file, h5Group):
        #print("Exporting %s as HDF5"%self)
        
        projGroup = h5file.create_group(h5Group, 'projection_'+self.id)
        projGroup._f_setattr("id", self.id)
        projGroup._f_setattr("type", "projection")
        projGroup._f_setattr("presynapticPopulation", self.presynaptic_population)
        projGroup._f_setattr("postsynapticPopulation", self.postsynaptic_population)
        projGroup._f_setattr("synapse", self.synapse)
            
        h5array = h5file.create_carray(projGroup, self.id, obj=self.connections.array, title="Connections of cells in "+ self.id)
        
        self.connections._add_index_information(h5array)
         
            
##
##      TODO: update this to act like ElectricalProjection
##
class ElectricalProjectionContainer(neuroml.ElectricalProjection):
    
    def __init__(self, neuro_lex_id=None, id=None, presynaptic_population=None, postsynaptic_population=None, electrical_connections=None, electrical_connection_instances=None):
        
        super(self.__class__, self).__init__(neuro_lex_id=neuro_lex_id, id=id, presynaptic_population=presynaptic_population,postsynaptic_population=postsynaptic_population,electrical_connections=electrical_connections,electrical_connection_instances=electrical_connection_instances)
    
        assert(electrical_connections==None)
        assert(electrical_connection_instances==None)
        self.connections = ConnectionList()
        self.connection_wds = ConnectionList()
        self.connections.presynaptic_population = presynaptic_population
        self.connections.postsynaptic_population = postsynaptic_population
        
        
    def __str__(self):
        return "Electrical projection (optimized): "+self.id+" from "+self.presynaptic_population+" to "+self.postsynaptic_population+", synapse: "+self.synapse
        
            
    def exportHdf5(self, h5file, h5Group):
        #print("Exporting %s as HDF5"%self)
        
        projGroup = h5file.create_group(h5Group, 'projection_'+self.id)
        projGroup._f_setattr("id", self.id)
        projGroup._f_setattr("type", "projection")
        projGroup._f_setattr("presynapticPopulation", self.presynaptic_population)
        projGroup._f_setattr("postsynapticPopulation", self.postsynaptic_population)
        projGroup._f_setattr("synapse", self.synapse)
            
        h5array = h5file.create_carray(projGroup, self.id, obj=self.connections.array, title="Connections of cells in "+ self.id)
        
        self.connections._add_index_information(h5array)
        
        
class ConnectionList(OptimizedList):

    presynaptic_population = None
    postsynaptic_population = None
    
    def __getitem__(self,index):

        id_index = self._get_index_or_add('id',-1)
        if id_index>0:
            id = int(self.array[index][id_index])
            assert(self.array[index][0]==index)
        else:
            id = index
        
        pre_cell_id =  int(self.array[index][self._get_index_or_add('pre_cell_id',1)])
        post_cell_id = int(self.array[index][self._get_index_or_add('post_cell_id',2)])
        pre_segment_id = int(self._get_value(index,'pre_segment_id',0))
        post_segment_id = int(self._get_value(index,'post_segment_id',0))
        pre_fraction_along = float(self._get_value(index,'pre_fraction_along',0.5))
        post_fraction_along = float(self._get_value(index,'post_fraction_along',0.5))
        
        input = neuroml.Connection(id=id,
                  pre_cell_id="../%s/%i/%s"%(self.presynaptic_population,pre_cell_id,"???"),
                  post_cell_id="../%s/%i/%s"%(self.postsynaptic_population,post_cell_id,"???"),
                  pre_segment_id=pre_segment_id,
                  post_segment_id=post_segment_id,
                  pre_fraction_along=pre_fraction_along,
                  post_fraction_along=post_fraction_along)  
        
        return input
        
        
    def append(self,conn):
        
        i = np.array([[conn.id,
                       conn.get_pre_cell_id(),
                       conn.get_post_cell_id()]], np.float32)
                       
        if len(self)==0:
            self.array = i
        else:
            self.array = np.concatenate((self.array, i))
        
        
class InputListContainer(neuroml.InputList):
    
    def __init__(self, neuro_lex_id=None, id=None, populations=None, component=None, input=None):
        super(self.__class__, self).__init__(neuro_lex_id=neuro_lex_id, id=id, populations=populations, component=component, input=input)
    
        assert(input==None)
        self.input = InputsList()
        self.input.target_population = populations
        
        #print("InputListContainer %s created"%self.id)
        
    def __str__(self):
        
        return "Input list (optimized): "+self.id+" to "+self.populations+", component "+self.component
    
    def exportHdf5(self, h5file, h5Group):
        #print("Exporting %s as HDF5"%self)
        
        ilGroup = h5file.create_group(h5Group, 'inputList_'+self.id)
        ilGroup._f_setattr("id", self.id)
        ilGroup._f_setattr("component", self.component)
        ilGroup._f_setattr("population", self.populations)
        
            
        h5array = h5file.create_carray(ilGroup, self.id, obj=self.input.array , title="Locations of inputs in "+ self.id)
            
        self.input._add_index_information(h5array)
        
        
        
        
    
class InputsList(OptimizedList):

    target_population = None
    
    def __getitem__(self,index):

        #print('    Getting instance %s'%(index))
        #print self.array
        
        id = self.array[index][self._get_index_or_add('id',0)]
        assert(id==index)
        
        target_cell_id = int(self.array[index][self._get_index_or_add('target_cell_id',1)])
        segment_id = int(self.array[index][self._get_index_or_add('segment_id',1)])
        fraction_along = float(self.array[index][self._get_index_or_add('fraction_along',1)])
        
        input = neuroml.Input(id=index,
                  target="../%s/%i/%s"%(self.target_population, target_cell_id, "???"), 
                  destination="synapses",
                  segment_id=segment_id,
                  fraction_along=fraction_along)  
        
        return input
        
        
    def append(self,input):
        
        #print('Adding input: %s'%input)
        
        i = np.array([[input.id,
                       input.get_target_cell_id(),
                       input.get_segment_id(),
                       input.get_fraction_along()]], np.float32)
                       
        if len(self)==0:
            self.array = i
        else:
            self.array = np.concatenate((self.array, i))
        

if __name__ == '__main__':
    
    from neuroml.loaders import read_neuroml2_file
    
    
    file_name = '../examples/test_files/MediumNet.net.nml'
    
    nml_doc = read_neuroml2_file(file_name,include_includes=True)
    
    print(nml_doc.summary())
    
    net0 = nml_doc.networks[0]
    
    nc = NetworkContainer(id="testnet")
    pc0 = PopulationContainer(id="pre", component="iffy",size=4)
    nc.populations.append(pc0)
    pc = PopulationContainer(id="fake", component="izzy")
    nc.populations.append(pc)
    instance = neuroml.Instance(0)
    instance.location = neuroml.Location(100,100,33.333)
    pc.instances.append(instance)
    instance = neuroml.Instance(1)
    instance.location = neuroml.Location(200,200,66.66)
    pc.instances.append(instance)
    
    prc = ProjectionContainer(id="proj", presynaptic_population=pc0.id, postsynaptic_population=pc.id,synapse="ampa")
    
    conn = neuroml.Connection(id=0,
                                    pre_cell_id="../%s/%i/%s"%(pc0.id,0,pc0.component), \
                                    pre_segment_id=2, \
                                    pre_fraction_along=0.1,
                                    post_cell_id="../%s/%i/%s"%(pc.id,2,pc.id))
    prc.connections.append(conn)    
    nc.projections.append(prc)
    
    ilc = InputListContainer(id="iii",component="CCC",populations=pc.id)
    nc.input_lists.append(ilc)
    ilc.input.append(neuroml.Input(id=0,target="../pyramidals_48/37/pyr_4_sym", destination="synapses", segment_id="2", fraction_along="0.3"))
    
    
    nc2 = NetworkContainer(id="testnet2")
    
    pc2 = PopulationContainer(id="fake2", component="iaf",size=4)
    nc2.populations.append(pc2)
    
    print(pc)
    
    nets = [nc,nc2,net0]
    nets = [nc]
    
    for n in nets:
        print('\n--------------------------------')
        print(n)
        for p in n.populations:
            print("  %s"%p)
            print("  > %s"%(p.instances))
            for i in p.instances:
                print("    > %s"%i)
        for pr in n.projections:
            print("  %s"%pr)
            print("  > %s"%(pr.connections))
            for c in pr.connections:
                print("    > %s"%c)
        for il in n.input_lists:
            print("  %s"%il)
            for i in il.input:
                print("    > %s"%i)
            
    nml_doc_c = neuroml.NeuroMLDocument(id="ndc")
    nml_doc_c.networks.append(nc)
    print('\n++++++++++')
    print(nml_doc_c.summary())
        
    print('\n++++++++++')
    exit()
    
    file_name = '../examples/tmp/MediumNet.net.nml.h5'
    
    nml_doc = read_neuroml2_file(file_name,optimized=True,include_includes=True)
    
    print(nml_doc.summary())
    
    file_name = '../examples/tmp/MediumNet2.net.nml.h5'
    
    from neuroml.writers import NeuroMLHdf5Writer
    
    NeuroMLHdf5Writer.write(nml_doc,file_name)
    
    print("Rewritten to %s"%file_name)