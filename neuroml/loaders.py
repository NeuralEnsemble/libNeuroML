import os
import sys
import warnings
from typing import Callable, Optional

import neuroml
import neuroml.utils as utils
from neuroml import NeuroMLDocument
from neuroml.nml.nml import parse as nmlparse
from neuroml.nml.nml import parseString as nmlparsestring

supressGeneratedsWarnings = True


class NeuroMLLoader(object):
    """Class for loading NeuroML."""

    @classmethod
    def load(cls, src: str) -> neuroml.NeuroMLDocument:
        """Load a NeuroML file.

        :param src: file
        :type src: str
        :returns: NeuroMLDocument object
        :rtype: neuroml.NeuromlDocument
        :raises TypeError: if the file is not a valid NeuroML document
        """
        doc = cls.__nml2_doc(src)
        if isinstance(doc, NeuroMLDocument):
            return doc
        else:
            raise TypeError(
                "{} does not appear to be a NeuroML Document. NeuroML documents must be contained in a <neuroml> tag.".format(
                    src
                )
            )

    @classmethod
    def __nml2_doc(cls, file_name: str) -> neuroml.NeuroMLDocument:
        """Load and parse a NeuroML file.

        :param file_name: the file
        :type file_name: str
        :returns: NeuroMLDocument object
        :rtype: neuroml.NeuromlDocument
        :raises Exception: if the document is not a valid NeuroML Document
        """
        try:
            if supressGeneratedsWarnings:
                warnings.simplefilter("ignore")
            nml2_doc = nmlparse(file_name, silence=True)
            if supressGeneratedsWarnings:
                warnings.resetwarnings()
        except Exception as e:
            raise Exception("Not a valid NeuroML 2 doc (%s): %s" % (file_name, e), e)

        return nml2_doc


class NeuroMLHdf5Loader(object):
    """Class for loading a NeuroML HDF5 file."""

    @classmethod
    def load(cls, src: str, optimized: bool = False) -> neuroml.NeuroMLDocument:
        """Load a NeuroML HDF5 file.

        :param src: file
        :type src: str
        :param optimized: load optimized numpy representation
            In the optimized representation, instead of the complete Python
            object tree being constructed, the various tables in the HDF5 file
            are loaded as numpy arrays. This is transparent to the user, who
            can continue using the standard methods to access the data.
        :type optimized: bool
        :returns: NeuroMLDocument object
        :rtype: neuroml.NeuromlDocument
        """
        doc = cls.__nml2_doc(src, optimized)
        return doc

    @classmethod
    def __nml2_doc(
        cls, file_name: str, optimized: bool = False
    ) -> neuroml.NeuroMLDocument:
        """Load and parse a NeuroML HDF5 file.

        :param file_name: the file
        :type file_name: str
        :param optimized: load optimized numpy representation
            In the optimized representation, instead of the complete Python
            object tree being constructed, the various tables in the HDF5 file
            are loaded as numpy arrays. This is transparent to the user, who
            can continue using the standard methods to access the data.
        :type optimized: bool
        :returns: NeuroMLDocument object
        :rtype: neuroml.NeuromlDocument
        """
        import logging

        logging.basicConfig(
            level=logging.INFO, format="%(name)-19s %(levelname)-5s - %(message)s"
        )

        from neuroml.hdf5.NeuroMLHdf5Parser import NeuroMLHdf5Parser

        if optimized:
            currParser = NeuroMLHdf5Parser(None, optimized=True)

            currParser.parse(file_name)

            return currParser.get_nml_doc()
        else:
            from neuroml.hdf5.NetworkBuilder import NetworkBuilder

            nmlHandler = NetworkBuilder()

            currParser = NeuroMLHdf5Parser(nmlHandler)

            currParser.parse(file_name)

            nml2_doc = nmlHandler.get_nml_doc()
            if currParser.nml_doc_extra_elements:
                utils.add_all_to_document(currParser.nml_doc_extra_elements, nml2_doc)

            return nml2_doc


class SWCLoader(object):
    """
    This class is deprecated and will be removed in a future release. Please
    refer to https://docs.neuroml.org/Userdocs/ImportingMorphologyFiles.html
    for information on importing/converting morphology files to NeuroML2.
    """

    @classmethod
    def load_swc_single(cls, src, name=None):
        warnings.warn(
            "This method/class is deprecated and will be removed in a future release. Please see https://docs.neuroml.org/Userdocs/ImportingMorphologyFiles.html",
            FutureWarning,
            stacklevel=2,
        )

        import numpy as np

        from neuroml import arraymorph

        dtype = {
            "names": ("id", "type", "x", "y", "z", "r", "pid"),
            "formats": ("int32", "int32", "f4", "f4", "f4", "f4", "int32"),
        }

        d = np.loadtxt(src, dtype=dtype)

        if len(np.nonzero(d["pid"] == -1)) != 1:
            assert False, "Unexpected number of id's of -1 in file"

        num_nodes = len(d["pid"])

        root_index = np.where(d["pid"] == -1)[0][0]

        # We might not nessesarily have continuous indices in the
        # SWC file, so lets convert them:
        index_to_id = d["id"]
        id_to_index_dict = dict([(id, index) for index, id in enumerate(index_to_id)])

        if len(id_to_index_dict) != len(index_to_id):
            s = "Internal Error Loading SWC: Index and ID map are different lengths."
            s += " [ID:%d, Index:%d]" % (len(index_to_id), len(id_to_index_dict))
            # TODO: this is undefined!!
            raise MorphologyImportError(s)  # noqa: F821

        # Vertices and section types are easy:
        vertices = d[["x", "y", "z", "r"]]
        vertices = np.vstack([d["x"], d["y"], d["z"], d["r"]]).T
        section_types = [swctype for ID, swctype in d[["id", "type"]]]

        # for connection indices we want the root to have index -1:
        connection_indices = np.zeros(num_nodes, dtype="int32")
        for i in range(num_nodes):
            pID = d["pid"][i]
            if pID != -1:
                parent_index = id_to_index_dict[pID]
                connection_indices[i] = parent_index
            else:
                connection_indices[i] = -1

        # This needs to become an "Optimized Morphology" of some kind
        return arraymorph.ArrayMorphology(
            vertices=vertices,
            connectivity=connection_indices,
            node_types=section_types,
            name=name,
        )


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

        with tables.open_file(filepath, mode="r") as file:
            document = neuroml.NeuroMLDocument()

            for node in file.root:
                if hasattr(node, "vertices"):
                    loaded_morphology = cls.__extract_morphology(node)
                    document.morphology.append(loaded_morphology)
                else:
                    for morphology in node:
                        loaded_morphology = cls.__extract_morphology(morphology)
                        document.morphology.append(loaded_morphology)

        return document


def read_neuroml2_file(
    nml2_file_name: str,
    include_includes: bool = False,
    verbose: bool = False,
    already_included: list = None,
    print_method: Callable = neuroml.print_,
    optimized: bool = False,
) -> NeuroMLDocument:
    """
    Read a NeuroML2 file into a NeuroMLDocument object

    :param nml2_file_name: name of NeuroML file to read
    :type nml2_file_name: str
    :param include_includes: toggle whether Included files should also be loaded
    :type include_includes: bool
    :param verbose: toggle verbose output
    :type verbose: bool
    :param already_included: list of already included files
    :type already_included: list
    :param print_method: print function to use
    :type print_method: Callable
    :param optimized: for optimized HDF5 NeuroML files
    :type optimized: bool
    :returns: NeuroMLDoc object containing the read file

    """
    if already_included is None:
        already_included = []

    print_method("Loading NeuroML2 file: %s" % nml2_file_name, verbose)

    if not os.path.isfile(nml2_file_name):
        print_method("Unable to find file: %s!" % nml2_file_name, True)
        sys.exit()

    return _read_neuroml2(
        nml2_file_name,
        include_includes=include_includes,
        verbose=verbose,
        already_included=already_included,
        print_method=print_method,
        optimized=optimized,
    )


def read_neuroml2_string(
    nml2_string: str,
    include_includes: bool = False,
    verbose: bool = False,
    already_included: list = [],
    print_method: Callable = neuroml.print_,
    optimized: bool = False,
    base_path: Optional[str] = None,
) -> NeuroMLDocument:
    """
    Read a NeuroML2 string into a NeuroMLDocument object

    :param nml2_string: NeuroML string to load
    :type nml2_string: str
    :param include_includes: toggle whether Included files should also be loaded
    :type include_includes: bool
    :param verbose: toggle verbose output
    :type verbose: bool
    :param already_included: list of already included files
    :type already_included: list
    :param print_method: print function to use
    :type print_method: Callable
    :param optimized: for optimized HDF5 NeuroML files
    :type optimized: bool
    :param base_path:
    :type base_path: str
    :returns: NeuroMLDoc object containing the model

    """

    print_method("Loading NeuroML2 string, base_path: %s" % base_path, verbose)

    return _read_neuroml2(
        nml2_string,
        include_includes=include_includes,
        verbose=verbose,
        already_included=already_included,
        print_method=print_method,
        optimized=optimized,
        base_path=base_path,
    )


def _read_neuroml2(
    nml2_file_name_or_string: str,
    include_includes: bool = False,
    verbose: bool = False,
    already_included: list = [],
    print_method: Callable = neuroml.print_,
    optimized: bool = False,
    base_path: Optional[str] = None,
) -> NeuroMLDocument:
    """
    Read a NeuroML2 file or string into a NeuroMLDocument object.

    Internal method, please use `read_neuroml2_file` or `read_neuroml2_string`
    instead.

    :param nml2_file_name_or_string: NeuroML file or string to load
    :type nml2_file_name_or_string: str
    :param include_includes: toggle whether Included files should also be loaded
    :type include_includes: bool
    :param verbose: toggle verbose output
    :type verbose: bool
    :param already_included: list of already included files
    :type already_included: list
    :param print_method: print function to use
    :type print_method: Callable
    :param optimized: for optimized HDF5 NeuroML files
    :type optimized: bool
    :param base_path:
    :type base_path: str
    :returns: NeuroMLDoc object containing the model

    """

    # print("................ Loading: %s"%nml2_file_name_or_string[:7])

    base_path_to_use = (
        os.path.dirname(os.path.realpath(nml2_file_name_or_string))
        if base_path is None
        else base_path
    )

    if supressGeneratedsWarnings:
        warnings.simplefilter("ignore")

    if not isinstance(
        nml2_file_name_or_string, str
    ) or nml2_file_name_or_string.startswith("<"):
        nml2_doc = nmlparsestring(nml2_file_name_or_string)
        base_path_to_use = "./" if base_path is None else base_path
    elif nml2_file_name_or_string.endswith(".h5") or nml2_file_name_or_string.endswith(
        ".hdf5"
    ):
        nml2_doc = NeuroMLHdf5Loader.load(nml2_file_name_or_string, optimized=optimized)
    else:
        nml2_doc = NeuroMLLoader.load(nml2_file_name_or_string)

    if supressGeneratedsWarnings:
        warnings.resetwarnings()

    if include_includes:
        print_method(
            "Including the included files (included already: %s)" % already_included,
            verbose,
        )

        for include in nml2_doc.includes:
            # if given path exists, use it, otherwise assume its relative to
            # current directory and try that
            if os.path.exists(include.href):
                incl_loc = os.path.abspath(include.href)
            else:
                incl_loc = os.path.abspath(os.path.join(base_path_to_use, include.href))
            if incl_loc not in already_included:
                print_method(
                    "Loading included NeuroML2 file: %s (base: %s, resolved: %s)"
                    % (include.href, base_path_to_use, incl_loc),
                    verbose,
                )

                if incl_loc.endswith(".nml") or incl_loc.endswith(".xml"):
                    nml2_sub_doc = read_neuroml2_file(
                        incl_loc,
                        True,
                        verbose=verbose,
                        already_included=already_included,
                    )
                    already_included.append(incl_loc)
                    utils.add_all_to_document(nml2_sub_doc, nml2_doc)

                elif incl_loc.endswith(".nml.h5"):
                    nml2_sub_doc = NeuroMLHdf5Loader.load(incl_loc)
                    already_included.append(incl_loc)
                    utils.add_all_to_document(nml2_sub_doc, nml2_doc)

                else:
                    raise Exception("Unrecognised extension on file: %s" % incl_loc)

        nml2_doc.includes = []

    else:
        if len(nml2_doc.includes) > 0:
            print_method(
                "NOT processing included files, even though %s are included!"
                % len(nml2_doc.includes),
                verbose,
            )

    return nml2_doc


if __name__ == "__main__":
    f = sys.argv[1]
    nml_doc = read_neuroml2_file(f)
    print("Read in %s" % f)
    print(nml_doc.summary())
