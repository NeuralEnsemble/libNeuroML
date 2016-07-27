"""
Unit tests for loaders

"""

from neuroml.hdf5.NetworkBuilder import NetworkBuilder
from neuroml.hdf5.NeuroMLXMLParser import NeuroMLXMLParser

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLXMLParser(unittest.TestCase):
    def test_parse(self):
        

        file_name = os.path.dirname(__file__)+'/../examples/test_files/testh5.nml'

        from neuroml.hdf5.DefaultNetworkHandler import DefaultNetworkHandler

        nmlHandler = DefaultNetworkHandler()     

        currParser = NeuroMLXMLParser(nmlHandler) # The HDF5 handler knows of the structure of NetworkML and calls appropriate functions in NetworkHandler

        currParser.parse(file_name)

        print('-------------------------------\n\n')


        nmlHandler = NetworkBuilder()   

        currParser = NeuroMLXMLParser(nmlHandler) 

        currParser.parse(file_name)

        nml_doc = nmlHandler.get_nml_doc()
        
        summary = nml_doc.summary()
        
        print(summary)
        
        comp = nml_doc.get_by_id("IafNet")
        print(comp)
        comp = nml_doc.get_by_id("IafNet2")

        nml_file = os.path.dirname(__file__)+'/../examples/tmp/testh5_2_.nml'
        import neuroml.writers as writers
        writers.NeuroMLWriter.write(nml_doc, nml_file)
        print("Written network file to: "+nml_file)
