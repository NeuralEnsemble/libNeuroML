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

class TestNeuroMLHDF5Optimized(unittest.TestCase):

    base_dir = os.path.dirname(__file__)
    #base_dir = '.'
    
        
    def runTest(self):
        print("Running tests in TestNeuroMLHDF5Optimized")
    
    def test_write_load(self):
        
        #for f in []:
        #for f in ['MediumNet.net.nml']:
        for f in ['complete.nml.h5']:
            file_name = '%s/../examples/test_files/%s'%(self.base_dir,f)
            
            print("Loading %s"%file_name)
        
            nml_doc0 = loaders.read_neuroml2_file(file_name,include_includes=True,optimized=True)
            summary0 = nml_doc0.summary()
            
            print(summary0)
            '''
            nml_h5_file = '%s/../examples/tmp/%s.h5'%(self.base_dir,f)
            writers.NeuroMLHdf5Writer.write(nml_doc0, nml_h5_file)
            print("Written to: %s"%nml_h5_file)
            
            nml_doc2 = loaders.NeuroMLHdf5Loader.load(nml_h5_file)

            summary1 = nml_doc2.summary()
            print('\n'+summary1)

            assert(summary0==summary1)

            print("Same!")'''
            
            

if __name__ == '__main__':
    
    tnxp = TestNeuroMLHDF5Optimized()
    tnxp.test_write_load()