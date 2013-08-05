import neuroml
import numpy as np
import tables


class NeuroMLWriter(object):
    @classmethod
    def write(cls,nmldoc,file):
        """
        Writes from NeuroMLDocument to nml file
        in future can implement from other types
        via chain of responsibility pattern.
        """

        if isinstance(file,str):
            file = open(file,'w')

        #TODO: this needs to be extracted from the schema:
        namespacedef = 'xmlns="http://www.neuroml.org/schema/neuroml2" '
        namespacedef += ' xmlns:xi="http://www.w3.org/2001/XInclude"'
        namespacedef += ' xmlns:xs="http://www.w3.org/2001/XMLSchema"'
        namespacedef += ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        namespacedef += ' xsi:schemaLocation="http://www.w3.org/2001/XMLSchema"'

        nmldoc.export(file,0,name_="neuroml",
                      namespacedef_=namespacedef) #name_ param to ensure root element named correctly - generateDS limitation

class HDF5ArrayMorph(tables.IsDescription):
    vertices = tables.Float32Col(dflt=1, pos = 1)
    connectivity =  tables.Float32Col(dflt=1, pos = 1)
    physical_mask = tables.Float32Col(dflt=1, pos = 1)


class ArrayMorphWriter(object):
    """
    For now just testing a simple method which can write a morphology, not a NeuroMLDocument.
    """

    @classmethod
    def __write_single_morphology(cls,array_morph,fileh):
        vertices = array_morph.vertices
        connectivity = array_morph.connectivity
        physical_mask = array_morph.physical_mask

        # Get the HDF5 root group
        root = fileh.root
        
        # Create the groups:
        # can use morphology name in future?
        morphology_name = "morphology_1"
        morphology_group = fileh.createGroup(root, morphology_name)

        # Now, create an array in root group
        vertices_array = fileh.createArray("/"+morphology_name, "vertices", vertices)
        connectivity_array = fileh.createArray("/"+morphology_name, "connectivity", connectivity)
        physical_mask_array = fileh.createArray("/"+morphology_name, "physical_mask", physical_mask)

    @classmethod
    def write(cls,array_morph,filepath):

        assert isinstance(array_morph,neuroml.Morphology)

        # Open a file in "w"rite mode
        fileh = tables.openFile(filepath, mode = "w")
        
        #Now instead we should go through a document/cell/morphology
        #hierarchy - this kind of tree traversal should be done recursively

        cls.__write_single_morphology(array_morph, fileh)

        # Finally, close the file (this also will flush all the remaining buffers!)
        fileh.close()
