===========================
HDF Examples already in use
===========================

Collecting all the HDF format already in use out there to have a better 
understanding how to uniform all of this in one true format. If you've got one, 
just add it to the list. Please keep the file small (<1 Mb) if possible, it 
should be just an example.

- neuroConstruct_NetworkMLv1.8.1.h5  _Padraig Gleeson_
  
  A version of NetworkML (cell positions & connections only, no 
  morphologies/channels) in HDF5 as can be saved/loaded in to 
  neuroConstruct at tab Generate

- neuroConstruct_simulationDataOnePop.h5  _Padraig Gleeson_
  
  Traces of membrane potentials from a single population/cell group, as saved 
  during a NEURON simulation. Option to save as HDF5 (as opposed to simple text 
  files) is enables by selecting "Save data as HDF5" at tab NEURON
  
- Neuronvisio_medium_cell_example_10ms.h5   _Michele Mattioni_

  Example of a Neuronvisio HDF file. The file is described in details in this 
  page: http://neuronvisio.org/storage.html#hdf-structure
  Quick pick: 
    - geometry branch --> NeuroML 1.8.1 (here only a cell, but 
      theoretically can hold anything NeuroML can keep)
    - results branch --> Numpy array arranged according section_name/var_name
  

 
