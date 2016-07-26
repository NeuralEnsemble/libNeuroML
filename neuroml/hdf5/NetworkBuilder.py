#
#
#   A class which stores the contents of a NeuroML file in libNeuroML classes
#   Used mainly to convert HDF5 representations of NeuroML to internal libNeuroML format
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council & Wellcome Trust
#
#

import sys
import logging

sys.path.append("../NeuroMLUtils")

from neuroml.hdf5.DefaultNetworkHandler import DefaultNetworkHandler

import neuroml


class NetworkBuilder(DefaultNetworkHandler):
    
    log = logging.getLogger("NetworkBuilder")
    
    populations = {}
    projections = {}
    input_lists = {}
    
    weightDelays = {}

    
    
    def get_nml_doc(self):
        return self.nml_doc
    
    #
    #  Overridden from DefaultNetworkHandler
    #    
    def handleDocumentStart(self, id, notes):
        self.nml_doc = neuroml.NeuroMLDocument(id=id)
        if notes and len(notes)>0:
            self.nml_doc.notes = notes
    
    #
    #  Overridden from DefaultNetworkHandler
    #    
    def handleNetwork(self, network_id, notes):
        
        self.network = neuroml.Network(id=network_id)
        self.nml_doc.networks.append(self.network)
        if notes and len(notes)>0:
            self.network.notes = notes
   
    #
    #  Overridden from DefaultNetworkHandler
    #    
    def handlePopulation(self, population_id, component, size, component_obj=None):
      
        pop = neuroml.Population(id=population_id, component=component, size=size)
        self.populations[population_id] = pop
        self.network.populations.append(pop)
        
        if (size>=0):
            sizeInfo = ", size "+ str(size)+ " cells"
            
            self.log.info("Creating population: "+population_id+", cell type: "+component+sizeInfo)
            
        else:
                
            self.log.error("Population: "+population_id+", cell type: "+component+" specifies no size. May lead to errors!")
        
  
    #
    #  Overridden from DefaultNetworkHandler
    #    
    def handleLocation(self, id, population_id, component, x, y, z):
        self.printLocationInformation(id, population_id, component, x, y, z)
        inst = neuroml.Instance(id=id)

        inst.location = neuroml.Location(x=x,y=y,z=z)
        self.populations[population_id].instances.append(inst)
        self.populations[population_id].type = 'populationList'
          
    #
    #  Overridden from DefaultNetworkHandler
    #
    def handleProjection(self, id, prePop, postPop, synapse, hasWeights=False, hasDelays=False):

        proj = neuroml.Projection(id=id, presynaptic_population=prePop, postsynaptic_population=postPop, synapse=synapse)
        self.projections[id] = proj
        self.network.projections.append(proj)
        self.weightDelays[id] = hasWeights or hasDelays

        self.log.info("Projection: %s from %s to %s with syn: %s, weights: %s, delays: %s"%(id, prePop, postPop, synapse, hasWeights, hasDelays))
     
        
    #
    #  Overridden from DefaultNetworkHandler
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
        
        #self.printConnectionInformation(proj_id, conn_id, prePop, postPop, synapseType, preCellId, postCellId, weight)
          
        if not self.weightDelays[proj_id] and delay==0 and weight==1:
            
            connection = neuroml.Connection(id=conn_id, \
                                pre_cell_id="../%s/%i/%s"%(prePop,preCellId,self.populations[prePop].component), \
                                pre_segment_id=preSegId, \
                                pre_fraction_along=preFract,
                                post_cell_id="../%s/%i/%s"%(postPop,postCellId,self.populations[postPop].component), \
                                post_segment_id=postSegId,
                                post_fraction_along=postFract)
                                
            self.projections[proj_id].connections.append(connection)
            
        else:
            connection = neuroml.ConnectionWD(id=conn_id, \
                                pre_cell_id="../%s/%i/%s"%(prePop,preCellId,self.populations[prePop].component), \
                                pre_segment_id=preSegId, \
                                pre_fraction_along=preFract,
                                post_cell_id="../%s/%i/%s"%(postPop,postCellId,self.populations[postPop].component), \
                                post_segment_id=postSegId,
                                post_fraction_along=postFract,
                                weight=weight,
                                delay='%sms'%(delay*1000.0))

            self.projections[proj_id].connection_wds.append(connection)
        
         
    #
    #  Overridden from DefaultNetworkHandler
    # 
    def handleInputList(self, inputListId, population_id, component, size):

        input_list = neuroml.InputList(id=inputListId,
                             component=component,
                             populations=population_id)
                             
        self.input_lists[inputListId]=input_list
        
        self.network.input_lists.append(input_list)
        
    #
    #  Overridden from DefaultNetworkHandler
    # 
    def handleSingleInput(self, inputListId, id, cellId, segId = 0, fract = 0.5):

        input_list = self.input_lists[inputListId]
        input = neuroml.Input(id=id, 
                  target="../%s/%i/%s"%(input_list.populations, cellId, self.populations[input_list.populations].component), 
                  destination="synapses")  
        if segId!=0:
            input.segment_id="%s"%(segId)
        if fract!=0.5:
            input.fraction_along="%s"%(fract)
        input_list.input.append(input)