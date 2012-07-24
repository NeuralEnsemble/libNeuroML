"""
Example of connecting segments together to create a 
multicompartmental model of a cell:
"""

import neuroml.morphology as ml

soma=ml.Segment(length=50,proximal_diameter=10)
iseg=ml.Segment(length=200,proximal_diameter=3)
node1=ml.Segment(length=20,proximal_diameter=1)
myelin1=ml.Segment(length=200,proximal_diameter=2)
node2=ml.Segment(length=20,proximal_diameter=1)
myelin2=ml.Segment(length=200,proximal_diameter=2)

myelin2.attach(node2)
node2.attach(myelin1)
myelin1.attach(node1)
node1.attach(iseg)
iseg.attach(soma)

print('vertices:')
print(soma.morphology.vertices)
print('connectivity:')
print(soma.morphology.connectivity)
