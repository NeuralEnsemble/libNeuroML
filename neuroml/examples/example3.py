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

"""
This example shows how segments are created and manipulated and
how a morphology is loaded
"""

import neuroml.morphology as morphology
import neuroml.loaders as loaders

#example of creating a segment:
iseg=morphology.Segment(length=20.0)
axonsec1=morphology.Segment(length=1000)
node1=morphology.Segment(length=20)
axonsec2=morphology.Segment(length=500)
axonsec3=morphology.Segment()

#connect them all together:
#standard is child.attach(parent)
axonsec1.attach(iseg)
node1.attach(axonsec1)
axonsec2.attach(node1)
axonsec3.attach(axonsec2)

#print some information from the morphology (nodecollection) backend: -
#potentially it would make more sense to offer a segmentcollection view of this too
artificial_morphology=iseg.morphology
print('Artificial morphology vertices:')
print(artificial_morphology.vertices)
print('Artificial morphology connectivity:')
print(artificial_morphology.connectivity)

#Load a morphology from an SWC file and print some info about it
morph1=loaders.SWCLoader.load_swc_single('./reconstructed_morphologies/tmp2.swc')
print('Loaded connectivity')
print(morph1.connectivity)
