#
#
#   A class to handle XML based NeuroML files.
#   Calls the appropriate methods in DefaultNetworkHandler when cell locations,
#   network connections are found. The NetworkHandler can either print 
#   information, or if it's a class overriding NetworkHandler can create
#   the appropriate network in a simulator dependent fashion
#
#
#   Author: Padraig Gleeson
#
#
  
import logging

class NeuroMLXMLParser():
    
  log = logging.getLogger("NeuroMLXMLParser")
  
  currPopulation = ""
  currentComponent = ""
  totalInstances = 0
  
  currentProjectionId = ""
  currentProjectionPrePop = ""
  currentProjectionPostPop = ""
  currentSynapse = ""
       
    
  def __init__ (self, netHandler): 
    
    self.netHandler = netHandler
    

  def parse(self, filename):
    
    print("Parsing: %s"%filename)

    import neuroml.loaders as loaders
    self.nml_doc = loaders.NeuroMLLoader.load(filename)
    print("Loaded: %s as NeuroMLDocument"%filename)
    
    
    self.netHandler.handleDocumentStart(self.nml_doc.id,self.nml_doc.notes)  
    
    for network in self.nml_doc.networks:
        
        self.netHandler.handleNetwork(network.id,network.notes)
        
        for population in network.populations:
            
            if len(population.instances)>0:
                self.netHandler.handlePopulation(population.id, population.component, len(population.instances))
                for inst in population.instances:
                    
                    loc = inst.location
                    self.netHandler.handleLocation(inst.id,                      \
                                            population.id,     \
                                            population.component,    \
                                            loc.x,       \
                                            loc.y,       \
                                            loc.z)       \
    
        
        
if __name__ == '__main__':


    file_name = '../examples/tmp/testh5.nml'

    logging.basicConfig(level=logging.DEBUG, format="%(name)-19s %(levelname)-5s - %(message)s")

    from neuroml.hdf5.DefaultNetworkHandler import DefaultNetworkHandler

    nmlHandler = DefaultNetworkHandler()     

    currParser = NeuroMLXMLParser(nmlHandler) # The HDF5 handler knows of the structure of NetworkML and calls appropriate functions in NetworkHandler

    currParser.parse(file_name)
    
    print('-------------------------------\n\n')
    
    from neuroml.hdf5.NetworkBuilder import NetworkBuilder

    nmlHandler = NetworkBuilder()   

    currParser = NeuroMLXMLParser(nmlHandler) 
    
    currParser.parse(file_name)
    
    
    nml_doc = nmlHandler.get_nml_doc()

    nml_file = '../examples/tmp/testh5_2_.nml'
    import neuroml.writers as writers
    writers.NeuroMLWriter.write(nml_doc, nml_file)
    print("Written network file to: "+nml_file)

        
        
        
        
        
    