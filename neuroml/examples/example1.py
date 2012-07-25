"""
In this example an axon is built, a morphology is loaded, the axon is
then connected to the loadeed morphology. As of 6/7/12 this is working except
for a bug in loading one of the nml segments - need to investigate
"""

import neuroml.loaders as loaders
import neuroml.morphology as ml
import os

iseg=ml.Segment(length=10,proximal_diameter=1,distal_diameter=2)
myelin1=ml.Segment(length=100,proximal_diameter=3,distal_diameter=4)
node1=ml.Segment(length=10,proximal_diameter=5,distal_diameter=6)
myelin2=ml.Segment(length=100,proximal_diameter=7,distal_diameter=8)
node2=ml.Segment(length=10.0,proximal_diameter=9,distal_diameter=10)

iseg.attach(myelin1)
myelin1.attach(node1)
node1.attach(myelin2)
myelin2.attach(node2)

filepath = '../../testFiles/NML2_FullCell.nml'
print(filepath)

doc=loaders.NeuroMLLoader.load_neuroml(filepath)
cell=doc.cells[0]
morphology=cell.morphology

print('Before attaching axon:')
for i,seg in enumerate(morphology):
    print('segment '+str(i)+' distal diameter:' + str(seg.distal_diameter))
    print('segment '+str(i)+' proximal diameter:' + str(seg.proximal_diameter))

morphology.attach(iseg)
total_morphology=iseg.morphology

print('\nAfter attaching axon:')
for i,seg in enumerate(total_morphology):
    print('segment '+str(i)+' distal diameter:' + str(seg.distal_diameter))
    print('segment '+str(i)+' proximal diameter:' + str(seg.proximal_diameter))

#now do a sanity test, the observer in the backend should 
#guarantee that this returns true despite the lazy evaluation of
#segment elements
print(total_morphology[0] == total_morphology[0])
