"""

Example to build a full spiking IaF network throught libNeuroML & save it as XML & validate it

"""

from neuroml import NeuroMLDocument
from neuroml import Network
from neuroml import ExpOneSynapse
from neuroml import Population
from neuroml import Annotation
from neuroml import Property
from neuroml import Cell
from neuroml import Location
from neuroml import Instance
from neuroml import Morphology
from neuroml import Point3DWithDiam
from neuroml import Segment
from neuroml import SegmentParent
from neuroml import Projection
from neuroml import Connection

import neuroml.writers as writers
from random import random

soma_diam = 10
soma_len = 10
dend_diam = 2
dend_len = 10
dend_num = 10

def generateRandomMorphology():

    morphology = Morphology()

    p = Point3DWithDiam(x=0,y=0,z=0,diameter=soma_diam)
    d = Point3DWithDiam(x=soma_len,y=0,z=0,diameter=soma_diam)
    soma = Segment(proximal=p, distal=d, name = 'Soma', id = 0)

    morphology.segments.append(soma)
    parent_seg = soma

    for dend_id in range(0,dend_num):

        p = Point3DWithDiam(x=d.x,y=d.y,z=d.z,diameter=dend_diam)
        d = Point3DWithDiam(x=p.x,y=p.y+dend_len,z=p.z,diameter=dend_diam)
        dend = Segment(proximal=p, distal=d, name = 'Dend_%i'%dend_id, id = 1+dend_id)
        dend.parent = SegmentParent(segments=parent_seg.id)
        parent_seg = dend

        morphology.segments.append(dend)

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

    
    proj_count = 0
    #conn_count = 0

    for cell_id in range(0,cell_num):

        cell = Cell(id="Cell_%i"%cell_id)

        cell.morphology = generateRandomMorphology()
        
        nml_doc.cells.append(cell)

        pop = Population(id="Pop_%i"%cell_id, component=cell.id, type="populationList")
        net.populations.append(pop)
        pop.properties.append(Property(tag="color", value="1 0 0"))

        inst = Instance(id="0")
        pop.instances.append(inst)

        inst.location = Location(x=str(x_size*random()), y=str(y_size*random()), z=str(z_size*random()))
    
        prob_connection = 0.5
        for post in range(0,cell_num):
            if post is not cell_id and random() <= prob_connection:

                from_pop = "Pop_%i"%cell_id
                to_pop = "Pop_%i"%post

                pre_seg_id = 0
                post_seg_id = 1
                

                projection = Projection(id="Proj_%i"%proj_count, presynaptic_population=from_pop, postsynaptic_population=to_pop, synapse=syn0.id)
                net.projections.append(projection)
                connection = Connection(id=proj_count, \
                                        pre_cell_id="%s[%i]"%(from_pop,0), \
                                        pre_segment_id=pre_seg_id, \
                                        pre_fraction_along=random(),
                                        post_cell_id="%s[%i]"%(to_pop,0), \
                                        post_segment_id=post_seg_id,
                                        post_fraction_along=random())

                projection.connections.append(connection)
                proj_count += 1
                #net.synaptic_connections.append(SynapticConnection(from_="%s[%i]"%(from_pop,0),  to="%s[%i]"%(to_pop,0)))
        
    
    #######   Write to file  ######    
 
    nml_file = 'tmp/net3d.nml'
    writers.NeuroMLWriter.write(nml_doc, nml_file)
    
    print("Written network file to: "+nml_file)


    ###### Validate the NeuroML ######    

    from neuroml.utils import validate_neuroml2

    validate_neuroml2(nml_file)

run()
