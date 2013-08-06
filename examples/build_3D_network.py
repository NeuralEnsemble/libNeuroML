"""

Example to build a full spiking IaF network throught libNeuroML & save it as XML & validate it

"""

from neuroml import NeuroMLDocument
from neuroml import Network
from neuroml import ExpOneSynapse
from neuroml import Population
from neuroml import SynapticConnection
from neuroml import Cell
from neuroml import Location
from neuroml import Instance
from neuroml import Morphology
from neuroml import Point3DWithDiam
from neuroml import Segment



import neuroml.writers as writers
from random import random

def generateRandomMorphology():

    soma_diam = 10
    soma_len = 10
    dend_diam = 2

    p = Point3DWithDiam(x=0,y=0,z=0,diameter=soma_diam)
    d = Point3DWithDiam(x=soma_len,y=0,z=0,diameter=soma_diam)
    soma = Segment(proximal=p, distal=d)
    soma.name = 'Soma'
    soma.id = 0

    morphology = Morphology()
    morphology.segments.append(soma)
    #morphology.segments += axon_segments
    morphology.id = "TestMorphology"

    return morphology

def run():

    cell_num = 10
    x_size = 500
    y_size = 500
    z_size = 500
    
    nml_doc = NeuroMLDocument(id="Net3DExample")

    syn0 = ExpOneSynapse(id="syn0", gbase="65nS", erev="0mV", tau_decay="3ms")
    nml_doc.exp_one_synapses.append(syn0)
    
    net = Network(id="Net3D")
    nml_doc.networks.append(net)

    
    for cell_id in range(0,cell_num):

        cell = Cell(id="Cell_%i"%cell_id)

        cell.morphology = generateRandomMorphology()
        
        nml_doc.cells.append(cell)

        pop = Population(id="Pop_%i"%cell_id, component=cell.id, type="populationList")
        net.populations.append(pop)

        inst = Instance(id="0")
        pop.instances.append(inst)

        inst.location = Location(x=str(x_size*random()), y=str(y_size*random()), z=str(z_size*random()))
    
        prob_connection = 0.5
    
        for post in range(0,cell_num):
            if post is not cell_id and random() <= prob_connection:
                net.synaptic_connections.append(SynapticConnection(from_="%s[%i]"%("Pop_%i"%cell_id,0), synapse=syn0.id, to="%s[%i]"%("Pop_%i"%post,0)))
        
    
    #######   Write to file  ######    
 
    fn = 'tmp/net3d.nml'
    writers.NeuroMLWriter.write(nml_doc, fn)
    
    print("Written network file to: "+fn)


    ###### Validate the NeuroML ######    

    from lxml import etree
    from urllib import urlopen
    schema_file = urlopen("https://raw.github.com/NeuroML/NeuroML2/master/Schemas/NeuroML2/NeuroML_v2beta.xsd")
    xmlschema = etree.XMLSchema(etree.parse(schema_file))
    print "Validating %s against %s" %(fn, schema_file.geturl())
    xmlschema.assertValid(etree.parse(fn))
    print "It's valid!"

run()
