"""
Unit tests for loaders

"""

from neuroml import loaders
import neuroml.writers as writers

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestNeuroMLHDF5Parser(unittest.TestCase):

    def test_parse(self):
    
        file_name = os.path.dirname(__file__)+'/../examples/test_files/testh5.nml'
        
        nml_doc0 = loaders.NeuroMLLoader.load(file_name)
        sum0 = nml_doc0.summary()#
        print('\n'+sum0)



        print('-------------------------------\n\n')


        nml_h5_file = os.path.dirname(__file__)+'/../examples/tmp/testh5a.nml.h5'
        writers.NeuroMLHdf5Writer.write(nml_doc0, nml_h5_file)

        print("Written H5 network file to: "+nml_h5_file)


        nml_doc2 = loaders.NeuroMLHdf5Loader.load(nml_h5_file)

        sum1 = nml_doc2.summary()
        print('\n'+sum1)

        assert(sum0==sum1)
        
        print("Same!")

        nml_file = os.path.dirname(__file__)+'/../examples/tmp/testh5_2_.nml'
        
        writers.NeuroMLWriter.write(nml_doc2, nml_file)
        print("Written network file to: "+nml_file)
