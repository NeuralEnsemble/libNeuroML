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
    projection_syns = {}
    projection_syns_pre = {}
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
    def handleNetwork(self, network_id, notes, temperature=None):
        
        self.network = neuroml.Network(id=network_id)
        self.nml_doc.networks.append(self.network)
        if notes and len(notes)>0:
            self.network.notes = notes
        if temperature:
            self.network.temperature = temperature
            self.network.type = "networkWithTemperature"
   
    #
    #  Overridden from DefaultNetworkHandler
    #    
    def handlePopulation(self, population_id, component, size, component_obj=None):
      
        if component_obj:
            self.nml_doc.append(component_obj)
        
        pop = neuroml.Population(id=population_id, component=component, size=size)
        self.populations[population_id] = pop
        self.network.populations.append(pop)
        
        comp_obj_info = ' (%s)'%type(component_obj) if component_obj else ''
        
        if (size>=0):
            sizeInfo = ", size "+ str(size)+ " cells" 
            self.log.debug("Creating population: "+population_id+", cell type: "+component+comp_obj_info+sizeInfo)
        else:
            self.log.error("Population: "+population_id+", cell type: "+component+comp_obj_info+" specifies no size. May lead to errors!")
        
  
    #
    #  Overridden from DefaultNetworkHandler
    #    
    def handleLocation(self, id, population_id, component, x, y, z):
        self.printLocationInformation(id, population_id, component, x, y, z)
        
        if x and y and z:
            inst = neuroml.Instance(id=id)

            inst.location = neuroml.Location(x=x,y=y,z=z)
            self.populations[population_id].instances.append(inst)
            self.populations[population_id].type = 'populationList'
          
    #
    #  Overridden from DefaultNetworkHandler
    #
    def handleProjection(self, id, prePop, postPop, synapse, hasWeights=False, hasDelays=False, type="projection", synapse_obj=None, pre_synapse_obj=None):
        
        if synapse_obj:
            self.nml_doc.append(synapse_obj)
        if pre_synapse_obj:
            self.nml_doc.append(pre_synapse_obj)
            
        proj = None
        
        if type=="projection":
            proj = neuroml.Projection(id=id, presynaptic_population=prePop, postsynaptic_population=postPop, synapse=synapse)
            self.network.projections.append(proj)
        elif type=="electricalProjection":
            proj = neuroml.ElectricalProjection(id=id, presynaptic_population=prePop, postsynaptic_population=postPop)
            self.network.electrical_projections.append(proj)
            self.projection_syns[id] = synapse
        elif type=="continuousProjection":
            proj = neuroml.ContinuousProjection(id=id, presynaptic_population=prePop, postsynaptic_population=postPop)
            self.network.continuous_projections.append(proj)
            self.projection_syns[id] = synapse_obj.id
            self.projection_syns_pre[id] = pre_synapse_obj.id
            
        self.projections[id] = proj
        self.weightDelays[id] = hasWeights or hasDelays

        self.log.debug("Projection: %s (%s) from %s to %s with syn: %s, weights: %s, delays: %s"%(id, type, prePop, postPop, synapse, hasWeights, hasDelays))
     
    #
    #  Overridden from DefaultNetworkHandler
    #
    def finaliseProjection(self, id, prePop, postPop, synapse=None, type="projection"):
        '''
            Check whether handleProjection was not called, e.g. due to no connections present
        '''
        self.log.info("Projection: %s from %s to %s completed"%(id,prePop,postPop))
        if type=="projection":
            present = False
            for p in self.network.projections:
                if p.id==id: present=True
            if not present:
                proj = neuroml.Projection(id=id, presynaptic_population=prePop, postsynaptic_population=postPop, synapse=synapse)
                self.network.projections.append(proj)
        elif type=="electricalProjection":
            present = False
            for p in self.network.electrical_projections:
                if p.id==id: present=True
            if not present:
                proj = neuroml.ElectricalProjection(id=id, presynaptic_population=prePop, postsynaptic_population=postPop)
                self.network.electrical_projections.append(proj)
        
    #
    #  Overridden from DefaultNetworkHandler
    #
    #  Assumes delay in ms
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
        
        if isinstance(self.projections[proj_id], neuroml.ElectricalProjection):
            
            instances = False
            if len(self.populations[prePop].instances)>0 or len(self.populations[postPop].instances)>0:
                instances = True
                
            if not instances:
                conn = neuroml.ElectricalConnection(id=conn_id, \
                                    pre_cell="%s"%(preCellId), \
                                    pre_segment=preSegId, \
                                    pre_fraction_along=preFract,
                                    post_cell="%s"%(postCellId), \
                                    post_segment=postSegId,
                                    post_fraction_along=postFract,
                                    synapse=self.projection_syns[proj_id])
                                    
                self.projections[proj_id].electrical_connections.append(conn)
                
            else:
                conn = neuroml.ElectricalConnectionInstance(id=conn_id, \
                                    pre_cell="../%s/%i/%s"%(prePop,preCellId,self.populations[prePop].component), \
                                    pre_segment=preSegId, \
                                    pre_fraction_along=preFract,
                                    post_cell="../%s/%i/%s"%(postPop,postCellId,self.populations[postPop].component), \
                                    post_segment=postSegId,
                                    post_fraction_along=postFract,
                                    synapse=self.projection_syns[proj_id])

                self.projections[proj_id].electrical_connection_instances.append(conn)
                
        elif isinstance(self.projections[proj_id], neuroml.ContinuousProjection):
            
            instances = False
            if len(self.populations[prePop].instances)>0 or len(self.populations[postPop].instances)>0:
                instances = True
                
            if not instances:
                conn = neuroml.ContinuousConnection(id=conn_id, \
                                    pre_cell="%s"%(preCellId), \
                                    pre_segment=preSegId, \
                                    pre_fraction_along=preFract,
                                    post_cell="%s"%(postCellId), \
                                    post_segment=postSegId,
                                    post_fraction_along=postFract,
                                    pre_component=self.projection_syns_pre[proj_id],
                                    post_component=self.projection_syns[proj_id])
                                    
                self.projections[proj_id].continuous_connections.append(conn)
                
            else:
                conn = neuroml.ContinuousConnectionInstance(id=conn_id, \
                                    pre_cell="../%s/%i/%s"%(prePop,preCellId,self.populations[prePop].component), \
                                    pre_segment=preSegId, \
                                    pre_fraction_along=preFract,
                                    post_cell="../%s/%i/%s"%(postPop,postCellId,self.populations[postPop].component), \
                                    post_segment=postSegId,
                                    post_fraction_along=postFract,
                                    pre_component=self.projection_syns_pre[proj_id],
                                    post_component=self.projection_syns[proj_id])

                self.projections[proj_id].continuous_connection_instances.append(conn)
        else:

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
                                    delay='%sms'%(delay))

                self.projections[proj_id].connection_wds.append(connection)

         
    #
    #  Overridden from DefaultNetworkHandler
    # 
    def handleInputList(self, inputListId, population_id, component, size, input_comp_obj=None):

        if input_comp_obj:
            self.nml_doc.append(input_comp_obj)
            
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