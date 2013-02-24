"""

Example to build a full spiking IaF network throught libNeuroML & save it as XML & validate it

"""

from neuroml import NeuroMLDocument
from neuroml import IaFCell
from neuroml import Network
from neuroml import ExpOneSynapse
from neuroml import Population
from neuroml import PulseGenerator
from neuroml import ExplicitInput
from neuroml import SynapticConnection
import neuroml.writers as writers
from random import random


########################   Build the network   ####################################

nml_doc = NeuroMLDocument(id="IafNet")

IaFCell0 = IaFCell(id="iaf0", C="1.0 nF", thresh = "-50mV", reset="-65mV", leak_conductance="10 nS", leak_reversal="-65mV")
nml_doc.add_iafCell(IaFCell0)

IaFCell1 = IaFCell(id="iaf1", C="1.0 nF", thresh = "-50mV", reset="-65mV", leak_conductance="20 nS", leak_reversal="-65mV")
nml_doc.add_iafCell(IaFCell1)


syn0 = ExpOneSynapse(id="syn0", gbase="65nS", erev="0mV", tau_decay="3ms")
nml_doc.add_expOneSynapse(syn0)


net = Network(id="IafNet")
nml_doc.add_network(net)

size0 = 5
pop0 = Population(id="IafPop0", component=IaFCell0.id, size=size0)
net.add_population(pop0)

size1 = 5
pop1 = Population(id="IafPop1", component=IaFCell0.id, size=size1)
net.add_population(pop1)

prob_connection = 0.5

for pre in range(0,size0):

    pg = PulseGenerator(id="pulseGen_%i"%pre, delay="0ms", duration="100ms", amplitude="%f nA"%(0.1*random()))
    nml_doc.add_pulseGenerator(pg)

    net.add_explicitInput(ExplicitInput(target="%s[%i]"%(pop0.id,pre), input=pg.id))

    for post in range(0,size1):
        # fromxx is used since from is Python keyword
        if random() <= prob_connection:
            net.add_synapticConnection(SynapticConnection(fromxx="%s[%i]"%(pop0.id,pre), synapse=syn0.id, to="%s[%i]"%(pop1.id,post)))


fn = './tmp/network.xml'
writers.NeuroMLWriter.write(nml_doc, fn)



#NOTE:This is another way of doing the above, which has not yet been tested properly
###########################  Save to file & validate  #################################
#newnmlfile = "testNml2.xml"
#nml_doc.write_neuroml(newnmlfile)


#from lxml import etree
#from urllib import urlopen

#schema_file = urlopen("http://neuroml.svn.sourceforge.net/viewvc/neuroml/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd")
#xmlschema_doc = etree.parse(schema_file)
#xmlschema = etree.XMLSchema(xmlschema_doc)

#print "Validating %s against %s" %(newnmlfile, schema_file.geturl())

#doc = etree.parse(newnmlfile)
#xmlschema.assertValid(doc)
#print "It's valid!"
