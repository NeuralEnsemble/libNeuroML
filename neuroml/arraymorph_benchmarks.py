"""
Benchmarks for reading and writing arraymorphs.
"""
import numpy as np
from neuroml import arraymorph as am
import neuroml
import neuroml.writers
import tempfile

import time                                                

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return te-ts

    return timed

class WriteBenchmark(object):

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
        
    @property
    def write_time(self):
        if self.__write_time == None:
            print("Benchmark has not been executed")
        else:
            return self.__write_time

    @timeit
    def run(self):
        self.test_write_big_arraymorph()

    def test_write_big_arraymorph(self):
        writer_method = neuroml.writers.ArrayMorphWriter.write
        filename = tempfile.mkstemp()[1]

        try:
            writer_method(self.test_doc,filename)
        except:
            self.fail("Exception raised!")

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
        
from matplotlib import pyplot as plt



#prototype:
if __name__ == "__main__":

    total_results= []
    num_tests =1
    for i in range(num_tests):
        times = []
        num_segments_list = []

        for i in range(5):
            print "test %d" % (i)
            num_segments = 1e5 * i
            benchmark = WriteBenchmark(num_segments=num_segments)
            write_time = benchmark.run()
            times.append(write_time)
            num_segments_list.append(num_segments)

        total_results.append(times)

    #Need to add JSON serialization and NeuroML saerialization
    times = np.mean(total_results,axis=0)
    num_segments_list = np.array(num_segments_list)
    plt.plot(num_segments_list/1000,times)
    plt.title("ArrayMorph write to disk benchmark (HDF5 serialization)")
    plt.xlabel("Number of segments in morphology (Units of 1000 segments)")
    plt.ylabel("Time to write to disk (s)")
    plt.show()

#    plt.plot(num_segments_list/1000,times)
#    plt.title("ArrayMorph write to disk benchmark (HDF5 serialization)")
#    plt.xlabel("Number of segments in morphology (Units of 1000 segments)")
#    plt.ylabel("Time to write to disk (s)")
#    plt.show()

#    write_time = benchmark_1.write_time
