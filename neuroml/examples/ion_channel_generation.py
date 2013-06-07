"""
Generating a Hodgkin-Huxley Ion Channel and writing it to NeuroML
"""

import neuroml
import neuroml.writers as writers

chan = neuroml.IonChannel(id='na',
                          type='ionChannelHH',
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

chan.gates.append(m_gate)
chan.gates.append(h_gate)

doc = neuroml.NeuroMLDocument()
doc.ion_channels.append(chan)

doc.id = "ChannelMLDemo"

fn = './tmp/channelMLtest.xml'
writers.NeuroMLWriter.write(doc,fn)
