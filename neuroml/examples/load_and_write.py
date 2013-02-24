import neuroml
from neuroml import loaders

doc = loaders.NeuroMLLoader.load('Purk2M9s.nml')

f = open('./tmp/test_load_and_write.xml','w')
doc.export(f,0)
