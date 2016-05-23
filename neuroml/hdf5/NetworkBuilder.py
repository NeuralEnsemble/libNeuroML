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
    
    populations = {}
    projections = {}
    
    
    def get_nml_doc(self):
        return self.nml_doc
    
    #
    #  Overridden from NetworkHandler
    #    
    def handleDocumentStart(self, id, notes):
        self.nml_doc = neuroml.NeuroMLDocument(id=id)
        if notes and len(notes)>0:
            self.nml_doc.notes = notes
    
    #
    #  Overridden from NetworkHandler
    #    
    def handleNetwork(self, network_id, notes):
        
        self.network = neuroml.Network(id=network_id)
        self.nml_doc.networks.append(self.network)
        if notes and len(notes)>0:
            self.network.notes = notes
   
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
        self.populations[population_id].type = 'populationList'
          
    #
    #  Overridden from NetworkHandler
    #
    def handleProjection(self, id, prePop, postPop, synapse):

        proj = neuroml.Projection(id=id, presynaptic_population=prePop, postsynaptic_population=postPop, synapse=synapse)
        self.projections[id] = proj
        self.network.projections.append(proj)


        self.log.info("Projection: "+id+" from "+prePop+" to "+postPop+" with syn: "+synapse)
     
        
    #
    #  Overridden from NetworkHandler
    #    
    def handleConnection(self, proj_id, conn_id, prePop, postPop, synapseType, \
                                                    preCellId, \
                                                    postCellId, \
                                                    preSegId = 0, \
                                                    preFract = 0.5, \
                                                    postSegId = 0, \
                                                    postFract = 0.5, \
                                                    delay=0,
                                                    weight=1):
        
        self.printConnectionInformation(proj_id, conn_id, prePop, postPop, synapseType, preCellId, postCellId, weight)
          


        connection = neuroml.Connection(id=conn_id, \
                                pre_cell_id="../%s/%i/%s"%(prePop,preCellId,self.populations[prePop].component), \
                                pre_segment_id=preSegId, \
                                pre_fraction_along=preFract,
                                post_cell_id="../%s/%i/%s"%(postPop,postCellId,self.populations[postPop].component), \
                                post_segment_id=postSegId,
                                post_fraction_along=postFract)

        self.projections[proj_id].connections.append(connection)
        
        
