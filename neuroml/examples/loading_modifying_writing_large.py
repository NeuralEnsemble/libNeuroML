"""
In this example an axon is built, a morphology is loaded, the axon is
then connected to the loadeed morphology.
"""

import neuroml
import neuroml.loaders as loaders
import neuroml.writers as writers


from guppy import hpy
h = hpy()



fn = './test_files/EC2-609291-4.CNG.nml'
#fn = './test_files/Purk2M9s.nml'

cells = []

numCells = 1

for n in range(numCells):

    doc = loaders.NeuroMLLoader.load(fn)
    cells.append(doc.cells[0])
    print("Loaded morphology file from: "+fn)

    #get the parent segment:
    parent_segment = doc.cells[0].morphology.segments[0]

    print("Cell %i has %i segments"%(n,len(doc.cells[0].morphology.segments)))
    print(h.heap())


    
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
    

fn = './tmp/modified_morphology2.nml'

writers.NeuroMLWriter.write(doc,fn)

print("Saved modified morphology file to: "+fn)


print("Done")



