import neuroml.loaders as loaders
import neuroml.morphology as ml

iseg=ml.Segment(length=10,proximal_diameter=1,distal_diameter=2)
myelin1=ml.Segment(length=100,proximal_diameter=3,distal_diameter=4)
node1=ml.Segment(length=10,proximal_diameter=5,distal_diameter=6)
myelin2=ml.Segment(length=100,proximal_diameter=7,distal_diameter=8)
node2=ml.Segment(length=10.0,proximal_diameter=9,distal_diameter=10)

iseg.attach(myelin1)
myelin1.attach(node1)
node1.attach(myelin2)
myelin2.attach(node2)
print #~~~#
print 'physical indices:'
print iseg._backend.physical_indices
print 'physical mask:'
print iseg._backend._physical_mask
print 'connectivity:'
print iseg._backend.connectivity
print 'vertices:'
print iseg._backend.vertices

for seg in iseg.morphology:
    print seg.proximal_diameter
    print seg.distal_diameter

#doc=loaders.NeuroMLLoader.load_neuroml('/home/mike/dev/libNeuroML/testFiles/NML2_FullCell.nml')
#cell=doc.cells[0]
#morphology=cell.morphology

#print morphology._backend.vertices
#morphology.attach(iseg)
#print morphology._backend.vertices
