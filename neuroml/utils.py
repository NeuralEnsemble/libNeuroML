"""

Utilities for checking generated code

"""
import os.path
import sys
import inspect
import warnings
from typing import Union, Any

from .__version__ import current_neuroml_version
import neuroml.nml.nml as schema

neuro_lex_ids = {
    "axon": "GO:0030424",
    "dend": "GO:0030425",
    "soma": "GO:0043025",
}


def validate_neuroml2(file_name: str) -> None:
    """Validate a NeuroML document against the NeuroML schema specification.

    :param file_name: name of NeuroML file to validate.
    :type file_name: str
    """
    from lxml import etree

    xsd_file = os.path.join(
        os.path.dirname(__file__),
        "nml/NeuroML_%s.xsd" % current_neuroml_version,
    )

    with open(xsd_file) as schema_file:
        xmlschema = etree.XMLSchema(etree.parse(schema_file))
        print("Validating %s against %s" % (file_name, xsd_file))
        if not xmlschema.validate(etree.parse(file_name)):
            xmlschema.assertValid(
                etree.parse(file_name)
            )  # print reason if file is invalid
            return
        print("It's valid!")


def is_valid_neuroml2(file_name: str) -> None:
    """Check if a file is valid NeuroML2.

    :param file_name: name of NeuroML file to check
    :type file_name: str
    :returns: True if file is valid, False if not.
    :rtype: Boolean
    """
    from lxml import etree

    xsd_file = os.path.join(
        os.path.dirname(__file__),
        "nml/NeuroML_%s.xsd" % current_neuroml_version,
    )

    with open(xsd_file) as schema_file:
        xmlschema = etree.XMLSchema(etree.parse(schema_file))
        return xmlschema.validate(etree.parse(file_name))
    return False


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


def component_factory(component_type: Union[str, type], validate: bool = True, **kwargs: Any) -> Any:
    """Factory function to create a NeuroML Component object.

    Wrapper around the component_factory method that is present in each NeuroML
    component type class.

    Please see `GeneratedsSuperSuper.component_factory` for more information.
    """
    # for a cell, call create_cell
    if component_type == schema.Cell or component_type == "Cell":
        return create_cell(**kwargs)

    # for everything else, create a new "vanilla" component
    return schema.NeuroMLDocument().component_factory(component_type, validate,
                                                      **kwargs)


def create_cell(cell_id: str, use_convention: bool = True) -> schema.Cell:
    """Create a NeuroML Cell.

    Initialises the cell with these properties assigning IDs where applicable:

    - Morphology: "morphology"
    - BiophysicalProperties: "biophys"
    - MembraneProperties
    - IntracellularProperties

    if `use_convention` is True, it also creates some default SegmentGroups for
    convenience:

    - "all", "soma_group", "dendrite_group", "axon_group" which
      are used by other helper functions to include all, soma, dendrite, and
      axon segments respectively.

    Note that since this cell does not currently include a segment in its
    morphology, it is *not* a valid NeuroML construct. Use the `add_segment`
    function to add segments. `add_segment` will also populate the default
    segment groups this creates.

    :param cell_id: id of the cell
    :type cell_id: str
    :param use_convention: whether helper segment groups should be created using the default convention
    :type use_convention: bool
    :returns: created cell object of type neuroml.Cell

    """
    # Do not use component_factory here because component_factory uses
    # create_cell
    cell = schema.Cell(id=cell_id)
    # do not validate yet, because segments are required
    cell.add("Morphology", id="morphology", validate=False)

    membrane_properties = component_factory("MembraneProperties")
    intracellular_properties = component_factory("IntracellularProperties")

    cell.biophysical_properties = component_factory(
        "BiophysicalProperties",
        id="biophys",
        intracellular_properties=intracellular_properties,
        membrane_properties=membrane_properties,
    )

    if use_convention:
        seg_group_all = component_factory("SegmentGroup", id="all")
        seg_group_soma = component_factory(
            "SegmentGroup",
            id="soma_group",
            neuro_lex_id=neuro_lex_ids["soma"],
            notes="Default soma segment group for the cell",
        )
        seg_group_axon = component_factory(
            "SegmentGroup",
            id="axon_group",
            neuro_lex_id=neuro_lex_ids["axon"],
            notes="Default axon segment group for the cell",
        )
        seg_group_dend = component_factory(
            "SegmentGroup",
            id="dendrite_group",
            neuro_lex_id=neuro_lex_ids["dend"],
            notes="Default dendrite segment group for the cell",
        )
        # skip validation: segments etc needed, cell is invalid
        cell.morphology.add(seg_group_all, validate=False)
        cell.morphology.add(seg_group_soma, validate=False)
        cell.morphology.add(seg_group_axon, validate=False)
        cell.morphology.add(seg_group_dend, validate=False)

    return cell


def main():
    if len(sys.argv) != 2:
        print("Please specify the name of the NeuroML2 file...")
        exit(1)

    print_summary(sys.argv[1])


if __name__ == "__main__":
    main()
