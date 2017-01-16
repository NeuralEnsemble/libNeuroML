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

    base_dir = os.path.dirname(__file__)
    #base_dir = '.'
    
    def test_write_load_hdf5(self):
        
        #for f in []:
        #for f in ['MediumNet.net.nml']:
        for f in ['simplenet.nml','testh5.nml','MediumNet.net.nml','complete.nml']:
            file_name = '%s/../examples/test_files/%s'%(self.base_dir,f)
            
            print("Loading %s"%file_name)
        
            nml_doc0 = loaders.read_neuroml2_file(file_name,include_includes=True)
            summary0 = nml_doc0.summary()
            
            print(summary0)

            nml_h5_file = '%s/../examples/tmp/%s.h5'%(self.base_dir,f)
            writers.NeuroMLHdf5Writer.write(nml_doc0, nml_h5_file)
            print("Written to: %s"%nml_h5_file)
            
            nml_doc2 = loaders.NeuroMLHdf5Loader.load(nml_h5_file)

            summary1 = nml_doc2.summary()
            print('\n'+summary1)

            assert(summary0==summary1)

            print("Same!")
            
            
    def test_write_xml_hdf5(self):
        
        #for f in ['simplenet.nml','MediumNet.net.nml']:
        for f in ['testh5.nml']:
            file_name = '%s/../examples/test_files/%s'%(self.base_dir,f)
            
            print("Loading %s"%file_name)
            
        
            nml_doc0 = loaders.NeuroMLLoader.load(file_name)
            
            show_non_network = f == 'MediumNet.net.nml'
            summary0 = nml_doc0.summary(show_includes=False,show_non_network=show_non_network)
            print(summary0)

            nml_xml_file = '%s/../examples/tmp/XH_%s.nml'%(self.base_dir,f)
            nml_h5_file = '%s/../examples/tmp/XH_%s.h5'%(self.base_dir,f)
            writers.NeuroMLHdf5Writer.write_xml_and_hdf5(nml_doc0, nml_xml_file, nml_h5_file)
            print("Written to: %s and %s"%(nml_xml_file,nml_h5_file))
            
            nml_doc2 = loaders.read_neuroml2_file(nml_xml_file,
                                                  include_includes=True,
                                                  verbose=True)
            summary2 = nml_doc2.summary(show_includes=False,show_non_network=show_non_network)
            
            print(summary2)
            ##assert(summary0==summary2)
        
        
    
    def test_parse(self):
    
        file_name = self.base_dir+'/../examples/test_files/testh5.nml'
        
        nml_doc0 = loaders.NeuroMLLoader.load(file_name)
        summary0 = nml_doc0.summary(show_includes=False,show_non_network=False)
        print('\n'+summary0)

        print('-------------------------------\n\n')

        nml_h5_file = self.base_dir+'/../examples/tmp/testh5a.nml.h5'
        writers.NeuroMLHdf5Writer.write(nml_doc0, nml_h5_file)

        print("Written H5 network file to: "+nml_h5_file)

        nml_doc2 = loaders.NeuroMLHdf5Loader.load(nml_h5_file)

        summary1 = nml_doc2.summary(show_includes=False,show_non_network=False)
        print('\n'+summary1)

        assert(summary0==summary1)
        
        print("Same!")

        
    def runTest(self):
        print("Running tests in TestNeuroMLHDF5Parser")


if __name__ == '__main__':
    
    tnxp = TestNeuroMLHDF5Parser()
    tnxp.test_write_load_hdf5()