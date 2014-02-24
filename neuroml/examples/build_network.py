"""

Example to build a full spiking IaF network
through libNeuroML, save it as XML and validate it

"""

from neuroml import NeuroMLDocument
from neuroml import IafCell
from neuroml import Network
from neuroml import ExpOneSynapse
from neuroml import Population
from neuroml import PulseGenerator
from neuroml import ExplicitInput
from neuroml import SynapticConnection
import neuroml.writers as writers
from random import random


nml_doc = NeuroMLDocument(id="IafNet")

IafCell0 = IafCell(id="iaf0",
                   C="1.0 nF",
                   thresh = "-50mV",
                   reset="-65mV",
                   leak_conductance="10 nS",
                   leak_reversal="-65mV")

nml_doc.iaf_cells.append(IafCell0)

IafCell1 = IafCell(id="iaf1",
                   C="1.0 nF",
                   thresh = "-50mV",
                   reset="-65mV",
                   leak_conductance="20 nS",
                   leak_reversal="-65mV")

nml_doc.iaf_cells.append(IafCell1)

syn0 = ExpOneSynapse(id="syn0",
                     gbase="65nS",
                     erev="0mV",
                     tau_decay="3ms")

nml_doc.exp_one_synapses.append(syn0)

net = Network(id="IafNet")

nml_doc.networks.append(net)

size0 = 5
pop0 = Population(id="IafPop0",
                  component=IafCell0.id,
                  size=size0)

net.populations.append(pop0)

size1 = 5
pop1 = Population(id="IafPop1",
                  component=IafCell0.id,
                  size=size1)

net.populations.append(pop1)

prob_connection = 0.5

for pre in range(0,size0):

    pg = PulseGenerator(id="pulseGen_%i"%pre,
                        delay="0ms",
                        duration="100ms",
                        amplitude="%f nA"%(0.1*random()))

    nml_doc.pulse_generators.append(pg)

    exp_input = ExplicitInput(target="%s[%i]"%(pop0.id,pre),
                                             input=pg.id)

    net.explicit_inputs.append(exp_input)

    for post in range(0,size1):
        # fromxx is used since from is Python keyword
        if random() <= prob_connection:
            syn = SynapticConnection(from_="%s[%i]"%(pop0.id,pre),
                                     synapse=syn0.id,
                                     to="%s[%i]"%(pop1.id,post))
            net.synaptic_connections.append(syn)

nml_file = 'tmp/testnet.nml'
writers.NeuroMLWriter.write(nml_doc, nml_file)


print("Written network file to: "+nml_file)


###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)
