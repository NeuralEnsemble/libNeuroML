"""
Example of connecting segments together to create a 
multicompartmental model of a cell.
"""

import neuroml
import neuroml.writers as writers


p = neuroml.Point3DWithDiam(x=0,y=0,z=0,diameter=50)
d = neuroml.Point3DWithDiam(x=50,y=0,z=0,diameter=50)
soma = neuroml.Segment(proximal=p, distal=d)
soma.name = 'Soma'
soma.id = 0

#now make an axon with 100 compartments:

parent = neuroml.SegmentParent(segments=soma.id)
parent_segment = soma
axon_segments = []
seg_id = 1
for i in range(100):
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

test_morphology = neuroml.Morphology()
test_morphology.segments.append(soma)
test_morphology.segments += axon_segments
test_morphology.id = "TestMorphology"

cell = neuroml.Cell()
cell.name = 'TestCell'
cell.id = 'TestCell'
cell.morphology = test_morphology


doc = neuroml.NeuroMLDocument()
#doc.name = "Test neuroML document"

doc.cells.append(cell)
doc.id = "TestNeuroMLDocument"

fn = './tmp/test_morphology_generation.xml'

writers.NeuroMLWriter.write(doc,fn)
