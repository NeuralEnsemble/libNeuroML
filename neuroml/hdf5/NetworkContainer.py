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
    
    def __init__(self, array=None):
        self.array = array
        print("Created %s "% self)
        
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
        
        return "%s (HDF5 based) with %s entries"%(self.__class__.__name__,len(self))
        
    
class InstanceList(OptimizedList):


    def __getitem__(self,index):

        #print('    Getting instance %s in %s'%(index,self))
        
        assert(self.array[index][0]==index)
        
        instance = neuroml.Instance(id=index)
        instance.location = neuroml.Location(self.array[index][1],
                                             self.array[index][2],
                                             self.array[index][3])
        
        return instance
        
        
    def append(self,instance):
        
        print('Adding instance: %s'%instance)
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
        
        print("PopulationContainer created")
    
    def __str__(self):
        
        return "Population (HDF5 based): "+str(self.id)+" with "+str( len(self.instances) )+" components of type "+(self.component if self.component else "???")
        
    def exportHdf5(self, h5file, h5Group):
        print("Exporting %s as HDF5"%self)
        
        popGroup = h5file.create_group(h5Group, 'population_'+self.id)
        popGroup._f_setattr("id", self.id)
        popGroup._f_setattr("component", self.component)
        
        if len(self.instances)>0:

            popGroup._f_setattr("size", len(self.instances))
            popGroup._f_setattr("type", "populationList")

            h5file.create_carray(popGroup, self.id, obj=self.instances.array, title="Locations of cells in "+ self.id)
            
        else:
            popGroup._f_setattr("size", self.size)
        
        
class InputListContainer(neuroml.InputList):

    
    def __init__(self, neuro_lex_id=None, id=None, populations=None, component=None, input=None):
        super(self.__class__, self).__init__(neuro_lex_id=neuro_lex_id, id=id, populations=populations, component=component, input=input)
    
        assert(input==None)
        self.input = InputsList()
        self.input.target_population = populations
        
        print("InputListContainer %s created"%self.id)
        
    def __str__(self):
        
        return "Input list (HDF5 based): "+self.id+" to "+self.populations+", component "+self.component
    
    def exportHdf5(self, h5file, h5Group):
        print("Exporting %s as HDF5"%self)
        
        ilGroup = h5file.create_group(h5Group, 'inputList_'+self.id)
        ilGroup._f_setattr("id", self.id)
        ilGroup._f_setattr("component", self.component)
        ilGroup._f_setattr("population", self.populations)
        
            
        array = h5file.create_carray(ilGroup, self.id, obj=self.input.array , title="Locations of inputs in "+ self.id)
            
        array._f_setattr("column_0", "id")
        array._f_setattr("column_1", "target_cell_id")
        array._f_setattr("column_2", "segment_id")
        array._f_setattr("column_3", "fraction_along")
        
        
    
class InputsList(OptimizedList):

    target_population = None
    
    def __getitem__(self,index):

        #print('    Getting instance %s'%(index))
        #print self.array
        
        assert(self.array[index][0]==index)
        
        cell_id = int(self.array[index][1])
        segment_id = int(self.array[index][2])
        fraction_along = float(self.array[index][3])
        
        input = neuroml.Input(id=index,
                  target="../%s/%i/%s"%(self.target_population, cell_id, "???"), 
                  destination="synapses",
                  segment_id=segment_id,
                  fraction_along=fraction_along)  
        
        return input
        
        
    def append(self,input):
        
        print('Adding input: %s'%input)
        
        i = np.array([[input.id,
                       input.get_target_cell_id(),
                       input.get_segment_id(),
                       input.get_fraction_along()]], np.float32)
                       
        if len(self)==0:
            self.array = i
        else:
            self.array = np.concatenate((self.array, i))
            
    '''
    def add_instance(self,id,x,y,z):
        
        i = np.array([[id,x,y,z]], np.float32)
        if len(self)==0:
            self.array = i
        else:
            self.array = np.concatenate((self.array, i))'''
        

if __name__ == '__main__':
    
    from neuroml.loaders import read_neuroml2_file
    
    
    file_name = '../examples/test_files/MediumNet.net.nml'
    
    nml_doc = read_neuroml2_file(file_name,include_includes=True)
    
    print(nml_doc.summary())
    
    net0 = nml_doc.networks[0]
    
    nc = NetworkContainer(id="testnet")
    pc = PopulationContainer(id="fake", component="izzy")
    nc.populations.append(pc)
    instance = neuroml.Instance(0)
    instance.location = neuroml.Location(100,100,33.333)
    pc.instances.append(instance)
    instance = neuroml.Instance(1)
    instance.location = neuroml.Location(200,200,66.66)
    pc.instances.append(instance)
    
    ilc = InputListContainer(id="iii",component="BackgroundRandomIClamps",populations=pc.id)
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