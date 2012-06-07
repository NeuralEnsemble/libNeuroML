#let's show how sections can be used


import neuroml.morphology as ml

soma=ml.Segment(length=0,r1=0)
axon=ml.Segment(length=0,r1=0)
soma.connect(axon)

print soma.morphology.connectivity
print soma.morphology.vertices
