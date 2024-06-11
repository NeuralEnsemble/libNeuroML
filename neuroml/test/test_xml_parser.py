"""
Unit tests for loaders

"""

import os

import pytest

import neuroml.writers as writers
from neuroml import loaders
from neuroml.hdf5.DefaultNetworkHandler import DefaultNetworkHandler
from neuroml.hdf5.NetworkBuilder import NetworkBuilder
from neuroml.hdf5.NeuroMLXMLParser import NeuroMLXMLParser


@pytest.mark.parametrize(
    "f",
    [
        "simplenet.nml",
        "testh5.nml",
        "pyr_4_sym.cell.nml",
        "MediumNet.net.nml",
        "complete.nml",
    ],
)
class TestNeuroMLXMLParser:
    def test_parse(self, f):
        base_dir = os.path.dirname(__file__)
        file_name = base_dir + "/../examples/test_files/" + f
        print("---- Testing {}".format(file_name))

        nml_doc0 = loaders.read_neuroml2_file(
            file_name, include_includes=True, verbose=True
        )

        summary0 = nml_doc0.summary(show_includes=False, show_non_network=False)
        # print("\n" + summary0)

        nmlHandler = DefaultNetworkHandler()
        currParser = NeuroMLXMLParser(nmlHandler)
        currParser.parse(file_name)

        print("-------------------------------\n\n")

        nmlHandler_new = NetworkBuilder()
        currParser_new = NeuroMLXMLParser(nmlHandler_new)
        currParser_new.parse(file_name)
        nml_doc_new = nmlHandler_new.get_nml_doc()

        summary = nml_doc_new.summary(show_includes=False, show_non_network=False)
        # print(summary)

        compare(summary, summary0)

        nml_file_new = base_dir + "/../examples/tmp/EXP_" + f

        writers.NeuroMLWriter.write(nml_doc_new, nml_file_new)
        print("Written network file to: " + nml_file_new)


def compare(s1, s2):
    if s1 == s2:
        print("Same!")
        return

    l1 = s1.split("\n")
    l2 = s2.split("\n")

    for i in range(min(len(l1), len(l2))):
        if not l1[i] == l2[i]:
            print("Mismatch at line %i:\n>>>  %s\n<<<  %s" % (i, l1[i], l2[i]))
    if len(l1) != len(l2):
        print("Different number of lines!")

    assert s1 == s2


if __name__ == "__main__":
    tnxp = TestNeuroMLXMLParser()
    tnxp.test_parse()
