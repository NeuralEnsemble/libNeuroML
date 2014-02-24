"""
Benchmarks for reading and writing arraymorphs.
"""
import numpy as np
from neuroml import arraymorph as am
import neuroml
import neuroml.writers
import tempfile
from matplotlib import pyplot as plt
import time                                                
import os
from os import path

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return te-ts

    return timed

class AMWriteBenchmark(object):
    """
    TODO: Get rid of methods which are not used
    """
    def __init__(self,num_segments=1e6):
        num_segments = int(num_segments)
        num_vertices = int(num_segments) + 1

        x = np.linspace(0,10,num_vertices)
        y = np.zeros(num_vertices)
        z = np.zeros(num_vertices)
        d = np.linspace(1,0.01,num_vertices)

        vertices = np.array([x,y,z,d]).T
        
        connectivity = range(-1,num_segments)

        big_arraymorph = am.ArrayMorphology(vertices = vertices,
                                            connectivity = connectivity)

        self.big_arraymorph = big_arraymorph

        self.cell = neuroml.Cell(id='test_cell')

        self.cell.morphology = big_arraymorph

        self.test_doc = neuroml.NeuroMLDocument(id='TestDocument')

        self.test_doc.cells.append(self.cell)

        self.__write_time = None

        self.num_segments = num_segments
        
    @property
    def write_time(self):
        if self.__write_time == None:
            print("Benchmark has not been executed")
        else:
            return self.__write_time

    @timeit
    def run_neuroml(self):
        self.test_write_big_arraymorph_neuroml()

    @timeit
    def run_json(self):
        self.test_write_big_arraymorph_json()

    @timeit
    def run_hdf5(self):
        self.test_write_big_arraymorph_hdf5()


    def test_write_big_arraymorph_json(self):
        writer_method = neuroml.writers.JSONWriter.write
        fh,filename = tempfile.mkstemp()

        try:
            writer_method(self.test_doc,filename)
        except:
            self.fail("Exception raised!")

        print 'JSON Number of segments:'
        print self.num_segments
        print 'JSON size in bytes:'
        print self.file_size(filename)

        os.close(fh)

    def test_write_big_arraymorph_neuroml(self):
        writer_method = neuroml.writers.NeuroMLWriter.write
        fh,filename = tempfile.mkstemp()

        try:
            writer_method(self.test_doc,filename)
        except:
            self.fail("Exception raised!")

        print 'NeuroML (XML) Number of segments:'
        print self.num_segments
        print 'NeuroML (XML) size in bytes:'
        print self.file_size(filename)

        os.close(fh)

    def file_size(self,path):
        return os.path.getsize(path)


    def test_write_big_arraymorph_hdf5(self):
        writer_method = neuroml.writers.ArrayMorphWriter.write
        fh,filename = tempfile.mkstemp()

        try:
            writer_method(self.test_doc,filename)
        except:
            self.fail("Exception raised!")

        print 'HDF5 Number of segments:'
        print self.num_segments
        print 'HDF5 size in bytes:'
        print self.file_size(filename)

        os.close(fh)

    def test_write_expected(self):
        """
        More of an integration test, write a file and confirm the contents are
        as expected.
        """

        filename = tempfile.mkstemp()[1]
        writer_method = neuroml.writers.ArrayMorphWriter.write
        writer_method(self.big_arraymorph,filename)

        loader_method = neuroml.loaders.ArrayMorphLoader.load
        doc = loader_method(filename)
        array_morph = doc.morphology[0]

        connectivity_equal = np.testing.assert_array_equal(array_morph.connectivity,self.big_arraymorph.connectivity)
        physical_masks_equal = np.testing.assert_array_equal(array_morph.physical_mask,self.big_arraymorph.physical_mask)
        vertices_equal = np.testing.assert_array_equal(array_morph.vertices,self.big_arraymorph.vertices)


        self.assertEqual(connectivity_equal,None) #None when equal
        self.assertEqual(physical_masks_equal,None) #None when equal
        self.assertEqual(vertices_equal,None) #None when equal        

    def test_write_multiple_morphologies(self):
        filename = tempfile.mkstemp()[1]

        writer_method = neuroml.writers.ArrayMorphWriter.write
        try:
            writer_method(self.test_doc,filename)
        except:
            self.fail("Exception raised!")

    def test_write_multiple_morphologies(self):
        filename = tempfile.mkstemp()[1]
        writer_method = neuroml.writers.ArrayMorphWriter.write
        writer_method(self.test_doc,filename)

        loader_method = neuroml.loaders.ArrayMorphLoader.load
        document = loader_method(filename)

        self.assertIsInstance(document,neuroml.NeuroMLDocument)





def benchmark_arraymorph_writer():
    """
    TODO: Add NeuroML Document benchmark
    TODO: Make the script a bit more understandable and modularised
    """
    num_tests = 10

    json_results= []
    neuroml_results= []
    hdf5_results= []

    for i in range(num_tests):
        json_runtimes = []
        hdf5_runtimes = []
        neuroml_runtimes = []

        json_num_segments_list = []
        hdf5_num_segments_list = []
        neuroml_num_segments_list = []

        for i in range(30):
            print "test %d" % (i)

            neuroml_num_segments_factor = 4e2
            json_num_segments_factor = 4e2
            hdf5_num_segments_factor = 4e2
            
            neuroml_num_segments = i * neuroml_num_segments_factor
            json_num_segments = i * json_num_segments_factor
            hdf5_num_segments = i * hdf5_num_segments_factor

            neuroml_benchmark = AMWriteBenchmark(num_segments=neuroml_num_segments)
            json_benchmark = AMWriteBenchmark(num_segments=json_num_segments)
            hdf5_benchmark = AMWriteBenchmark(num_segments=hdf5_num_segments)

            write_time_neuroml = neuroml_benchmark.run_neuroml()
            write_time_json = json_benchmark.run_json()
            write_time_hdf5 = hdf5_benchmark.run_hdf5()

            neuroml_runtimes.append(write_time_neuroml)
            json_runtimes.append(write_time_json)
            hdf5_runtimes.append(write_time_hdf5)

            neuroml_num_segments_list.append(neuroml_num_segments)
            json_num_segments_list.append(json_num_segments)
            hdf5_num_segments_list.append(hdf5_num_segments)

        neuroml_results.append(neuroml_runtimes)
        json_results.append(json_runtimes)
        hdf5_results.append(hdf5_runtimes)

        np.savetxt("neuroml_results.csv", neuroml_results, delimiter=",")
        np.savetxt("json_results.csv", json_results, delimiter=",")
        np.savetxt("hdf5_results.csv", hdf5_results, delimiter=",")


    neuroml_runtimes_averaged = np.mean(neuroml_results,axis=0)
    json_runtimes_averaged = np.mean(json_results,axis=0)
    hdf5_runtimes_averaged = np.mean(hdf5_results,axis=0)

    hdf5_errors = np.std(hdf5_results,axis=0)
    json_errors = np.std(json_results,axis=0)
    neuroml_errors = np.std(neuroml_results,axis=0)

    neuroml_num_segments_list = np.array(neuroml_num_segments_list)
    json_num_segments_list = np.array(json_num_segments_list)
    hdf5_num_segments_list = np.array(hdf5_num_segments_list)


    plt_neuroml = plt.errorbar(neuroml_num_segments_list,
                 neuroml_runtimes_averaged,
                 yerr=hdf5_errors,
                 marker='o',
                 color='k',
                 ecolor='k',
                 markerfacecolor='r',
                 label="series 2",
                 capsize=5,)
    plt.title("ArrayMorph write to disk benchmark (NeuroML (XML) serialization)")
    plt.xlabel("Number of segments in morphology (Units of 1000 segments)")
    plt.ylabel("Time to write to disk (s)")

    plt_hdf5 = plt.errorbar(hdf5_num_segments_list,
                 hdf5_runtimes_averaged,
                 yerr=hdf5_errors,
                 marker='o',
                 color='k',
                 ecolor='k',
                 markerfacecolor='g',
                 label="series 2",
                 capsize=5,)
    plt.title("ArrayMorph write to disk benchmark (HDF5 serialization)")
    plt.xlabel("Number of segments in morphology (Units of 1000 segments)")
    plt.ylabel("Time to write to disk (s)")

#    plt.show()

    plt_json = plt.errorbar(json_num_segments_list,
                 json_runtimes_averaged,
                 yerr=json_errors,
                 marker='o',
                 color='k',
                 ecolor='k',
                 markerfacecolor='b',
                 label="series 2",
                 capsize=5,)

    plt.title("ArrayMorph write to disk benchmarks for JSON, HDF5 and NeuroML serialization formats")
    plt.xlabel("Number of segments in morphology")
    plt.ylabel("Time to write to disk (s)")

    plt.legend([plt_json, plt_hdf5,plt_neuroml], ["JSON serialization", "HDF5 serialization","NeuroML serialization"])

    plt.yscale('log')
    plt.xscale('log')
    plt.show()

#prototype:
if __name__ == "__main__":
    benchmark_arraymorph_writer()
