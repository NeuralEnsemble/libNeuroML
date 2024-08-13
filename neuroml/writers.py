import typing

import neuroml
from neuroml.arraymorph import ArrayMorphology

"""Classes to write NeuroML to various formats."""


class NeuroMLWriter(object):
    """Writes from NeuroMLDocument to nml file.

    In future can implement from other types via chain of responsibility pattern.
    """

    @classmethod
    def write(cls, nmldoc: neuroml.NeuroMLDocument, file: str, close: bool = True):
        """Write a NeuroMLDocument to file.

        :param nmldoc: NeuroML document object to write
        :type nmldoc: neuroml.NeuroMLDocument
        :param file: file name to write to
        :type file: str
        :param close: toggle whether file should be closed
        :type close: bool
        :raises AttributeError: if export fails
        """

        if isinstance(file, str):
            fileh = open(file, "w")
        else:
            fileh = file

        # TODO: this should be extracted from the schema:
        namespacedef = 'xmlns="http://www.neuroml.org/schema/neuroml2" '
        namespacedef += ' xmlns:xs="http://www.w3.org/2001/XMLSchema"'
        namespacedef += ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        namespacedef += (
            ' xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_%s.xsd"'
            % neuroml.current_neuroml_version
        )

        try:
            nmldoc.export(
                fileh, 0, name_="neuroml", namespacedef_=namespacedef
            )  # name_ param to ensure root element named correctly - generateDS limitation
        except AttributeError as ae:
            fileh.close()
            raise (ae)

        if close:
            fileh.close()


class NeuroMLHdf5Writer(object):
    """Exports NeuroML documents to HDF5 format."""

    @classmethod
    def write(
        cls,
        nml_doc: neuroml.NeuroMLDocument,
        h5_file_name: str,
        embed_xml: bool = True,
        compress: bool = True,
    ):
        """Write a NeuroMLDocument to HDF5 file

        :param nmldoc: NeuroML document object to write
        :type nmldoc: neuroml.NeuroMLDocument
        :param h5_file_name: file name to write to
        :type h5_file_name: str
        :param embed_xml: toggle whether XML serialization should be embedded
        :type embed_xml: bool
        :param compress: toggle compression
        :type compress: bool
        """

        import tables

        FILTERS = (
            tables.Filters(complib="zlib", complevel=5)
            if compress
            else tables.Filters()
        )
        h5file = tables.open_file(
            h5_file_name, mode="w", title=nml_doc.id, filters=FILTERS
        )

        rootGroup = h5file.create_group("/", "neuroml", "Root NeuroML group")

        rootGroup._f_setattr("id", nml_doc.id)
        rootGroup._f_setattr("notes", nml_doc.notes)
        rootGroup._f_setattr("GENERATED_BY", "libNeuroML v%s" % (neuroml.__version__))

        for network in nml_doc.networks:
            network.exportHdf5(h5file, rootGroup)

        if embed_xml:
            networks = []
            for n in nml_doc.networks:
                networks.append(n)

            nml_doc.networks = []

            try:
                import StringIO

                sf = StringIO.StringIO()
            except ImportError:
                import io

                sf = io.StringIO()

            NeuroMLWriter.write(nml_doc, sf, close=False)
            nml2 = sf.getvalue()
            rootGroup._f_setattr("neuroml_top_level", nml2)

            # Put back into previous form...
            for n in networks:
                nml_doc.networks.append(n)

        h5file.close()  # Close (and flush) the file

    """
    @classmethod
    def write_xml_and_hdf5(cls,nml_doc0,xml_file_name,h5_file_name):

        nml_doc_hdf5 = neuroml.NeuroMLDocument(nml_doc0.id)

        for n in nml_doc0.networks:
            nml_doc_hdf5.networks.append(n)

        nml_doc0.networks = []

        nml_doc0.includes.append(neuroml.IncludeType(h5_file_name))

        NeuroMLWriter.write(nml_doc0,xml_file_name)

        NeuroMLHdf5Writer.write(nml_doc_hdf5,h5_file_name,embed_xml=False)

        # Put back into previous form...
        for n in nml_doc_hdf5.networks:
            nml_doc0.networks.append(n)
        for inc in nml_doc0.includes:
            if inc.href == h5_file_name:
                nml_doc0.includes.remove(inc)"""


class ArrayMorphWriter(object):
    """
    Write morphology to ArrayMorph format.

    For now just testing a simple method which can write a morphology, not a NeuroMLDocument.
    """

    @classmethod
    def __write_single_cell(
        cls,
        array_morph: ArrayMorphology,
        fileh,
        cell_id: typing.Optional[str] = None,
    ):
        """Write a array morphology to a file handler.

        :param array_morph: a array morph object containing a morphology
        :type array_morph: ArrayMorphology
        :param fileh: pytables file object of file to write to
        :type fileh: pytables file object
        :param cell_id: id of cell
        :type cell_id: str
        """
        vertices = array_morph.vertices
        connectivity = array_morph.connectivity
        physical_mask = array_morph.physical_mask

        # Get the HDF5 root group
        root = fileh.root

        # Create the groups:
        # can use morphology name in future?

        if array_morph.id is None:
            morphology_name = "Morphology"
        else:
            morphology_name = array_morph.id

        if cell_id is None:
            morphology_group = fileh.create_group(root, morphology_name)
            hierarchy_prefix = "/" + morphology_name
        else:
            cell_group = fileh.create_group(root, cell_id)
            morphology_group = fileh.create_group(cell_group, morphology_name)
            hierarchy_prefix = "/" + cell_id + "/" + morphology_name

        vertices_array = fileh.create_array(hierarchy_prefix, "vertices", vertices)
        connectivity_array = fileh.create_array(
            hierarchy_prefix, "connectivity", connectivity
        )
        physical_mask_array = fileh.create_array(
            hierarchy_prefix, "physical_mask", physical_mask
        )

    @classmethod
    def __write_neuroml_document(cls, document: neuroml.NeuroMLDocument, fileh):
        """Write a NeuroMLDocument containing morphology to a file handler

        :param document: a NeuroML document object containing a morphology
        :type document: neuroml.NeuroMLDocument
        :param fileh: file handler of file to write to
        :type fileh: file object
        """
        for default_id, cell in enumerate(document.cells):
            morphology = cell.morphology

            if morphology.id is None:
                morphology.id = "Morphology" + str(default_id)
            if cell.id is None:
                cell.id = "Cell" + str(default_id)

            cls.__write_single_cell(morphology, fileh, cell_id=cell.id)

        for default_id, morphology in enumerate(document.morphology):
            if morphology.id is None:
                morphology.id = "Morphology" + str(default_id)

            cls.__write_single_cell(morphology, fileh, cell_id=cell.id)

    @classmethod
    def write(
        cls,
        data: typing.Union[neuroml.NeuroMLDocument, ArrayMorphology],
        filepath: str,
    ):
        """Write morphology to file in ArrayMorph format.

        :param data: data to write
        :type data: ArrayMorphology or neuroml.NeuroMLDocument
        :param filepath: path of file to write to
        :type filepath: str

        """
        import tables

        fileh = tables.open_file(filepath, mode="w")

        # Now instead we should go through a document/cell/morphology
        # hierarchy - this kind of tree traversal should be done recursively

        if isinstance(data, ArrayMorphology):
            cls.__write_single_cell(data, fileh)

        if isinstance(data, neuroml.NeuroMLDocument):
            cls.__write_neuroml_document(data, fileh)

        # Finally, close the file (this also will flush all the remaining buffers!)
        fileh.close()
