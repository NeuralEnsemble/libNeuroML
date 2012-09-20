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


class BaseVoltageDepRate(KineticComponent):
    def __init__(self):
        pass


class BaseVoltageConcDepRate(KineticComponent):
    def __init__(self):
        pass


class BaseHHRate(KineticComponent):
    def __init__(self):
        pass


class HHExpRate(BaseHHRate):
    def __init__(self):
        pass


class HHSigmoidRate(BaseHHRate):
    def __init__(self):
        pass


class HHExpLinearRate(BaseHHRate):
    def __init__(self):
        pass


class BaseVoltageDepVariable(KineticComponent):
    def __init__(self):
        pass


class BaseVoltageConcDepVariable(BaseVoltageDepVariable):
    def __init__(self):
        pass


class BaseHHVariable(BaseVoltageDepVariable):
    def __init__(self):
        pass

    
class HHExpVariable(BaseHHVariable):
    def __init__(self):
        pass


class HHSigmoidVariable(BaseHHVariable):
    def __init__(self):
        pass


class HHExpLinearVariable(BaseHHVariable):
    def __init__(self):
        pass


class BaseVoltageDepTime(KineticComponent):
    def __init__(self):
        pass


class FixedTimeCourse(BaseVoltageDepTime):
    def __init__(self):
        pass


class BaseQ10Settings(KineticComponent):
    def __init__(self):
        pass


class Q10Fixed(BaseQ10Settings):
    def __init__(self):
        pass


class Q10ExpTemp(BaseQ10Settings):
    def __init__(self):
        pass


class BaseGate(KineticComponent):
    def __init__(self):
        pass


class GateHH(BaseGate):
    def __init__(self):
        pass


class BaseIonChannel(KineticComponent):
    def __init__(self):
        pass


class IonChannel(BaseIonChannel):
    def __init__(self):
        pass


class IonChannelPassive(IonChannel):
    def __init__(self):
        pass

class IonChnnelHH(IonChannel):
    def __init__(self):
        pass


class KSState(KineticComponent):
    def __init__(self):
        pass


class ClosedState(KSState):
    def __init__(self):
        pass


class OpenState(KSState):
    def __init__(self):
        pass


class IonChannelKS(IonChannel):
    def __init__(self):
        pass
        

class KSTransition(KineticComponent):
    def __init__(self):
        pass


class ForwardTransition(KSTransition):
    def __init__(self):
        pass

    
class ReverseTransition(KSTransition):
    def __init__(self):
        pass


class VHalfTransition(KSTransition):
    def __init__(self):
        pass


class GateKS(BaseGate):
    def __init__(self):
        pass


class PointCurrent(KineticComponent):
    def __init__(self):
        pass


class HHChannel(IonChannel):

    class _HHGate(KineticComponent):
        def __init__(self,name,params,vdivs=150,vmin=-90,vmax=120):
            """
            This is primarily inspired by HHGate in MOOSE as per MOOSE
            the params set up both gates using 10 parameters, as follows:

            AA AB AC AD AF BA BB BC BD BF

            Here AA-AF are Coefficients A to F of the alpha (forward) term
            Here BA-BF are Coefficients A to F of the beta (reverse) term

            Here xdivs is the number of entries in the table, xmin and xmax
            define the range for lookup (Only relevant to MOOSE)
            Outside this range the returned value will be the low [high]
            entry of the table.

            The equation describing each table is:
            y(x) = (A + B * x) / (C + exp((x + D) / F))
            The original HH equations can readily be cast into this form
            """
            self.name = name
            self.params = params
            self.vmin = vmin
            self.vmax = vmax
            self.vdivs = vdivs
                  
    def __init__(self, name, specific_gbar, ion,
                 e_rev, x_power, y_power=0.0, z_power=0.0):

        """Instantiate an ion channel.

        name -- name of the channel.
        
        specific_gbar -- specific value of maximum conductance.

        e_rev -- reversal potential of the channel.
        
        Xpower -- exponent for the first gating parameter.

        Ypower -- exponent for the second gatinmg component.
        """

        self.ion = ion
        self.type = 'HHChannel'
        self.specific_gbar = specific_gbar
        self.e_rev = e_rev
        self.x_power = x_power
        self.y_power = y_power
        self.z_power = z_power
        self.channel_name = name
        self.reversal_potential = e_rev

    def setup_alpha(self, gate, params, vdivs, vmin, vmax):
        """
        Setup alpha and beta parameters of specified gate.

        gate -- 'X'/'Y'/'Z' string initial of the gate.

        params -- dict of parameters to compute alpha and beta, the rate constants for gates.

        vdivs -- number of divisions in the interpolation tables for alpha and beta parameters.

        vmin -- minimum voltage value for the alpha/beta lookup tables.

        vmax -- maximum voltage value for the alpha/beta lookup tables.
        """
        #need to set up a dict so that there is correspondence between
        #the gate and the parameters, gate can be X,Y or Z

        self.vmin = vmin
        self.vmax = vmax
        
        if gate == 'X':
            self.x_gating_params = params
            self.x_gate=self._HHGate(gate,params,vdivs=vdivs,vmin=vmin,vmax=vmax)
        elif gate == 'Y':
            self.y_gating_params = params
            self.y_gate=self._HHGate(gate,params,vdivs=vdivs,vmin=vmin,vmax=vmax)
        elif gate == 'Z':
            self.z_gating_params = params
            self.z_gate=self._HHGate(gate,params,vdivs=vdivs,vmin=vmin,vmax=vmax)
        else:
            raise(NotImplementedError,"This is an unkown gate")
        return True


class Synapse(KineticComponent):
    def __init__(self):
        pass


class ExtracellularProperties(KineticComponent):
    def __init__(self):
        pass


class PassiveProperties(KineticComponent):
    """
    """
    def __init__(self,rm=5e9,cm=1e-12,ra=1e6,init_vm=-65e-3):
        self.init_vm = init_vm # Initial membrane potential
        self.rm = rm # Total membrane resistance of the compartment
        self.cm = cm# Total membrane capacitance of the compartment
        self.ra = ra # Total axial resistance of the compartment


class LeakCurrent(IonChannel):
    """
    """
    def __init__(self,em=-65e-3):
        self.em = em

        
class IClamp(PointCurrent):
    """
    Steady point current injection
    
    :param current: injected current
    :param delay: initiation of current injection
    :param duration: current injection duration
    :param fraction_along: fraction along section for current injection
    """

    def __init__(self,current,delay,duration,fraction_along=None):
        self.type = 'IClamp'
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
    def __init__(self,name,attribute_values = None):
        self.type = 'NMODL'
        self.name = name

        if attribute_values != None:
            #any accessible attribute should be settable through this
            self.attribute_values = attribute_values
        else:
            attribute_values = {}
