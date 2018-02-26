"""

Example to build an NML2 file with many (all?) NeuroML elements, particularly for 
different network options

"""

from neuroml import NeuroMLDocument
from neuroml import IafCell
from neuroml import IzhikevichCell
from neuroml import Network
from neuroml import ExpOneSynapse
from neuroml import ExpTwoSynapse
from neuroml import Population
from neuroml import GapJunction

from neuroml import Input
from neuroml import InputW
from neuroml import InputList
from neuroml import ConnectionWD
from neuroml import Connection
from neuroml import Projection
from neuroml import ContinuousConnection
from neuroml import ContinuousConnectionInstance
from neuroml import ContinuousConnectionInstanceW
from neuroml import ContinuousProjection
from neuroml import SilentSynapse

from neuroml import GradedSynapse

from neuroml import ElectricalProjection
from neuroml import ElectricalConnection
from neuroml import ElectricalConnectionInstance
from neuroml import ElectricalConnectionInstanceW
from neuroml import Property
from neuroml import Instance
from neuroml import Location
from neuroml import PoissonFiringSynapse

import neuroml.writers as writers
import random

random.seed(123)

scale = 2

nml_doc = NeuroMLDocument(id="Complete")

nml_doc.notes = "Lots of notes...."

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

iz0 = IzhikevichCell(id="iz0", v0="-70mV", thresh="30mV", a="0.02", b="0.2", c="-65.0", d="6")

nml_doc.izhikevich_cells.append(iz0)

syn0 = ExpOneSynapse(id="syn0",
                     gbase="14nS",
                     erev="0mV",
                     tau_decay="3ms")

nml_doc.exp_one_synapses.append(syn0)

syn1 = ExpTwoSynapse(id="syn1",
                     gbase="2nS",
                     erev="0mV",
                     tau_rise="1ms",
                     tau_decay="3ms")

nml_doc.exp_two_synapses.append(syn1)


gj = GapJunction(id="gj1",conductance="10pS")

nml_doc.gap_junctions.append(gj)


sil_syn = SilentSynapse(id="silent1")
nml_doc.silent_synapses.append(sil_syn)


grad_syn = GradedSynapse(id="gs1",conductance="0.5pS",delta="5mV",Vth="-55mV",k="0.025per_ms",erev="0mV")
nml_doc.graded_synapses.append(grad_syn)

pfs = PoissonFiringSynapse(id='pfs',
                                   average_rate='150Hz',
                                   synapse=syn0.id, 
                                   spike_target="./%s"%syn0.id)

nml_doc.poisson_firing_synapses.append(pfs)

net = Network(id="CompleteNet", type="networkWithTemperature", temperature="6.3 degC")

net.notes = "Network notes..."

nml_doc.networks.append(net)

size0 = int(5*scale)
pop0 = Population(id="IafPop0",
                  component=IafCell0.id,
                  size=size0)

net.populations.append(pop0)

size1 = int(5*scale)
pop1 = Population(id="IafPop1",
                  component=IafCell1.id,
                  size=size1)

net.populations.append(pop1)


size2 = int(5*scale)
pop2 = Population(id="IzhPop",
                  component=iz0.id,
                  size=size2)

net.populations.append(pop2)


cell_num = int(4*scale)
pop = Population(id="Pop_x", component=IafCell0.id, type="populationList",size=cell_num)
net.populations.append(pop)
pop.properties.append(Property(tag="color", value="1 0 0"))

x_size = 500
y_size = 500
z_size = 500
    
for i in range(cell_num):
    inst = Instance(id=i)
    pop.instances.append(inst)

    inst.location = Location(x=str(x_size*random.random()), y=str(y_size*random.random()), z=str(z_size*random.random()))

prob_connection = 0.5
proj_count = 0


from_pop = pop.id
to_pop = pop.id
projection = Projection(id="Proj", presynaptic_population=from_pop, postsynaptic_population=to_pop, synapse=syn0.id)
electricalProjection = ElectricalProjection(id="ElectProj", presynaptic_population=from_pop, postsynaptic_population=to_pop)
electricalProjectionW = ElectricalProjection(id="ElectProjW", presynaptic_population=from_pop, postsynaptic_population=to_pop)

net.projections.append(projection)
net.electrical_projections.append(electricalProjection)
net.electrical_projections.append(electricalProjectionW)


input_list = InputList(id='il',
                     component=pfs.id,
                     populations=from_pop)

net.input_lists.append(input_list)

input_list_w = InputList(id='ilw',
                     component=pfs.id,
                     populations=from_pop)

net.input_lists.append(input_list_w)

for pre_index in range(0,cell_num):
    
    for post_index in range(0,cell_num):
        if pre_index != post_index and random.random() <= prob_connection:

            pre_seg_id = 0
            post_seg_id = 0

            connection = ConnectionWD(id=proj_count, \
                                    pre_cell_id="../%s/%i/%s"%(from_pop,pre_index,IafCell0.id), \
                                    pre_segment_id=pre_seg_id, \
                                    pre_fraction_along=random.random(),
                                    post_cell_id="../%s/%i/%s"%(to_pop,post_index,IafCell0.id), \
                                    post_segment_id=post_seg_id,
                                    post_fraction_along=random.random(),
                                    weight=random.random(),
                                    delay='%sms'%(random.random()*10))

            projection.connection_wds.append(connection)
            
            electricalConnection = ElectricalConnectionInstance(id=proj_count, \
                                    pre_cell="../%s/%i/%s"%(from_pop,pre_index,IafCell0.id), \
                                    pre_segment=pre_seg_id, \
                                    pre_fraction_along=random.random(),
                                    post_cell="../%s/%i/%s"%(to_pop,post_index,IafCell0.id), \
                                    post_segment=post_seg_id,
                                    post_fraction_along=random.random(), 
                                    synapse=gj.id)
                                    
            electricalProjection.electrical_connection_instances.append(electricalConnection)
            
            electricalConnectionW = ElectricalConnectionInstanceW(id=proj_count, \
                                    pre_cell="../%s/%i/%s"%(from_pop,pre_index,IafCell0.id), \
                                    pre_segment=pre_seg_id, \
                                    pre_fraction_along=random.random(),
                                    post_cell="../%s/%i/%s"%(to_pop,post_index,IafCell0.id), \
                                    post_segment=post_seg_id,
                                    post_fraction_along=random.random(), 
                                    synapse=gj.id, 
                                    weight=random.random())
                                    
            electricalProjectionW.electrical_connection_instance_ws.append(electricalConnectionW)
            
            proj_count += 1
            
    input = Input(id=pre_index, 
              target="../%s/%i/%s"%(from_pop, pre_index, pop.component), 
              destination="synapses")  
    input_list.input.append(input)  
            
    input_w = InputW(id=pre_index, 
              target="../%s/%i/%s"%(from_pop, pre_index, pop.component), 
              destination="synapses",
              weight=10)  
              
    input_list_w.input_ws.append(input_w)  
    

proj_count = 0

from_pop = pop0.id
to_pop = pop1.id
electricalProjection = ElectricalProjection(id="ElectProj0", presynaptic_population=from_pop, postsynaptic_population=to_pop)
net.electrical_projections.append(electricalProjection)

for pre_index in range(0,size0):
    
    for post_index in range(0,size1):
        if pre_index != post_index and random.random() <= prob_connection:

            pre_seg_id = 0
            post_seg_id = 0
            
            electricalConnection = ElectricalConnection(id=proj_count, \
                                    pre_cell="%s"%(pre_index), \
                                    pre_segment=pre_seg_id, \
                                    pre_fraction_along=random.random(),
                                    post_cell="%s"%(post_index), \
                                    post_segment=post_seg_id,
                                    post_fraction_along=random.random(), 
                                    synapse=gj.id)
                                    
            electricalProjection.electrical_connections.append(electricalConnection)
            
            proj_count += 1

projection0 = Projection(id="ProjEmpty", presynaptic_population=from_pop, postsynaptic_population=to_pop, synapse=syn0.id)

net.projections.append(projection0)


from_pop = pop0.id
to_pop = pop1.id

projection = Projection(id="ProjConnection", presynaptic_population=from_pop, postsynaptic_population=to_pop, synapse=syn1.id)
net.projections.append(projection)

connection = Connection(id=0, \
                        pre_cell_id="../%s[%i]"%(from_pop,size0-1), \
                        pre_segment_id=pre_seg_id, \
                        pre_fraction_along=random.random(),
                        post_cell_id="../%s[%i]"%(to_pop,size0-1), \
                        post_segment_id=post_seg_id,
                        post_fraction_along=random.random())

projection.connections.append(connection)


from_pop = pop0.id
to_pop = pop1.id

continuous_projection = ContinuousProjection(id="ProjCC", presynaptic_population=from_pop, postsynaptic_population=to_pop)
net.continuous_projections.append(continuous_projection)

continuous_connection = ContinuousConnection(id=0, \
                        pre_cell="0", \
                        post_cell="0", \
                        pre_component=sil_syn.id, \
                        post_component=grad_syn.id)

continuous_projection.continuous_connections.append(continuous_connection)

from_pop = pop.id
to_pop = pop1.id

continuous_projection_i = ContinuousProjection(id="ProjCCI", presynaptic_population=from_pop, postsynaptic_population=to_pop)
net.continuous_projections.append(continuous_projection_i)

continuous_connection_i = ContinuousConnectionInstance(id=0, \
                                    pre_cell="../%s/%i/%s"%(from_pop,0,pop.component), \
                                    pre_segment=pre_seg_id, \
                                    pre_fraction_along=random.random(),
                                    post_cell="../%s[%i]"%(to_pop,0), \
                                    post_segment=post_seg_id,
                                    post_fraction_along=random.random(), 
                                    pre_component=sil_syn.id, \
                                    post_component=grad_syn.id)

continuous_projection_i.continuous_connection_instances.append(continuous_connection_i)

continuous_projection_iw = ContinuousProjection(id="ProjCCIW", presynaptic_population=from_pop, postsynaptic_population=to_pop)
net.continuous_projections.append(continuous_projection_iw)

continuous_connection_iw = ContinuousConnectionInstanceW(id=0, \
                                    pre_cell="../%s/%i/%s"%(from_pop,0,pop.component), \
                                    pre_segment=pre_seg_id, \
                                    pre_fraction_along=random.random(),
                                    post_cell="../%s[%i]"%(to_pop,0), \
                                    post_segment=post_seg_id,
                                    post_fraction_along=random.random(), 
                                    pre_component=sil_syn.id, \
                                    post_component=grad_syn.id, \
                                    weight=5)

continuous_projection_iw.continuous_connection_instance_ws.append(continuous_connection_iw)


nml_file = 'test_files/complete.nml'
writers.NeuroMLWriter.write(nml_doc, nml_file)

summary0 = nml_doc.summary() 
print("Created:\n"+summary0)
print("Written network file to: "+nml_file)

###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)

nml_h5_file = 'test_files/complete.nml.h5'
writers.NeuroMLHdf5Writer.write(nml_doc, nml_h5_file)

print("Written H5 network file to: "+nml_h5_file)
