#
# Hypothetical Example of libNeuroML API for setting up a model and running
# a simulation
#

from libNeuroML import morphology
from libNeuroML.currents import ionchannels
from libNeuroML.currents import patch
from libNeuroML import simulators

soma=morphology.Section(tag='Soma')
dend1=morphology.Section(tag='Apical1')
dend2=morphology.Section(tag='Proximal1')
dend3=morphology.Section(tag='Proximal2')
axon=morphology.Section(tag='Axon')

#Connect everything together
soma.connect(dend1)
soma.connect(dend2)
soma.connect(axon)

#Build a cell - pass any section to Cell constructor and 
#it will figure out all the sections belonging to the cell
#from their connectivity
testcell=morphology.Cell(soma) 

#work out some statistics of this morphology
num_term=testcell.num_terminations
num_sections=testcell.num_sections
area=testcell.area
volume=testcell.volume

#save this morphology to neuroML or neuroHDF format:
testcell.save_neroML('mymorphology.neuroML)
testcell.save_neuorHDF('mymorphology.neuroML)

#make a region, similar to a cell but requires sections
#to be added explicitly in an array
proximals=morphology.Region()
proximals.add([dend2,dend3])

#define a function which describes an ion channel's kinetics,
#this may be difficult/impossible to implement, but would be 
#nice..
def afunction(Vm):
    #do some maths here...#
    return current

#Make some ion channels objects in different ways
KV=ionchannels.hodgkinhuxley(afunction)
Na=ionchannels.fromfile('modfile.mod')
NaFast=ionchannels.fromfile('ChannelMLfile.nml') #channelML format

#Now insert the ion channels

testcell.insert(KV,200) #all the cell gets the same density of KV
axon.insert(NaFast,1000)#insert the fast sodium into the axon
proximal.insert(Na,300)#proximal dendrites get Na

#save again, this time with all the ion channel info:
testcell.save_neuroml('withionchans.nml')

#Now we want to set up an experiment
#make a current clamp object with 20pA injection from 200ms to 500ms
iclamp=patch.CurrentClamp(tstart=200,tstop=500,current=20)

#insert it into the soma
soma.insert(iclamp)

#set up the simulator
mysimulator=simulators.Neuron(min_timestep=0.05,timestep='fixed',min_seg_length=50)

#simulate
mysimulator.go()

#plot results
mysimulator.plot()

#save results in some format, to be decided
mysimulator.save_results('results.?')
