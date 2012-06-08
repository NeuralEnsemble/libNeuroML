import neuroml.morphology as ml
a=ml.Node()
b=ml.Node()
c=ml.Node()
d=ml.Node()
a.connect(b)
b.connect(c)
c.connect(d)

print 'old connectivity:'
print a.morphology.connectivity
print 'new connectivity:'
a.morphology.to_root(2)
print a.morphology.connectivity
