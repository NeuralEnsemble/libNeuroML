from neuroml.nml.nml import parse as nmlparse

from neuroml.nml.nml import parseString as nmlparsestring

import neuroml
import neuroml.utils as utils

import os
import sys
import warnings

from typing import Callable, Optional

supressGeneratedsWarnings = True


def print_(text, verbose=True):
    if verbose:
        prefix = "libNeuroML >>> "
        # if not isinstance(text, str): text = text.decode('ascii')
        if verbose:

            print("%s%s" % (prefix, text.replace("\n", "\n" + prefix)))


class NeuroMLLoader(object):
    @classmethod
    def load(cls, src):
        doc = cls.__nml2_doc(src)
        if isinstance(doc, neuroml.nml.nml.NeuroMLDocument):
            return doc
        else:
            raise TypeError(
                "{} does not appear to be a NeuroML Document. NeuroML documents must be contained in a <neuroml> tag.".format(
                    src
                )
            )

    @classmethod
    def __nml2_doc(cls, file_name):
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
    @classmethod
    def load(cls, src, optimized=False):
        doc = cls.__nml2_doc(src, optimized)
        return doc

    @classmethod
    def __nml2_doc(cls, file_name, optimized=False):
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
    print_method: Callable = print_,
    optimized: bool = False,
) -> neuroml.nml.nml.NeuroMLDocument:
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
    :param optimised: for optimised HDF5 NeuroML files
    :type optimised: bool
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
    print_method: Callable = print_,
    optimized: bool = False,
    base_path: Optional[str] = None,
) -> neuroml.nml.nml.NeuroMLDocument:
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
    :param optimised: for optimised HDF5 NeuroML files
    :type optimised: bool
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
    print_method: Callable = print_,
    optimized: bool = False,
    base_path: Optional[str] = None,
) -> neuroml.nml.nml.NeuroMLDocument:
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
    :param optimised: for optimised HDF5 NeuroML files
    :type optimised: bool
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
                "NOT including included files, even though %s are included!"
                % len(nml2_doc.includes),
                verbose,
            )

        nml2_doc.includes = []

    return nml2_doc


if __name__ == "__main__":
    f = sys.argv[1]
    nml_doc = read_neuroml2_file(f)
    print("Read in %s" % f)
    print(nml_doc.summary())
