# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull, Michael Vella
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

import neuroml.morphology as morphology
from neuroml.morphology import MorphologyArray
import random

"""
This module is in its early stages but demonstrates how one can
generate morphologies artificially using segment objects which
control the morphology backend.
"""

def __grand(sigma):
    import random

    random_number=abs(random.gauss(1.0,sigma))
    return random_number

def __branch_decision(probability):
    """
    For a fixed probability returns a 1 or a 0

    The function is used to decide whether a bifibrication should occur
    """        
    return random.random() < probability

def __rall_power(parent_diam,e=1.5):
    """
    Returns the diameter of a child segment of a branch 
    according to Rall's Power Law as described
    in Van Ooyen et al 2010. Assumes child branches
    will be of equal diameter.
    """

    child_diam=parent_diam/(2**(1/e))
    return child_diam

def soma(radius=30,length=30):
    segment=morphology.Segment(r1=radius,length=30)
    return segment.morphology


def arborization(bifurcations=3.0,root_L=100.0,term_L=1.0,
                 root_d=10.0,term_d=1,L_sigma=0.0,branch_prob=1.0):

    """
    returns a morphology corresponding to a dendritic tree
    """

    root_segment_length=root_L*__grand(L_sigma)
    root_segment=morphology.Segment(r1=root_d,
                                length=root_segment_length)
        
    heads=[root_segment]                            
    i=0
    while i<bifurcations:
        i+=1
        new_heads=[]
        for head in heads:
            #make decision whether to branch
            if __branch_decision(branch_prob):
                segment_length=(term_L-root_L)*i/bifurcations+root_L
                segment_diam=__rall_power(head.r1)
                if segment_diam<term_d:
                    segment_diam=term_d

                #make two segments for it:
                branch1_l=segment_length*__grand(L_sigma)
                branch2_l=segment_length*__grand(L_sigma)

                branch1=morphology.Segment(length=branch1_l,r1=
                                            segment_diam)
                branch2=morphology.Segment(length=branch2_l,r1=
                                            segment_diam)

                branch1.connect(head)
                branch2.connect(head)
                new_heads+=[branch1,branch2]
                
        heads=new_heads
    
    return root_segment.morphology
