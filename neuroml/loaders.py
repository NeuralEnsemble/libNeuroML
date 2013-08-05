import numpy as np
from nml.nml import parse as nmlparse
from neuroml import arraymorph

class NeuroMLLoader(object):

    @classmethod
    def load(cls,src):
        doc = cls.__nml2_doc(src)
        return doc

    @classmethod    
    def __nml2_doc(cls,src):
        import sys

        try:
            nml2_doc = nmlparse(src)
        except Exception:
            print("Not a valid NeuroML 2 doc: %s" % str(sys.exc_info())) 
            return None    
        return nml2_doc


class SWCLoader(object):
    """
    WARNING: Class defunct
    """
    
    @classmethod
    def load_swc_single(cls,  src, name=None):
      
        dtype= {'names':   ('id', 'type', 'x','y','z','r','pid'),
                'formats': ('int32', 'int32', 'f4','f4','f4','f4','int32') }
        
        d = np.loadtxt(src,dtype=dtype )
        
        if len( np.nonzero( d['pid']==-1)) != 1:
            assert False, "Unexpected number of id's of -1 in file" 
            
        num_nodes=len(d['pid'])

        root_index=np.where(d['pid']==-1)[0][0]
 
        # We might not nessesarily have continuous indices in the 
        # SWC file, so lets convert them:
        index_to_id = d['id']
        id_to_index_dict = dict( [(id,index) for index,id in enumerate(index_to_id) ] )

        if len(id_to_index_dict) != len(index_to_id):
            s =  "Internal Error Loading SWC: Index and ID map are different lengths."
            s += " [ID:%d, Index:%d]"%( len(index_to_id), len(id_to_index_dict) )
            raise MorphologyImportError(s)
        
        # Vertices and section types are easy:
        vertices =  d[ ['x','y','z','r'] ]
        vertices =  np.vstack( [d['x'], d['y'],d['z'],d['r'] ]).T
        section_types = [ swctype for ID,swctype in d[['id','type']]]

        #for connection indices we want the root to have index -1:
        connection_indices=np.zeros(num_nodes,dtype='int32')
        for i in range(num_nodes):
            pID=d['pid'][i]
            if pID !=-1:
                parent_index=id_to_index_dict[pID]
                connection_indices[i]=parent_index
            else:
                connection_indices[i]=-1

        #This needs to become an "Optimized Morphology" of some kind
        return Backend(vertices=vertices, 
                       connectivity=connection_indices, 
                       name=name )

class ArrayMorphLoader(object):

    @classmethod
    def load(cls, filepath):
        import tables
        file = tables.openFile(filepath,mode='r')

        loaded_morphology = arraymorph.ArrayMorphology()

        for morphology in file.root:
            loaded_morphology.physical_mask = morphology.physical_mask[:]
            loaded_morphology.vertices = morphology.vertices[:]
            loaded_morphology.connectivity = morphology.connectivity[:]

        return loaded_morphology
            
