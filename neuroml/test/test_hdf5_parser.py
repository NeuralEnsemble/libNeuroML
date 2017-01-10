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
    '''
    def test_write_hdf5(self):
        
        for f in ['simplenet.nml']:
            file_name = '%s/../examples/test_files/%s'%(os.path.dirname(__file__),f)
            
            print("Loading %s"%file_name)
        
            nml_doc0 = loaders.NeuroMLLoader.load(file_name)
            summary0 = nml_doc0.summary()
            
            print summary0

            nml_h5_file = '%s/../examples/tmp/%s.h5'%(os.path.dirname(__file__),f)
            writers.NeuroMLHdf5Writer.write(nml_doc0, nml_h5_file)
            print("Written to: %s"%nml_h5_file)'''
            
            
    def test_write_xml_hdf5(self):
        
        #for f in ['simplenet.nml','MediumNet.net.nml']:
        for f in ['testh5.nml']:
            file_name = '%s/../examples/test_files/%s'%(os.path.dirname(__file__),f)
            
            print("Loading %s"%file_name)
            
        
            nml_doc0 = loaders.NeuroMLLoader.load(file_name)
            
            show_non_network = f == 'MediumNet.net.nml'
            summary0 = nml_doc0.summary(show_includes=False,show_non_network=show_non_network)
            print(summary0)

            nml_xml_file = '%s/../examples/tmp/XH_%s.nml'%(os.path.dirname(__file__),f)
            nml_h5_file = '%s/../examples/tmp/XH_%s.h5'%(os.path.dirname(__file__),f)
            writers.NeuroMLHdf5Writer.write_xml_and_hdf5(nml_doc0, nml_xml_file, nml_h5_file)
            print("Written to: %s and %s"%(nml_xml_file,nml_h5_file))
            
            nml_doc2 = loaders.read_neuroml2_file(nml_xml_file,
                                                  include_includes=True,
                                                  verbose=True)
            summary2 = nml_doc2.summary(show_includes=False,show_non_network=show_non_network)
            
            print(summary2)
            ##assert(summary0==summary2)
        
        
    '''
    def test_parse(self):
    
        file_name = os.path.dirname(__file__)+'/../examples/test_files/testh5.nml'
        
        nml_doc0 = loaders.NeuroMLLoader.load(file_name)
        summary0 = nml_doc0.summary()#
        print('\n'+summary0)

        print('-------------------------------\n\n')


        nml_h5_file = os.path.dirname(__file__)+'/../examples/tmp/testh5a.nml.h5'
        writers.NeuroMLHdf5Writer.write(nml_doc0, nml_h5_file)

        print("Written H5 network file to: "+nml_h5_file)

        nml_doc2 = loaders.NeuroMLHdf5Loader.load(nml_h5_file)

        summary1 = nml_doc2.summary()
        print('\n'+summary1)

        assert(summary0==summary1)
        
        print("Same!")

        nml_file = os.path.dirname(__file__)+'/../examples/tmp/testh5_2_.nml'
        
        writers.NeuroMLWriter.write(nml_doc2, nml_file)
        print("Written network file to: "+nml_file)'''
