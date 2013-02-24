"""
In this example an axon is built, a morphology is loaded, the axon is
then connected to the loadeed morphology.
"""

import neuroml
import neuroml.loaders as loaders
import neuroml.writers as writers

doc = loaders.NeuroMLLoader.load('./test_files/Purk2M9s.nml')

#get the parent segment:
parent_segment = doc.cells[0].morphology.segments[0]

parent = neuroml.SegmentParent(segments=parent_segment.id)

#make an axon:
seg_id = 5000 # need a way to get a unique id from a morphology
axon_segments = []
for i in range(10):
    p = neuroml.Point3DWithDiam(x=parent_segment.distal.x,
                                y=parent_segment.distal.y,
                                z=parent_segment.distal.z,
                                diameter=0.1)

    d = neuroml.Point3DWithDiam(x=parent_segment.distal.x+10,
                                y=parent_segment.distal.y,
                                z=parent_segment.distal.z,
                                diameter=0.1)

    axon_segment = neuroml.Segment(proximal = p, 
                                   distal = d, 
                                   parent = parent)

    axon_segment.id = seg_id
    
    axon_segment.name = 'axon_segment_' + str(axon_segment.id)

    #now reset everything:
    parent = neuroml.SegmentParent(segments=axon_segment.id)
    parent_segment = axon_segment
    seg_id += 1 

    axon_segments.append(axon_segment)

doc.cells[0].morphology.segments += axon_segments

fn = './tmp/modified_morphology.nml'

writers.NeuroMLWriter.write(doc,fn)
