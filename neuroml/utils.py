"""

Utilities for checking generated code

"""

import inspect
import os
import sys
import warnings
from typing import Any, Dict, Optional, Type, Union

import networkx

import neuroml.nml.nml as schema
from neuroml import NeuroMLDocument

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


def print_hierarchy(tree, indent=4, current_ind=0):
    """Print the hierarchy tree generated by get_class_hierarchy

    Reference: https://stackoverflow.com/a/75161393/375067
    """
    for k, v in tree.items():
        if current_ind:
            before_dashes = current_ind - indent
            print(" " * before_dashes + "└" + "-" * (indent - 1) + k)
        else:
            print(k)
        for sub_tree in v:
            print_hierarchy(sub_tree, indent=indent, current_ind=current_ind + indent)


def get_hier_graph_networkx(graph: networkx.DiGraph, hier: Dict[str, Any]):
    """Get a networkx graph of the NeuroML hierarchy

    :param graph: graph object to populate
    :param hier: component type hierarchy obtained from `get_class_hierarchy`
        and `get_nml2_class_hierarchy` methods
    :returns: None

    """
    for k, vs in hier.items():
        for v in vs:
            if type(v) is dict:
                graph.add_edge(k, list(v.keys())[0])
                get_hier_graph_networkx(graph, v)
            else:
                graph.add_edge(k, v)


def get_relative_component_path(
    src: str,
    dest: str,
    root: Type = schema.NeuroMLDocument,
    graph: Optional[networkx.DiGraph] = None,
):
    """Construct a path from src component to dest in a neuroml document.

    Useful when referring to components in other components
    Note that

    :param src: source component
    :param dest: destination component
    :param root: root component of the hierarchy
    :param graph: a networkx digraph of the NeuroML hierarchy if available
        if not, one is constructed
    :returns: calculated path and networkx digraph for future use
    """
    if graph is None:
        graph = networkx.DiGraph()
        get_hier_graph_networkx(graph, root.get_nml2_class_hierarchy())

    p1 = list(networkx.all_shortest_paths(graph, root.__name__, "Instance"))
    p2 = list(networkx.all_shortest_paths(graph, root.__name__, "Input"))

    if len(p1) > 1 or len(p2) > 1:
        print("Multiple paths found, cannot calculate recommended path")
        print("Paths are:")
        for p in p1 + p2:
            print("/".join(p1[0]))
    else:
        p1s = "/".join(p1[0])
        p2s = "/".join(p2[0])
        print(f"Path1: {p1s}")
        print(f"Path2: {p2s}")
        # remove one "../" because we do not need to get to the common level
        # here, unlike actual file system path traversal
        path = os.path.relpath(p1s, p2s).replace("../", "", 1)
        print("Relative path: " + path)

    return (path, graph)


def fix_external_morphs_biophys_in_cell(nml2_doc: NeuroMLDocument) -> None:
    """
    Only used in the case where a cell element has a morphology (or biophysicalProperties) attribute, as opposed to a
    subelement morphology/biophysicalProperties. This will substitute the external element into the cell element for ease of access
    """
    for cell in nml2_doc.cells:
        if cell.morphology_attr != None:
            ext_morph = nml2_doc.get_by_id(cell.morphology_attr)
            cell.morphology = ext_morph
        if cell.biophysical_properties_attr != None:
            ext_bp = nml2_doc.get_by_id(cell.biophysical_properties_attr)
            cell.biophysical_properties = ext_bp


def main():
    if len(sys.argv) != 2:
        print("Please specify the name of the NeuroML2 file...")
        exit(1)

    print_summary(sys.argv[1])


if __name__ == "__main__":
    main()
