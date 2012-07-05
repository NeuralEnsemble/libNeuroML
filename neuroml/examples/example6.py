import neuroml.loaders as loaders
import neuroml.morphology as ml

a=ml.Segment(proximal_diameter=1,distal_diameter=2)
b=ml.Segment(proximal_diameter=3,distal_diameter=4)
a.attach(b)
print a._backend.connectivity
print a._backend.vertices


doc=loaders.NeuroMLLoader.load_neuroml('/home/mike/dev/libNeuroML/testFiles/NML2_FullCell.nml')
cell=doc.cells[0]
morphology=cell.morphology
segment0=morphology[0]
segment3=morphology[3]
