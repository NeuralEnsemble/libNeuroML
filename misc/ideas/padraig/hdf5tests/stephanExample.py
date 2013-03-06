import h5py
import numpy as np

neurohdf = h5py.File('neuroHdf.hdf', 'w')
neurohdf.attrs['neurohdf_version'] = '0.1'

mcgroup = neurohdf.create_group("Single Neuron Morphology")
vert = mcgroup.create_group("vertices")
conn = mcgroup.create_group("connectivity")

vert.create_dataset("id", data=np.array( [100,200,300], dtype = np.uint8) )
vert.create_dataset("location", data=np.random.rand( 3, 3 ).astype(np.float32) )
vert_type=vert.create_dataset("type", data=np.array( [1,2,3], dtype = np.uint8) )
vert_type.attrs['value'] = np.array([
    ['1', 'skeleton'],
    ['2', 'skeleton root'],
    ['3', 'connector']
    ])

vert.create_dataset("confidence", data=np.array( [5,5,5], dtype = np.uint8))
vert_radius=vert.create_dataset("radius", data=np.array( [5,4,2], dtype = np.float32))
vert_radius.attrs['unit_label'] = 'um'
vert_radius.attrs['unit_xref'] = 'PURL:...' # reference to ontology for um concept

conn.create_dataset("id", data=np.array( [11,12,13], dtype = np.uint8) )
conn_type=conn.create_dataset("type", data=np.array( [1,2,3], dtype = np.uint8))
conn_type.attrs['value'] = np.array([
    ['1', 'neurite'],
    ['2', 'presynaptic'],
    ['3', 'postsynaptic']
    ])
# other values could be: axonal arbor, dendrite, spine neck, spine head, cell body
neurohdf.close()
