import neuroml


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
        namespacedef += ' xmlns:xs="http://www.w3.org/2001/XMLSchema"'
        namespacedef += ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        namespacedef += ' xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_%s.xsd"'%neuroml.current_neuroml_version

        nmldoc.export(file,0,name_="neuroml",
                      namespacedef_=namespacedef) #name_ param to ensure root element named correctly - generateDS limitation


class NeuroMLHdf5Writer(object):
    @classmethod
    def write(cls,nml_doc,h5_file_name):
        
        import tables
        
        h5file = tables.openFile(h5_file_name, mode = "w", title = nml_doc.id)
        
        rootGroup = h5file.createGroup("/", 'neuroml', 'Root NeuroML group')
        
        rootGroup._f_setAttr("id", nml_doc.id)
        rootGroup._f_setAttr("notes", nml_doc.notes)
        
        for network in nml_doc.networks:

            network.exportHdf5(h5file, rootGroup)
        
        '''
        projsGroup = h5file.createGroup(rootGroup, 'projections', 'Projections group')
        projsGroup._f_setAttr("units", self.projUnits)
        
        for projection in self.projections:
            projection.generateHDF5(h5file, projsGroup)'''
            
        
        h5file.close()  # Close (and flush) the file
        
        
class JSONWriter(object):
    """
    Write a NeuroMLDocument to JSON, particularly useful
    when dealing with lots of ArrayMorphs.
    """

    
    @classmethod
    def __encode_as_json(cls,neuroml_document):
        neuroml_document = cls.__sanitize_doc(neuroml_document)
        from jsonpickle import encode as json_encode
        encoded = json_encode(neuroml_document)
        return encoded
    
    @classmethod
    def __sanitize_doc(cls,neuroml_document):
        """
        Some operations will need to be performed
        before the document is JSON-pickleable.
        """

        for cell in neuroml_document.cells:
            try:
                cell.morphology.vertices = cell.morphology.vertices.tolist()
                cell.morphology.physical_mask = cell.morphology.physical_mask.tolist()
                cell.morphology.connectivity = cell.morphology.connectivity.tolist()
            except:
                pass

        return neuroml_document

    @classmethod
    def __file_handle(file):
        if isinstance(cls,file,str):
            import tables
            fileh = tables.openFile(filepath, mode = "w")

            
    @classmethod    
    def write(cls,neuroml_document,file):
        if isinstance(file,str):
            fileh = open(file, mode = 'w')
        else:
            fileh = file

        if isinstance(neuroml_document,neuroml.NeuroMLDocument):
            encoded = cls.__encode_as_json(neuroml_document)

        else:
            raise NotImplementedError("Currently you can only serialize NeuroMLDocument type in JSON format")

        fileh.write(encoded)

    @classmethod
    def write_to_mongodb(cls,neuroml_document,db,host=None,port=None,id=None):
        from pymongo import MongoClient
        import json

        if id == None:
            id = neuroml_document.id
        
        if host == None:
            host = 'localhost'
        if port == None:
            port = 27017

        client = MongoClient(host, port)
        db = client[db]
        collection = db[id]

        if isinstance(neuroml_document,neuroml.NeuroMLDocument):
            encoded = cls.__encode_as_json(neuroml_document)

        encoded_dict = json.loads(encoded)
        collection.insert(encoded_dict)

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

        import tables
        fileh = tables.openFile(filepath, mode = "w")
        
        #Now instead we should go through a document/cell/morphology
        #hierarchy - this kind of tree traversal should be done recursively

        if isinstance(data,neuroml.arraymorph.ArrayMorphology):
            cls.__write_single_cell(data, fileh)

        if isinstance(data,neuroml.NeuroMLDocument):
            cls.__write_neuroml_document(data,fileh)
            
        # Finally, close the file (this also will flush all the remaining buffers!)
        fileh.close()
