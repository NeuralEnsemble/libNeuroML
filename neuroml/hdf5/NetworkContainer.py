'''
Work in progress..

'''

import neuroml
import numpy as np



class NetworkContainer(neuroml.Network):
    
    def __getattr__(self,name):
        print('Requesting in NC: %s'%name)
    
    
    
class InstanceList(object):

    pos_array = None
    cursor = 0
    
    def __init__(self, pos_array=None):
        self.pos_array = pos_array
        #print("InstanceList created with %s "% self.pos_array)
    
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
        
        
    def __len__(self):
        length = self.pos_array.shape[0] if isinstance(self.pos_array,np.ndarray) else 0
        #print('Getting length %s: %s'%(length,self.pos_array))
        return length
    
    
    def __iadd__(self,instance_list):
        for i in instance_list:
            self.append(i)
        return self
    
    def __delitem__(self, index):
        
        raise NotImplementedError("__delitem__ is not implemented (yet) in HDF5 based instance list")

    def __getitem__(self,instance_index):

        print('Getting instance %s'%instance_index)
        
        assert(self.pos_array[instance_index][0]==instance_index)
        
        instance = neuroml.Instance(id=instance_index)
        instance.location = neuroml.Location(self.pos_array[instance_index][1],
                                             self.pos_array[instance_index][2],
                                             self.pos_array[instance_index][3])
        
        return instance

    def __setitem__(self,index,instance):
        
        raise NotImplementedError("__setitem__() is not implemented (yet) in HDF5 based instance list")
        
        
    def append(self,instance):
        
        print('Adding instance: %s'%instance)
        l = instance.location
        i = np.array([[instance.id,l.x,l.y,l.z]], np.float32)
        if len(self)==0:
            self.pos_array = i
        else:
            self.pos_array = np.concatenate((self.pos_array, i))
            
        
        
    def __str__(self):
        
        return "InstanceList (HDF5 based) with "+str( len(self) )+" entries"
        
        
    
class PopulationContainer(neuroml.Population):

    
    def __init__(self, neuro_lex_id=None, id=None, metaid=None, notes=None, properties=None, annotation=None, component=None, size=None, type=None, extracellular_properties=None, layout=None, instances=None):
        super(self.__class__, self).__init__(neuro_lex_id=neuro_lex_id, id=id, metaid=metaid, notes=notes, properties=properties, annotation=annotation, component=component, size=size, type=type, extracellular_properties=extracellular_properties, layout=layout, instances=instances)
    
        self.instances = InstanceList()
        
        print("PopulationContainer created")
        
    def info(self):
        return "%s: id=%s"%(self.__class__(),self.id)
    
    
    def __str__(self):
        
        return "Population (HDF5 based): "+str(self.id)+" with "+str( len(self.instances) )+" components of type "+(self.component if self.component else "???")
        
        

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
    
    
    
    nc2 = NetworkContainer(id="testnet2")
    
    pc2 = PopulationContainer(id="fake2", component="iaf",size=4)
    nc2.populations.append(pc2)
    
    print(pc)
    
    nets = [nc,nc2,net0]
    nets = [nc,nc2]
    
    for n in nets:
        print('\n--------------------------------')
        print(n)
        for p in n.populations:
            print("  %s"%p)
            print("  > %s"%(p.instances))
            for i in p.instances:
                print("    > %s"%i)
            
    nml_doc_c = neuroml.NeuroMLDocument(id="ndc")
    nml_doc_c.networks.append(nc)
    print(nml_doc_c.summary())
        
    print('\n++++++++++')
    
    file_name = '../examples/tmp/MediumNet.net.nml.h5'
    
    nml_doc = read_neuroml2_file(file_name,optimized=True,include_includes=True)
    
    print(nml_doc.summary())