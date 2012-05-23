# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Vella
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

#in the following example we create an axon object, load a
#reconstructed morphology from an SWC file and connect the
#axon to the morphology

import neuroml.morphology as morphology
import neuroml.loaders as loaders

#example of creating a section:
iseg=morphology.Section(length=20.0)
axonsec1=morphology.Section(length=1000)
node1=morphology.Section(length=20)
axonsec2=morphology.Section(length=500)
axonsec3=morphology.Section()

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
morph1=loaders.SWCLoader.load_swc_single('/home/mike/tmp2mod.swc')
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
