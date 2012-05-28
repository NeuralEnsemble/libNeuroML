import neuroml.morphology as ml

a=ml.Node()
b=ml.Node()
testmorph=a.morphology
print testmorph.connectivity
a.connect(b)
print 'should work...'
print a.morphology.connectivity
print 'should fail as testmorph no longer references anything...'
print testmorph.connectivity
