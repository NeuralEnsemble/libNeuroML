"""
This example shows simple node connectivity
"""

import neuroml.morphology as ml

a=ml.Node()
b=ml.Node()
c=ml.Node()
a.attach(b)
c.attach(b)
chain1=a.morphology
#now create and connect a new node:
d=ml.Node()
d.attach(c)
chain2=d.morphology

#now let's make yet another chain:
f=ml.Node()
g=ml.Node()
h=ml.Node()
f.attach(g)
g.attach(h)

chain3=g.morphology
chain3[0].attach(chain1[1])
morph1=a.morphology

print morph1.vertices
