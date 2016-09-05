"""
Unit tests for loaders

"""

from neuroml.hdf5.NetworkBuilder import NetworkBuilder
from neuroml.hdf5.NeuroMLXMLParser import NeuroMLXMLParser
from neuroml import loaders

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLXMLParser(unittest.TestCase):
    def test_parse(self):
        

        file_name = os.path.dirname(__file__)+'/../examples/test_files/testh5.nml'
        
        nml_doc0 = loaders.NeuroMLLoader.load(file_name)
        summary0 = nml_doc0.summary()
        print('\n'+summary0)

        from neuroml.hdf5.DefaultNetworkHandler import DefaultNetworkHandler

        nmlHandler = DefaultNetworkHandler()     

        currParser = NeuroMLXMLParser(nmlHandler) 

        currParser.parse(file_name)

        print('-------------------------------\n\n')


        nmlHandler = NetworkBuilder()   

        currParser = NeuroMLXMLParser(nmlHandler) 

        currParser.parse(file_name)

        nml_doc = nmlHandler.get_nml_doc()
        
        summary = nml_doc.summary()
        
        
        print(summary)
        
        assert(summary==summary0)
        
        print("Same!")
        
        comp = nml_doc.get_by_id("IafNet")
        print(comp)
        comp = nml_doc.get_by_id("IafNet2")

        nml_file = os.path.dirname(__file__)+'/../examples/tmp/testh5_2_.nml'
        import neuroml.writers as writers
        writers.NeuroMLWriter.write(nml_doc, nml_file)
        print("Written network file to: "+nml_file)
