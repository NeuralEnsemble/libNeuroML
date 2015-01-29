"""
Generating a Hodgkin-Huxley Ion Channel and writing it to NeuroML
"""

import neuroml
import neuroml.writers as writers

chan = neuroml.IonChannelHH(id='na',
                          conductance='10pS',
                          species='na',
                          notes="This is an example voltage-gated Na channel")

m_gate = neuroml.GateHHRates(id='m',instances='3')
h_gate = neuroml.GateHHRates(id='h',instances='1')

m_gate.forward_rate = neuroml.HHRate(type="HHExpRate",
                                     rate="0.07per_ms",
                                     midpoint="-65mV",
                                     scale="-20mV")

m_gate.reverse_rate = neuroml.HHRate(type="HHSigmoidRate",
                                     rate="1per_ms",
                                     midpoint="-35mV",
                                     scale="10mV")

h_gate.forward_rate = neuroml.HHRate(type="HHExpLinearRate",
                                     rate="0.1per_ms",
                                     midpoint="-55mV",
                                     scale="10mV")

h_gate.reverse_rate = neuroml.HHRate(type="HHExpRate",
                                     rate="0.125per_ms",
                                     midpoint="-65mV",
                                     scale="-80mV")

chan.gate_hh_rates.append(m_gate)
chan.gate_hh_rates.append(h_gate)

doc = neuroml.NeuroMLDocument()
doc.ion_channel_hhs.append(chan)

doc.id = "ChannelMLDemo"

nml_file = './tmp/ionChannelTest.xml'
writers.NeuroMLWriter.write(doc,nml_file)

print("Written channel file to: "+nml_file)


###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)
