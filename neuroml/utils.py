"""

Utilities for checking generated code

"""
import inspect
import sys
import warnings
from typing import Any, List, Optional, Union

import neuroml.nml.nml as schema

from . import loaders


def validate_neuroml2(file_name: str) -> None:
    """Validate a NeuroML document against the NeuroML schema specification.

    :param file_name: name of NeuroML file to validate.
    :type file_name: str
    :raises ValueError: if document is invalid
    """
    nml_doc = loaders.read_neuroml2_file(
        file_name, include_includes=True, verbose=False, optimized=True
    )
    nml_doc.validate(recursive=True)
    print("It's valid!")


def is_valid_neuroml2(file_name: str) -> None:
    """Check if a file is valid NeuroML2.

    :param file_name: name of NeuroML file to check
    :type file_name: str
    :returns: True if file is valid, False if not.
    :rtype: Boolean
    """
    nml_doc = loaders.read_neuroml2_file(
        file_name, include_includes=True, verbose=False, optimized=True
    )
    try:
        nml_doc.validate(recursive=True)
    except ValueError:
        return False
    return True


def print_summary(nml_file_name: str) -> None:
    """Print a summary of the NeuroML model in the given file.

    :param nml_file_name: name of NeuroML file to print summary of
    :type nml_file_name: str
    """
    print(get_summary(nml_file_name))


def get_summary(nml_file_name: str) -> str:
    """Get a summary of the given NeuroML file.

    :param nml_file_name: name of NeuroML file to get summary of
    :type nml_file_name: str
    :returns: summary of provided file
    :rtype: str
    """
    from neuroml.loaders import read_neuroml2_file

    nml_doc = read_neuroml2_file(
        nml_file_name, include_includes=True, verbose=False, optimized=True
    )

    return nml_doc.summary(show_includes=False)


def add_all_to_document(
    nml_doc_src: schema.NeuroMLDocument,
    nml_doc_tgt: schema.NeuroMLDocument,
    verbose: bool = False,
) -> None:
    """Add all members of the source NeuroML document to the target NeuroML document.

    :param nml_doc_src: source NeuroML document to copy from
    :type nml_doc_src: NeuroMLDocument
    :param nml_doc_tgt: target NeuroML document to copy to
    :type nml_doc_tgt: NeuroMLDocument
    :param verbose: control verbosity of working
    :type verbose: bool

    :raises Exception: if a member could not be copied.
    """
    membs = inspect.getmembers(nml_doc_src)

    for memb in membs:
        if isinstance(memb[1], list) and len(memb[1]) > 0 and not memb[0].endswith("_"):
            for entry in memb[1]:
                if memb[0] != "includes":
                    added = False
                    for c in getattr(nml_doc_tgt, memb[0]):
                        if hasattr(c, "id") and c.id == entry.id:
                            added = True
                    if not added:
                        # print("  Adding %s to list: %s" \
                        #    %(entry.id if hasattr(entry,'id') else entry.name, memb[0]))
                        getattr(nml_doc_tgt, memb[0]).append(entry)
                        added = True

                    if not added:
                        raise Exception(
                            "Could not add %s from %s to %s"
                            % (entry, nml_doc_src, nml_doc_tgt)
                        )


def append_to_element(parent, child):
    """Append a child element to a parent Component

    :param parent: parent NeuroML component to add element to
    :type parent: Object
    :param child: child NeuroML component to be added to parent
    :type child: Object
    :raises Exception: when the child could not be added to the parent
    """
    warnings.warn(
        "This method is deprecated and will be removed in future releases. Please use the `add` methods provided in each NeuroML ComponentType object",
        FutureWarning,
        stacklevel=2,
    )
    membs = inspect.getmembers(parent)
    # print("Adding %s to element %s"%(child, parent))
    mappings = {}
    for mdi in parent.member_data_items_:
        mappings[mdi.data_type] = mdi.name
    added = False
    for memb in membs:
        if isinstance(memb[1], list) and not memb[0].endswith("_"):
            # print("Adding %s to %s in %s?"%(child.__class__.__name__, memb[0], parent.__class__.__name__))
            if mappings[child.__class__.__name__] == memb[0]:
                for c in getattr(parent, memb[0]):
                    if c.id == child.id:
                        added = True
                if not added:
                    getattr(parent, memb[0]).append(child)
                    # print("Adding %s to %s in %s?"%(child.__class__.__name__, memb[0], parent.__class__.__name__))
                    added = True

    if not added:
        raise Exception("Could not add %s to %s" % (child, parent))


def has_segment_fraction_info(connections: list) -> bool:
    """Check if connections include fraction information

    :param connections: list of connection objects
    :type connections: list
    :returns: True if connections include fragment information, otherwise False
    :rtype: Boolean
    """
    if not connections:
        return False
    no_seg_fract_info = True
    i = 0
    while no_seg_fract_info and i < len(connections):
        conn = connections[i]
        no_seg_fract_info = (
            conn.pre_segment_id == 0
            and conn.post_segment_id == 0
            and conn.pre_fraction_along == 0.5
            and conn.post_fraction_along == 0.5
        )
        i += 1
    # print("Checked connections: [%s,...], no_seg_fract_info: %s"%(connections[0],no_seg_fract_info))
    return not no_seg_fract_info


def ctinfo(component_type):
    """Provide information on any neuroml Component Type class.

    This creates a new object (component) of the component type and call its
    info() method.

    :param component_type: component type to print information for, either a
        string (the name) or the class itself
    :type component_type: str or type
    :returns: informatin string
    :rtype: str

    """
    if isinstance(component_type, str):
        comp_type_class = getattr(schema, component_type)
    else:
        comp_type_class = getattr(schema, component_type.__name__)

    return comp_type_class().info()


def ctparentinfo(component_type):
    """Provide information on the parentage of any NeuroML Component Type
    class.

    This creates a new object (component) of the component type and call its
    parentinfo() method.

    :param component_type: component type to print information for, either a
        string (the name) or the class itself
    :type component_type: str or type
    :returns: information string
    :rtype: str
    """
    if isinstance(component_type, str):
        comp_type_class = getattr(schema, component_type)
    else:
        comp_type_class = getattr(schema, component_type.__name__)

    return comp_type_class().parentinfo()


def component_factory(
    component_type: Union[str, type], validate: bool = True, **kwargs: Any
) -> Any:
    """Factory function to create a NeuroML Component object.

    Wrapper around the component_factory method that is present in each NeuroML
    component type class.

    Please see `GeneratedsSuperSuper.component_factory` for more information.
    """
    new_obj = schema.NeuroMLDocument().component_factory(
        component_type, validate, **kwargs
    )
    return new_obj


def create_annotation(id_: str,
                      reference_publication: Optional[str] = None,
                      reference_publication_doi: Optional[str] = None,
                      biological_entity: Optional[str] = None,
                      biological_entity_identifiers: Optional[List[str]] = None,
                      biological_entities_is_part_of: Optional[List[str]] = None,
                      model_doi: Optional[str] = None,
                      modeldb_id: Optional[str] = None,
                      model_is_derived_from: Optional[str] = None,
                      ):
    """Utility for creating an RDF Annotation.

    This will create a new annotation that can be added to a NeuroML object
    that supports Annotations.

    To find suitable identifiers for entities, please see the various
    registries listed on https://registry.identifiers.org/registry

    Some common registries are:

    - Gene Ontology: https://geneontology.org/
    - InterLex (formerly Neurolex): https://scicrunch.org/scicrunch/interlex/dashboard
    - NeuroMorpho: https://neuromorpho.org/
    - NeuronDB: https://senselab.med.yale.edu/NeuronDB/
    - ModelDB: https://modeldb.science/
    - BioModels: https://www.ebi.ac.uk/biomodels/

    This does not implement the complete set of RDF qualifiers described in the
    COMBINE specifications:

    - http://biomodels.net/biology-qualifiers/ and
    - http://biomodels.net/model-qualifiers/ for the current specification.

    An example is here:
    https://github.com/combine-org/Annotations/blob/master/nonstandardized/NeuroML/NML2_FullCell.xml

    :param id_: id of component being described
    :param reference_publication: citation/reference of the manuscript related
        to the model element
    :param reference_publication_doi: DOI of the manuscript
    :param biological_entity: biological entity that the component models
    :param biological_entity_identifiers: identifier(s) of biological entity that
        component models
    :param biological_entites_is_part_of: identifier(s) of biological entities
        that the component is part of
    :param model_doi: DOI of model
    :param modeldb_id: ID of model on ModelDB
    :param model_is_derived_from: DOI of a model that this one may be derived
        from/a modification of
    :returns: created annotation

    """
    annotation = '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'

    '""
    if reference_publication is not None or reference_publication_doi is not None:
        if reference_publication is not None:
            ref_pub = rdflib.Bag(graph, rdflib.BNode, (rdflib.URIRef("")))
    """

    return graph.serialize(format="xml")

    # graph.add((rdflib.Literal("NaConductance"), ))


def main():
    if len(sys.argv) != 2:
        print("Please specify the name of the NeuroML2 file...")
        exit(1)

    print_summary(sys.argv[1])


if __name__ == "__main__":
    main()
