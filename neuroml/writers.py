import neuroml
import numpy as np

class NeuroMLWriter(object):
    @classmethod
    def write(cls,nmldoc,file_path):
        """
        Writes from NeuroMLDocument to nml file
        in future can implement from other types
        via chain of responsibility pattern.
        """

        #TODO: this needs to be extracted from the schema:
        namespacedef = 'xmlns="http://www.neuroml.org/schema/neuroml2" '
        namespacedef += ' xmlns:xi="http://www.w3.org/2001/XInclude"'
        namespacedef += ' xmlns:xs="http://www.w3.org/2001/XMLSchema"'
        namespacedef += ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        namespacedef += ' xsi:schemaLocation="http://www.w3.org/2001/XMLSchema"'

        f = open(file_path,'w')
        nmldoc.export(f,0,name_="neuroml",
                      namespacedef_=namespacedef) #name_ param to ensure root element named correctly - generateDS limitation

class ArrayMorphWriter(object):
    @classmethod
    def write(cls,arraymorph,file_path):

        import h5py

        f = h5py.File(file_path,'w')
        identifier = arraymorph.id

        f['vertices_'+str(identifier)] = arraymorph.vertices
        f['connectivity_'+str(identifier)] = arraymorph.connectivity

        f.close()
