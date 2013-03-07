import neuroml
from neuroml import loaders
import neuroml.writers as writers

doc = loaders.NeuroMLLoader.load('./test_files/Purk2M9s.nml')

fn = './tmp/test_load_and_write.xml'

writers.NeuroMLWriter.write(doc,fn)
