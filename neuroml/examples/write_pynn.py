"""

Example to build a PyNN based network

"""

from neuroml import NeuroMLDocument
from neuroml import *
import neuroml.writers as writers
from random import random


########################   Build the network   ####################################

nml_doc = NeuroMLDocument(id="IafNet")


pynn0 = IF_curr_alpha(id="IF_curr_alpha_pop_IF_curr_alpha", cm="1.0", i_offset="0.9", tau_m="20.0", tau_refrac="10.0", tau_syn_E="0.5", tau_syn_I="0.5", v_init="-65", v_reset="-62.0", v_rest="-65.0", v_thresh="-52.0")
nml_doc.IF_curr_alpha.append(pynn0)

pynn1 = HH_cond_exp(id="HH_cond_exp_pop_HH_cond_exp", cm="0.2", e_rev_E="0.0", e_rev_I="-80.0", e_rev_K="-90.0", e_rev_Na="50.0", e_rev_leak="-65.0", g_leak="0.01", gbar_K="6.0", gbar_Na="20.0", i_offset="0.2", tau_syn_E="0.2", tau_syn_I="2.0", v_init="-65", v_offset="-63.0")
nml_doc.HH_cond_exp.append(pynn1)

pynnSynn0 = ExpCondSynapse(id="ps1", tau_syn="5", e_rev="0")
nml_doc.exp_cond_synapses.append(pynnSynn0)

newnmlfile = 'tmp/pynn_network.xml'
writers.NeuroMLWriter.write(nml_doc, newnmlfile)
print("Saved to: "+newnmlfile)


from lxml import etree
from urllib import urlopen
schema_file = urlopen("../../../NeuroML2/Schemas/NeuroML2/NeuroML_v2beta.xsd")
xmlschema = etree.XMLSchema(etree.parse(schema_file))
print "Validating %s against %s" %(newnmlfile, schema_file.geturl())
xmlschema.assertValid(etree.parse(newnmlfile))
print "It's valid!"

