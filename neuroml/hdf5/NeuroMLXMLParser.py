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
    
  def _parse_delay(self, delay_string):
      if delay_string.endswith('ms'):
          return float(delay_string[:-2].strip())
      elif delay_string.endswith('s'):
          return float(delay_string[:-1].strip())*1000.0
      else:
          print("Can't parse string for delay: %s"%delay_string)
          exit(1)

  def parse(self, filename):
    
    print("Parsing: %s"%filename)

    import neuroml.loaders as loaders
    
    self.nml_doc = loaders.read_neuroml2_file(filename, 
                                              include_includes=True,
                                              already_included=[])
    
    print("Loaded: %s as NeuroMLDocument"%filename)
    
    self.netHandler.handleDocumentStart(self.nml_doc.id,self.nml_doc.notes)  
    
    for network in self.nml_doc.networks:
        
        self.netHandler.handleNetwork(network.id,network.notes, temperature=network.temperature)
        
        for population in network.populations:
            
            component_obj = self.nml_doc.get_by_id(population.component)
            
            if len(population.instances)>0 and population.type=='populationList':
                  
                self.netHandler.handlePopulation(population.id, 
                                                 population.component, 
                                                 len(population.instances),
                                                 component_obj=component_obj)

                for inst in population.instances:

                    loc = inst.location
                    self.netHandler.handleLocation(inst.id,                      \
                                            population.id,     \
                                            population.component,    \
                                            loc.x,       \
                                            loc.y,       \
                                            loc.z)       
            else:
                self.netHandler.handlePopulation(population.id, 
                                                 population.component, 
                                                 population.size,
                                                 component_obj=component_obj)
                                                     
                for i in range(population.size):
                    self.netHandler.handleLocation(i,                      \
                                            population.id,     \
                                            population.component,    \
                                            None,       \
                                            None,       \
                                            None)  
                                                
        for projection in network.projections:
            
            synapse_obj = self.nml_doc.get_by_id(projection.synapse)
            
            self.netHandler.handleProjection(projection.id,
                                            projection.presynaptic_population,
                                            projection.postsynaptic_population,
                                            projection.synapse,
                                            synapse_obj=synapse_obj)
                                            
            for connection in projection.connections:
                
                self.netHandler.handleConnection(projection.id, \
                                            connection.id, \
                                            projection.presynaptic_population,
                                            projection.postsynaptic_population,
                                            projection.synapse, \
                                            preCellId=connection.get_pre_cell_id(), \
                                            postCellId=connection.get_post_cell_id(), \
                                            preSegId=int(connection.pre_segment_id), \
                                            postSegId=int(connection.post_segment_id), \
                                            preFract=float(connection.pre_fraction_along), \
                                            postFract=float(connection.post_fraction_along), \
                                            delay=0,
                                            weight=1)
                                            
            for connection in projection.connection_wds:
                
                self.netHandler.handleConnection(projection.id, \
                                            connection.id, \
                                            projection.presynaptic_population,
                                            projection.postsynaptic_population,
                                            projection.synapse, \
                                            preCellId=connection.get_pre_cell_id(), \
                                            postCellId=connection.get_post_cell_id(), \
                                            preSegId=int(connection.pre_segment_id), \
                                            postSegId=int(connection.post_segment_id), \
                                            preFract=float(connection.pre_fraction_along), \
                                            postFract=float(connection.post_fraction_along), \
                                            delay=self._parse_delay(connection.delay),
                                            weight=float(connection.weight))
                                            
                                            
        for ep in network.electrical_projections:
            
            synapse = None
            
            for connection in ep.electrical_connections:
                if synapse != None and synapse != connection.synapse:
                    raise Exception("There are different synapses for connections inside: %s!"%ep)
                synapse = connection.synapse
            for connection in ep.electrical_connection_instances:
                if synapse != None and synapse != connection.synapse:
                    raise Exception("There are different synapses for connections inside: %s!"%ep)
                synapse = connection.synapse
            for connection in ep.electrical_connection_instance_ws:
                if synapse != None and synapse != connection.synapse:
                    raise Exception("There are different synapses for connections inside: %s!"%ep)
                synapse = connection.synapse
                
            synapse_obj = self.nml_doc.get_by_id(synapse)
                
            self.netHandler.handleProjection(ep.id,
                                            ep.presynaptic_population,
                                            ep.postsynaptic_population,
                                            synapse, 
                                            type="electricalProjection",
                                            synapse_obj=synapse_obj)
                                            
            for connection in ep.electrical_connections:
                
                self.netHandler.handleConnection(ep.id, \
                                            connection.id, \
                                            ep.presynaptic_population,
                                            ep.postsynaptic_population,
                                            connection.synapse, \
                                            preCellId=connection.get_pre_cell_id(), \
                                            postCellId=connection.get_post_cell_id(), \
                                            preSegId=int(connection.pre_segment), \
                                            postSegId=int(connection.post_segment), \
                                            preFract=float(connection.pre_fraction_along), \
                                            postFract=float(connection.post_fraction_along))
                                            
            for connection in ep.electrical_connection_instances:
                
                self.netHandler.handleConnection(ep.id, \
                                            connection.id, \
                                            ep.presynaptic_population,
                                            ep.postsynaptic_population,
                                            connection.synapse, \
                                            preCellId=connection.get_pre_cell_id(), \
                                            postCellId=connection.get_post_cell_id(), \
                                            preSegId=int(connection.pre_segment), \
                                            postSegId=int(connection.post_segment), \
                                            preFract=float(connection.pre_fraction_along), \
                                            postFract=float(connection.post_fraction_along))
                                            
            for connection in ep.electrical_connection_instance_ws:
                
                self.netHandler.handleConnection(ep.id, \
                                            connection.id, \
                                            ep.presynaptic_population,
                                            ep.postsynaptic_population,
                                            connection.synapse, \
                                            preCellId=connection.get_pre_cell_id(), \
                                            postCellId=connection.get_post_cell_id(), \
                                            preSegId=int(connection.pre_segment), \
                                            postSegId=int(connection.post_segment), \
                                            preFract=float(connection.pre_fraction_along), \
                                            postFract=float(connection.post_fraction_along),
                                            weight=connection.get_weight())
                                            
        for cp in network.continuous_projections:
            
            pre_comp = None
            post_comp = None
            
            for connection in cp.continuous_connections:
                if pre_comp != None and pre_comp != connection.pre_component:
                    raise Exception("There are different pre components for connections inside: %s!"%cp)
                pre_comp = connection.pre_component
                if post_comp != None and post_comp != connection.post_component:
                    raise Exception("There are different post components for connections inside: %s!"%cp)
                post_comp = connection.post_component
                
            for connection in cp.continuous_connection_instances:
                if pre_comp != None and pre_comp != connection.pre_component:
                    raise Exception("There are different pre components for connections inside: %s!"%cp)
                pre_comp = connection.pre_component
                if post_comp != None and post_comp != connection.post_component:
                    raise Exception("There are different post components for connections inside: %s!"%cp)
                post_comp = connection.post_component
                
            for connection in cp.continuous_connection_instance_ws:
                if pre_comp != None and pre_comp != connection.pre_component:
                    raise Exception("There are different pre components for connections inside: %s!"%cp)
                pre_comp = connection.pre_component
                if post_comp != None and post_comp != connection.post_component:
                    raise Exception("There are different post components for connections inside: %s!"%cp)
                post_comp = connection.post_component
                
            pre_obj = self.nml_doc.get_by_id(pre_comp)
            post_obj = self.nml_doc.get_by_id(post_comp)
            
            self.netHandler.handleProjection(cp.id,
                                            cp.presynaptic_population,
                                            cp.postsynaptic_population,
                                            synapse, 
                                            type="continuousProjection",
                                            pre_synapse_obj=pre_obj,
                                            synapse_obj=post_obj)
            
            for connection in cp.continuous_connections:
                
                self.netHandler.handleConnection(cp.id, \
                                            connection.id, \
                                            cp.presynaptic_population,
                                            cp.postsynaptic_population,
                                            synapseType=None, \
                                            preCellId=connection.get_pre_cell_id(), \
                                            postCellId=connection.get_post_cell_id(), \
                                            preSegId=int(connection.pre_segment), \
                                            postSegId=int(connection.post_segment), \
                                            preFract=float(connection.pre_fraction_along), \
                                            postFract=float(connection.post_fraction_along))
            
            for connection in cp.continuous_connection_instances:
                
                self.netHandler.handleConnection(cp.id, \
                                            connection.id, \
                                            cp.presynaptic_population,
                                            cp.postsynaptic_population,
                                            synapseType=None, \
                                            preCellId=connection.get_pre_cell_id(), \
                                            postCellId=connection.get_post_cell_id(), \
                                            preSegId=int(connection.pre_segment), \
                                            postSegId=int(connection.post_segment), \
                                            preFract=float(connection.pre_fraction_along), \
                                            postFract=float(connection.post_fraction_along))
            
            for connection in cp.continuous_connection_instance_ws:
                
                self.netHandler.handleConnection(cp.id, \
                                            connection.id, \
                                            cp.presynaptic_population,
                                            cp.postsynaptic_population,
                                            synapseType=None, \
                                            preCellId=connection.get_pre_cell_id(), \
                                            postCellId=connection.get_post_cell_id(), \
                                            preSegId=int(connection.pre_segment), \
                                            postSegId=int(connection.post_segment), \
                                            preFract=float(connection.pre_fraction_along), \
                                            postFract=float(connection.post_fraction_along),
                                            weight=connection.get_weight())
            
                                            
        for input_list in network.input_lists:   
            
            input_comp_obj = self.nml_doc.get_by_id(input_list.component)
                
            self.netHandler.handleInputList(input_list.id, input_list.populations, input_list.component, len(input_list.input),input_comp_obj=input_comp_obj)
            
            for input in input_list.input:
                
                self.netHandler.handleSingleInput(input_list.id, 
                                                  input.id, 
                                                  cellId = input.get_target_cell_id(), 
                                                  segId = input.get_segment_id(), 
                                                  fract = input.get_fraction_along())
            for input_w in input_list.input_ws:
                
                self.netHandler.handleSingleInput(input_list.id, 
                                                  input_w.id, 
                                                  cellId = input_w.get_target_cell_id(), 
                                                  segId = input_w.get_segment_id(), 
                                                  fract = input_w.get_fraction_along(),
                                                  weight = input_w.get_weight())
                                               
        for explicitInput in network.explicit_inputs:     
            list_name = 'INPUT_%s_%s'%(explicitInput.input,explicitInput.target.replace('[','_').replace(']','_'))
            pop = explicitInput.target.split('[')[0]
            self.netHandler.handleInputList(list_name, pop, explicitInput.input, 1)   

            self.netHandler.handleSingleInput(list_name, 
                                              0, 
                                              cellId = explicitInput.get_target_cell_id(), 
                                              segId = 0, 
                                              fract = 0.5)
    
        
        
if __name__ == '__main__':


    file_name = '../examples/tmp/testh5.nml'

    logging.basicConfig(level=logging.INFO, format="%(name)-19s %(levelname)-5s - %(message)s")

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
    
    print(nml_doc.summary())

    nml_file = '../examples/tmp/testh5_2_.nml'
    import neuroml.writers as writers
    writers.NeuroMLWriter.write(nml_doc, nml_file)
    print("Written network file to: "+nml_file)

        
        
        
        
        
    