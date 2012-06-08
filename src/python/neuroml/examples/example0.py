#Connecting segments together to create a multicompartmental model of a cell:

import neuroml.morphology as ml

soma=ml.Segment(length=50,r1=10)
iseg=ml.Segment(length=200,r1=3)
node1=ml.Segment(length=20,r1=1)
myelin1=ml.Segment(length=200,r1=2)
node2=ml.Segment(length=20,r1=1)
myelin2=ml.Segment(length=200,r1=2)

myelin2.connect(node2)
node2.connect(myelin1)
myelin1.connect(node1)
node1.connect(iseg)
iseg.connect(soma)

print('vertices:')
print(soma.morphology.vertices)
print('connectivity:')
print(soma.morphology.connectivity)
