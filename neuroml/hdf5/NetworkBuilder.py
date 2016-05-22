#
#
#   A class which stores the contents of a NeuroML file
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council
#
#

import sys
import logging


sys.path.append("../NeuroMLUtils")

from neuroml.hdf5.NetworkHandler import NetworkHandler

import neuroml


class NetworkBuilder(NetworkHandler):
    
    log = logging.getLogger("NetworkBuilder")
  
    nml_doc = neuroml.NeuroMLDocument()
    
    populations = {}
    
    
    def get_nml_doc(self):
        return self.nml_doc
    
    #
    #  Overridden from NetworkHandler
    #    
    def handleNetwork(self, network_id):
        
        self.network = neuroml.Network(id=network_id)
        self.nml_doc.networks.append(self.network)
   
    #
    #  Overridden from NetworkHandler
    #    
    def handlePopulation(self, population_id, component, size):
      
        pop = neuroml.Population(id=population_id, component=component, size=size)
        self.populations[population_id] = pop
        self.network.populations.append(pop)
        
        if (size>=0):
            sizeInfo = ", size "+ str(size)+ " cells"
            
            self.log.info("Creating population: "+population_id+", cell type: "+component+sizeInfo)
            
        else:
                
            self.log.error("Population: "+population_id+", cell type: "+component+" specifies no size. May lead to errors!")
        
  
    #
    #  Overridden from NetworkHandler
    #    
    def handleLocation(self, id, population_id, component, x, y, z):
        self.printLocationInformation(id, population_id, component, x, y, z)
        inst = neuroml.Instance(id=id)

        inst.location = neuroml.Location(x=x,y=y,z=z)
        self.populations[population_id].instances.append(inst)
          
    #
    #  Overridden from NetworkHandler
    #
    def handleProjection(self, projName, source, target, synapseTypes, size=-1):

        proj = self.nmlNet.addProjection(projName, source, target, size)

        sizeInfo = "as yet unspecified size"
        if (size>=0):
            sizeInfo = " size: "+ str(size)+ " connections"

        self.log.info("Projection: "+projName+" from "+source+" to "+target+" with syns: "+str(synapseTypes.keys())+" with "+sizeInfo)
     
        
    #
    #  Overridden from NetworkHandler
    #    
    def handleConnection(self, projName, id, source, target, synapseType, \
                                                    preCellId, \
                                                    postCellId, \
                                                    preSegId = 0, \
                                                    preFract = 0.5, \
                                                    postSegId = 0, \
                                                    postFract = 0.5, \
                                                    localInternalDelay = 0, \
                                                    localPreDelay = 0, \
                                                    localPostDelay = 0, \
                                                    localPropDelay = 0, \
                                                    localWeight = 1, \
                                                    localThreshold = 0):
        
        self.printConnectionInformation(projName, id, source, target, synapseType, preCellId, postCellId, localWeight)
          
        
        proj = self.nmlNet.getProjection(projName)
        if proj == None:
            proj = self.nmlNet.addProjection(projName, source, target)
            
            
        # NOTE: segment ID, fractalong, synapse props not supported yet in NetworkMLFile!!
        proj.addConnection(preCellId, postSegId)
        
        
