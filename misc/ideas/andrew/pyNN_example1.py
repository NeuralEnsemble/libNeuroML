"""
Some ideas for syntax for multicompartmental modelling in PyNN

Andrew Davison, May 2012
"""

# Example 1
import pyNN.neuron as sim
from neuroml import load_morphology, load_lems, Section
from pyramidal.spatial_distributions import uniform, by_distance
from nineml.abstraction_layer.readers import XMLReader
from quantities import S, cm, um
from pyNN.space import Grid2D, RandomStructure, Sphere


pkj_morph = load_morphology("http://neuromorpho.org/...")  # smart inference of morphology file format

# support ion channel models defined in NineML, LEMS, or from built-in library
na_channel = XMLReader.read("na.xml")
kdr_channel = load_lems("kd.xml")
ka_channel = XMLReader.read("ka.xml")
ampa = XMLReader.read("ampa.xml")
gabaa = sim.ExpSynCond

# first we define cell types (templates)

# ... declarative style
purkinje_cell = sim.MultiCompartmentNeuron(
                    morphology=pkj_morph, 
                    ion_channels={'na': na_channel, 'kdr': kdr_channel, 'kA': kA_channel},
                    channel_distribution={'na': uniform('all', 0.1*S/cm**2),
                                          'kdr': by_distance(lambda d: 0.05*S/cm**2*d/200.0*um),
                                          'kA': uniform('soma', 0.02*S/cm**2)},
                    # need to specify cm, Ra (possibly with spatial variation) somewhere here
                    synapses={'AMPA': ampa, 'GABA_A': gabaa},
                    synapse_distribution={'AMPA': uniform('all', 0.5/um),
                                          'GABA_A': by_distance(lambda d: 0.5*(d<50.0)/um)}
)

# ... imperative style
gc_soma = Section(length=50, diam=10, label="soma")
gc_dend = Section(length=200, diam=2, label="dendrite")
gc_dend.connect(gc_soma)

granule_cell = sim.MultiCompartmentNeuron(morphology=soma.get_morphology(), cm=..., Ra=...)
granule_cell.soma.insert(na_channel, 0.05*S/cm**2)
granule_cell.soma.insert(kdr_channel, 0.01*S/cm**2)
granule_cell.dendrite.insert(gabaa, label="GABA_A")


# now we actually create the cells in the simulator
purkinje_cells = sim.Population(100, purkinje_cell, initial_values={'v': -60.0}, structure=Grid2D(…))
granule_cells = sim.Population(1000, granule_cell, structure=RandomStructure(boundary=Sphere(radius=300.0)))

# inject current into soma of Purkinje cells
noise = sim.NoisyCurrentSource(mean=0.0, stdev=0.5) # nA
noise.inject_into(purkinje_cells, section='soma')

# define which variables to record
(purkinje_cells + granule_cells).record('spikes')    # record spikes from all cells
granule_cells.sample(20).record('v')                 # record v from a sample of 20 granule cells
granule_cells[0:5].record('GABA_A.i', sections=['dendrite'])  # record the GABA_A synaptic current from the synapse
purkinje_cells[0].record('na.m', sections=longest_dendrite(pkj_morph)) # record the sodium channel m state variable along the length of one dendrite

# connect populations
depressing = sim.SynapseDynamics(fast=sim.TsodysMarkramMechanism(U=500.0))
p2g = sim.Projection(purkinje_cells, granule_cells,
                     method=sim.FixedProbabilityConnector(weights="0.1*exp(-d/100.0)", delays="0.2+d/100.0"),
                     source="soma.v", target="GABA_A", synapse_dynamics=depressing)
g2p = sim.Projection(granule_cells, purkinje_cells, method=sim.FromFileConnector("connections.h5"),
                     source="soma.v", target="AMPA")

sim.run(10000)

(purkinje_cells + granule_cells).write_data("output.h5")

sim.end()


# -------------------------------


# Example 2
from pyNN.neuroml import read
import pyNN.moose as sim

sim.setup()

network = read("complete_neuroml_model.xml")

network.populations["purkinje"].record('spikes')
network.populations["purkinje"].sample(10).record('v')

sim.run(1000.0)
data = network.get_data()

sim.end()
# -------------------------------