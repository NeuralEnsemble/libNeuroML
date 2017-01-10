"""
Unit tests for loaders

"""

from neuroml.hdf5.NetworkBuilder import NetworkBuilder
from neuroml.hdf5.NeuroMLXMLParser import NeuroMLXMLParser
from neuroml import loaders
import logging

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLXMLParser(unittest.TestCase):
    
    def test_parse(self):
        
        base_dir = os.path.dirname(__file__)
        #base_dir = '.'
        
        logging.basicConfig(level=logging.INFO, format="%(name)-19s %(levelname)-5s - %(message)s")
        
        for f in ['simplenet.nml','testh5.nml','pyr_4_sym.cell.nml']: #for f in ['MediumNet.net.nml']:
            file_name = base_dir+'/../examples/test_files/'+f

            nml_doc0 = loaders.read_neuroml2_file(file_name,
                                                  include_includes=True,
                                                  verbose=True)
                                                  
            summary0 = nml_doc0.summary(show_includes=False,show_non_network=False)
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

            summary = nml_doc.summary(show_includes=False,show_non_network=False)

            print(summary)

            assert(summary==summary0)

            print("Same!")

            nml_file = base_dir+'/../examples/tmp/EXP_'+f
            import neuroml.writers as writers
            writers.NeuroMLWriter.write(nml_doc, nml_file)
            print("Written network file to: "+nml_file)
        
        
    def runTest(self):
        print("Running tests in TestNeuroMLXMLParser")

if __name__ == '__main__':
    
    tnxp = TestNeuroMLXMLParser()
    tnxp.test_parse()