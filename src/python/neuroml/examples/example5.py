"""
This example shows how a morphology can be translated
such that the translated node moves to the new origin
and all other nodes move along with it
"""
import neuroml.morphology as ml

a=ml.Node([1,2,3,10])
b=ml.Node([4,5,6,20])
a.connect(b)
print a.morphology.vertices
b.translate_morphology([1,2,3])
print 'translated:'
print b.morphology.vertices
