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

        #TODO: this should be extracted from the schema:
        namespacedef = 'xmlns="http://www.neuroml.org/schema/neuroml2" '
        namespacedef += ' xmlns:xi="http://www.w3.org/2001/XInclude"'
        namespacedef += ' xmlns:xs="http://www.w3.org/2001/XMLSchema"'
        namespacedef += ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        namespacedef += ' xsi:schemaLocation="http://www.w3.org/2001/XMLSchema"'

        nmldoc.export(file,0,name_="neuroml",
                      namespacedef_=namespacedef) #name_ param to ensure root element named correctly - generateDS limitation

class JSONWriter(object):
    """
    Write a NeuroMLDocument to JSON, particularly useful
    when dealing with lots of ArrayMorphs.
    """

    @classmethod
    def write(neuroml_document):
        if isinstance(neuroml_document,neuroml.NeuroMLDocument):
            import jsonpickle
            encoded = jsonpickle.encode(neuroml_document):
        else:
            raise NotImplementedError("Currently you can only serialize NeuroMLDocument type in JSON format")
        

class ArrayMorphWriter(object):
    """
    For now just testing a simple method which can write a morphology, not a NeuroMLDocument.
    """

    @classmethod
    def __write_single_cell(cls,array_morph,fileh,cell_id=None):
        vertices = array_morph.vertices
        connectivity = array_morph.connectivity
        physical_mask = array_morph.physical_mask

        # Get the HDF5 root group
        root = fileh.root
        
        # Create the groups:
        # can use morphology name in future?

        if array_morph.id == None:
            morphology_name = 'Morphology'
        else:
            morphology_name = array_morph.id

        if cell_id == None:
            morphology_group = fileh.createGroup(root, morphology_name)
            hierarchy_prefix = "/" + morphology_name
        else:
            cell_group = fileh.createGroup(root, cell_id)
            morphology_group = fileh.createGroup(cell_group, morphology_name)
            hierarchy_prefix = '/' + cell_id + '/' + morphology_name

        vertices_array = fileh.createArray(hierarchy_prefix, "vertices", vertices)
        connectivity_array = fileh.createArray(hierarchy_prefix, "connectivity", connectivity)
        physical_mask_array = fileh.createArray(hierarchy_prefix, "physical_mask", physical_mask)

    @classmethod
    def __write_neuroml_document(cls,document,fileh):
        document_id = document.id

        for default_id,cell in enumerate(document.cells):
            morphology = cell.morphology

            if morphology.id == None:
                morphology.id = 'Morphology' + str(default_id)
            if cell.id == None:
                cell.id = 'Cell' + str(default_id)

            cls.__write_single_cell(morphology,fileh,cell_id=cell.id)

        for default_id,morphology in enumerate(document.morphology):

            if morphology.id == None:
                morphology.id = 'Morphology' + str(default_id)

            cls.__write_single_cell(morphology,fileh,cell_id=cell.id)


    @classmethod
    def write(cls,data,filepath):

        fileh = tables.openFile(filepath, mode = "w")
        
        #Now instead we should go through a document/cell/morphology
        #hierarchy - this kind of tree traversal should be done recursively

        if isinstance(data,neuroml.arraymorph.ArrayMorphology):
            print "writing array morphology"
            cls.__write_single_cell(data, fileh)

        if isinstance(data,neuroml.NeuroMLDocument):
            print "writing neuroml document"
            cls.__write_neuroml_document(data,fileh)
            
        # Finally, close the file (this also will flush all the remaining buffers!)
        fileh.close()
