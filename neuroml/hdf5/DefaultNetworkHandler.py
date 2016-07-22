#
#
#   A class to handle events from the NeuroMLHdf5Parser, etc.
#   This should be overridden by simulator specific implementations.
#   Parsing classes, e.g. NetworkBuilder should call the appropriate
#   function here when a cell location, connection, etc. is encountered.
#
#   Use of this handler class should mean that the network setup is 
#   independent of the source of the network info (XML or HDF5 based NeuroML
#   files for example) and the instantiator of the network objects (NetManagerNEURON
#   or PyNN based setup class)
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council & Wellcome Trust
#
#


import logging


class DefaultNetworkHandler:
        
    log = logging.getLogger("DefaultNetworkHandler")
    
    isParallel = 0

    #
    #  Internal info method, can be reused in overriding classes for debugging
    #
    def printLocationInformation(self, id, population_id, component, x, y, z):
        position = "(%s, %s, %s)" % (x, y, z)
        self.log.debug("Location "+str(id)+" of population: "+population_id+", component: "+component+": "+position)
        

    #
    #  Internal info method, can be reused in overriding classes for debugging
    #        
    def printConnectionInformation(self,  projName, id, prePop, postPop, synapseType, preCellId, postCellId, weight):
        self.log.debug("Connection "+str(id)+" of: "+projName+": cell "+str(preCellId)+" in "+prePop \
                              +" -> cell "+str(postCellId)+" in "+postPop+", syn: "+ str(synapseType)+", weight: "+str(weight))
        
         
    #
    #  Internal info method, can be reused in overriding classes for debugging
    #        
    def printInputInformation(self, inputName, population_id, component, size=-1):
        sizeInfo = " size: "+ str(size)+ " cells"
        self.log.debug("Input Source: "+inputName+", on population: "+population_id+sizeInfo+" with component: "+ component)
        
    

    #
    #  Should be overridden
    #  
    def handleDocumentStart(self, id, notes):
            
        self.log.info("Document: "+id)
        if notes:
            self.log.info("  Notes: "+notes)

    #
    #  Should be overridden to create network
    #  
    def handleNetwork(self, network_id, notes):
            
        self.log.info("Network: "+network_id)
        if notes:
            self.log.info("  Notes: "+notes)

    #
    #  Should be overridden to create population array
    #  
    def handlePopulation(self, population_id, component, size=-1, component_obj=None):
      
        sizeInfo = " as yet unspecified size"
        if (size>=0):
            sizeInfo = " size: "+ str(size)+ " cells"
            
        self.log.info("Population: "+population_id+", component: "+component+sizeInfo)
        
        
    #
    #  Should be overridden to create specific cell instance
    #    
    def handleLocation(self, id, population_id, component, x, y, z):
        self.printLocationInformation(id, population_id, component, x, y, z)
        


    #
    #  Should be overridden to create population array
    #
    def handleProjection(self, projName, prePop, postPop, synapse, hasWeights=False, hasDelays=False):


        self.log.info("Projection: "+projName+" from "+prePop+" to "+postPop+" with syn: "+synapse)


    #
    #  Should be overridden to handle network connection
    #  
    def handleConnection(self, projName, id, prePop, postPop, synapseType, \
                                                    preCellId, \
                                                    postCellId, \
                                                    preSegId = 0, \
                                                    preFract = 0.5, \
                                                    postSegId = 0, \
                                                    postFract = 0.5, \
                                                    delay = 0, \
                                                    weight = 1):
        
        self.printConnectionInformation(projName, id, prePop, postPop, synapseType, preCellId, postCellId, weight)
        if preSegId != 0 or postSegId!=0 or preFract != 0.5 or postFract != 0.5:
            self.log.debug("Src cell: %d, seg: %f, fract: %f -> Tgt cell %d, seg: %f, fract: %f" % (preCellId,preSegId,preFract,postCellId,postSegId,postFract))
        
    #
    #  Should be overridden to handle end of network connection
    #  
    def finaliseProjection(self, projName, prePop, postPop):
   
        self.log.info("Projection: "+projName+" from "+prePop+" to "+postPop+" completed")
        
        
    #
    #  Should be overridden to create input source array
    #  
    def handleInputList(self, inputListId, population_id, component, size):
        self.printInputInformation(inputListId, population_id, component, size)
        
        if size<0:
            self.log.error("Error! Need a size attribute in sites element to create spike source!")
            return
             
        
    #
    #  Should be overridden to to connect each input to the target cell
    #  
    def handleSingleInput(self, inputListId, id, cellId, segId = 0, fract = 0.5):
        
        self.log.debug("Input: %s[%s], cellId: %i, seg: %i, fract: %f" % (inputListId,id,cellId,segId,fract))
        
        
    #
    #  Should be overridden to to connect each input to the target cell
    #  
    def finaliseInputSource(self, inputName):
        self.log.info("Input : %s completed" % inputName)
        
        

    #
    #  To signify network is distributed over parallel nodes
    #    
    def setParallelStatus(self, val):
        
        self.log.debug("Parallel status (0=serial mode, 1=parallel distributed): "+str(val))
        self.isParallel = val
        