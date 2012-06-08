"""
This example shows simple node connectivity
"""

import neuroml.morphology as ml

a=ml.Node()
b=ml.Node()
c=ml.Node()
a.connect(b)
c.connect(b)
chain1=a.morphology
#now create and connect a new node:
d=ml.Node()
d.connect(c)
chain2=d.morphology

#now let's make yet another chain:
f=ml.Node()
g=ml.Node()
h=ml.Node()
f.connect(g)
g.connect(h)

chain3=g.morphology
chain3[0].connect(chain1[1])
morph1=a.morphology


