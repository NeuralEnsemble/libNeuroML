#in the following example we create an axon object, load a
#reconstructed morphology from an SWC file and connect the
#axon to the morphology

#example of creating a section:
iseg=Section(length=20.0)
axonsec1=Section(length=1000)
node1=Section(length=20)
axonsec2=Section(length=500)
axonsec3=Section()

#connect them all together:
#standard is child.connect(parent)
axonsec1.connect(iseg)
node1.connect(axonsec1)
axonsec2.connect(node1)
axonsec3.connect(axonsec2)

#print some information from the morphology backend:
artificial_morphology=iseg.morphology
print 'Artificial morphology vertices:'
print artificial_morphology.vertices
print 'Artificial morphology connectivity:'
print artificial_morphology.connectivity
print 'Artificial morphology section types:'
print artificial_morphology.section_types

#Load a morphology from an SWC file and print some info about it
morph1=SWCLoader.load_swc_single('/home/mike/tmp2mod.swc')
print 'Loaded connectivity'
print morph1.connectivity

#now connect the loaded cell to axon (axon is child)
iseg.connect(morph1[3])
#connectivity of loaded cell now connected to an axon:
print 'New connectivity (with artificial cell connected)'
print morph1.connectivity

#can get a section object and info about it 
#easily eg by doing:
print 'Example - vertex of element 4 of morph1 morphology'
print morph1[4].vertex

#artificial_morphology is destroyed once the morphology becomes
#part of the parent morphology

print 'the artificial morphology should no longer exist:'
print 'it does however as the delete() method is not working'
print artificial_morphology[1].vertex
