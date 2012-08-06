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

class KineticComponent(object):
    def __init__(self):
        pass


class PointCurrent(KineticComponent):
    def __init__(self):
        pass


class IonChannel(KineticComponent):
    def __init__(self):
        pass


class Synapse(KineticComponent):
    def __init__(self):
        pass


class ExtracellularProperties(KineticComponent):
    def __init__(self):
        pass


class IClamp(PointCurrent):
    """
    Steady point current injection
    
    :param current: injected current in pA
    :param delay: initiation of current injection, in ms
    :param duration: current injection duration, in ms
    :param fraction_along: fraction along section for current injection
    """

    def __init__(self,current,delay,duration,fraction_along=None):
        self.name = 'IClamp'
        self.amp = current
        self.delay = delay
        self.dur = duration

        if fraction_along != None:
            self.fraction_along = fraction_along
        else:
            self.fraction_along = 0.5

class Nmodl(IonChannel):
    """
    NMODL (NEURON-Compatible) ion channel description
    plan for now is that these still need to be
    precompiled and located in the correct folder
    """
    def __init__(self,name):
        self.type = 'NMODL'
        self.name = name
        self.attributes={}

