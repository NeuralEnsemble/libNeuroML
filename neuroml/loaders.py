
from neuroml.nml.nml import parse as nmlparse
import neuroml
import os
import inspect
import sys

def print_(msg, verbose=True):
    if verbose:
        print(msg)

def read_neuroml2_file(nml2_file_name, include_includes=False, verbose=False, 
                       already_included=[], print_method=print_):  
    
    print_method("Loading NeuroML2 file: %s" % nml2_file_name, verbose)
    
    if not os.path.isfile(nml2_file_name):
        print_method("Unable to find file: %s!" % nml2_file_name, True)
        sys.exit()
        
    if nml2_file_name.endswith('.h5') or nml2_file_name.endswith('.hdf5'):
        nml2_doc = NeuroMLHdf5Loader.load(nml2_file_name)
    else:
        nml2_doc = NeuroMLLoader.load(nml2_file_name)
    
    base_path = os.path.dirname(os.path.realpath(nml2_file_name))
    
    if include_includes:
        print_method('Including included files (included already: %s)' \
                      % already_included, verbose)
        
        for include in nml2_doc.includes:
            incl_loc = os.path.abspath(os.path.join(base_path, include.href))
            if incl_loc not in already_included:
                print_method("Loading included NeuroML2 file: %s (base: %s, resolved: %s)" % (include.href, base_path, incl_loc), 
                              verbose)
                nml2_sub_doc = read_neuroml2_file(incl_loc, True, 
                    verbose=verbose, already_included=already_included)
                already_included.append(incl_loc)
                
                membs = inspect.getmembers(nml2_sub_doc)

                for memb in membs:
                    if isinstance(memb[1], list) and len(memb[1])>0 \
                            and not memb[0].endswith('_'):
                        for entry in memb[1]:
                            if memb[0] != 'includes':
                                print_method("  Adding %s from: %s to list: %s" \
                                    %(entry.id if hasattr(entry,'id') else entry.name, incl_loc, memb[0]),verbose)
                                getattr(nml2_doc, memb[0]).append(entry)
                            
        nml2_doc.includes = []
            
    return nml2_doc

class NeuroMLLoader(object):

    @classmethod
    def load(cls,src):
        doc = cls.__nml2_doc(src)
        return doc

    @classmethod    
    def __nml2_doc(cls,file_name):
        import sys

        try:
            nml2_doc = nmlparse(file_name)
        except Exception:
            print("Not a valid NeuroML 2 doc: %s" % str(sys.exc_info())) 
            return None    
        return nml2_doc

class NeuroMLHdf5Loader(object):

    @classmethod
    def load(cls,src):
        doc = cls.__nml2_doc(src)
        return doc

    @classmethod    
    def __nml2_doc(cls,file_name):
        import sys
        
        import logging
        logging.basicConfig(level=logging.INFO, format="%(name)-19s %(levelname)-5s - %(message)s")
        
        from neuroml.hdf5.NetworkBuilder import NetworkBuilder
        from neuroml.hdf5.NeuroMLHdf5Parser import NeuroMLHdf5Parser
        
        try:
            nmlHandler = NetworkBuilder()   

            currParser = NeuroMLHdf5Parser(nmlHandler) 

            currParser.parse(file_name)

            nml2_doc = nmlHandler.get_nml_doc()
            
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
        
        import numpy as np
        from neuroml import arraymorph
      
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
        return arraymorph.ArrayMorphology(vertices=vertices, 
                       connectivity=connection_indices, 
                       name=name )

class JSONLoader(object):

    @classmethod
    def load(cls,file):

        from jsonpickle import decode as json_decode
        if isinstance(file,str):
            fileh = open(file,'r')
        else:
            fileh = file

        json_string = fileh.read()
        unpickled = json_decode(json_string)
        return unpickled
        
    @classmethod
    def load_from_mongodb(cls,
                          db,
                          id,
                          host=None,
                          port=None):
        
        from pymongo import MongoClient
        try:
            import simplejson as json
        except ImportError:
            import json
        
        from jsonpickle import decode as json_decode

        if host == None:
            host = 'localhost'
        if port == None:
            port = 27017

        client = MongoClient(host,port)

        db = client[db]

        collection = db[id]

        doc = collection.find_one()

        del doc['_id']         

        doc = json.dumps(doc)

        document = json_decode(doc)

        return document
        
class ArrayMorphLoader(object):

    @classmethod
    def __extract_morphology(cls, node):
        
            from neuroml import arraymorph
            
            loaded_morphology = arraymorph.ArrayMorphology()
            loaded_morphology.physical_mask = node.physical_mask[:]
            loaded_morphology.vertices = node.vertices[:]
            loaded_morphology.connectivity = node.connectivity[:]

            return loaded_morphology

    @classmethod
    def load(cls, filepath):
        """
        Right now this load method isn't done in a very nice way.
        TODO: Complete refactoring.
        """
        import tables
        file = tables.openFile(filepath,mode='r')

        document = neuroml.NeuroMLDocument()

        for node in file.root:
            if hasattr(node,'vertices'):
                loaded_morphology = cls.__extract_morphology(node)
                document.morphology.append(loaded_morphology)
            else:
                for morphology in node:
                    loaded_morphology = cls.__extract_morphology(morphology)
                    document.morphology.append(loaded_morphology)
                
        return document
            
    
