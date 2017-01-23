#
#
#   A class to parse HDF5 based NeuroML files.
#   Calls the appropriate methods in DefaultNetworkHandler when cell locations,
#   network connections are found. The DefaultNetworkHandler can either print 
#   information, or if it's a class overriding DefaultNetworkHandler can create
#   the appropriate network in a simulator dependent fashion
#
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council & Wellcome Trust
#
#
  
import logging
import sys
import numpy

import tables   # pytables for HDF5 support

from neuroml.nml.nml import parseString

from neuroml.loaders import read_neuroml2_string

class NeuroMLHdf5Parser():
    
  log = logging.getLogger("NeuroMLHdf5Parser")
  
  currPopulation = ""
  currentComponent = ""
  totalInstances = 0
  
  currentProjectionId = ""
  currentProjectionType = ""
  currentProjectionPrePop = ""
  currentProjectionPostPop = ""
  currentSynapse = ""
  
  currInputList = ""
        
  nml_doc_extra_elements = None
    
  def __init__ (self, netHandler): 
    self.netHandler = netHandler
    
    
  def get_str_attribute_group(self, group, name):
    if not hasattr(group._v_attrs,name):
          return None
      
    for attrName in group._v_attrs._v_attrnames:
        if attrName == name:
            val = group._v_attrs[name]
            
            if isinstance(val,numpy.ndarray):
                val = str(val[0])
            else:
                val = str(val)
            #print("- Found %s in %s: %s = [%s]"%(group, attrName, name,val))
            return val
    return None

    
  def parse(self, filename):
      
    h5file=tables.open_file(filename,mode='r')
    
    self.log.info("Opened HDF5 file: %s; id=%s"%(h5file.filename,h5file.root.neuroml._v_attrs.id))
    
    if hasattr(h5file.root.neuroml._v_attrs,"neuroml_top_level"):
        nml = self.get_str_attribute_group(h5file.root.neuroml,"neuroml_top_level")
        
        if sys.version_info[0] == 3:
            nml = nml.encode()
            
        self.nml_doc_extra_elements = read_neuroml2_string(nml, include_includes=True, verbose=False)
        
        #print(self.nml_doc_extra_elements.summary())
        
        self.log.info("Added NeuroML2 elements from extra string found in HDF5 file")
    
    self.parse_group(h5file.root.neuroml)
    
    h5file.close()
    
  def _is_dataset(self,node):
      return node._c_classid == 'ARRAY' or node._c_classid == 'CARRAY'
    
  def parse_group(self, g):
    self.log.debug("Parsing group: "+ str(g))
    
    self.start_group(g)
    
    # Note this ensures groups are parsed before datasets. Important for synapse props
    
    # Ensure populations parsed first!
    for node in g:
      
        if node._c_classid == 'GROUP' and node._v_name.count('population_')>=1:
            self.log.debug("Sub node: "+ str(node)+ ", class: "+ node._c_classid)
            self.parse_group(node)
          
    # Non populations!
    for node in g:
      
        if node._c_classid == 'GROUP' and node._v_name.count('population_')==0:
            self.log.debug("Sub node (ng): "+ str(node)+ ", class: "+ node._c_classid)
            self.parse_group(node)
          
    for node in g:
        self.log.debug("Sub node: "+ str(node)+ ", class: "+ node._c_classid)
      
        if self._is_dataset(node):
            self.parse_dataset(node)
          
    self.end_group(g)
    
    
  def parse_dataset(self, d):
    self.log.debug("Parsing dataset/array: "+ str(d))
    
    if self.currPopulation!="":
        self.log.debug("Using data for population: "+ self.currPopulation)
        self.log.debug("Size is: "+str(d.shape[0])+" rows of: "+ str(d.shape[1])+ " entries")
        
        for i in range(0, d.shape[0]):
            
                self.netHandler.handleLocation( int(d[i,0]),                      \
                                            self.currPopulation,     \
                                            self.currentComponent,    \
                                            float(d[i,1]),       \
                                            float(d[i,2]),       \
                                            float(d[i,3]))       \
            
      
    elif self.currentProjectionId!="":
        self.log.debug("Using data for proj: "+ self.currentProjectionId)
        self.log.debug("Size is: "+str(d.shape[0])+" rows of: "+ str(d.shape[1])+ " entries")
        

        indexId = -1
        indexPreCellId = -1
        indexPreSegId = -1
        indexPreFractAlong= -1
        indexPostCellId = -1
        indexPostSegId = -1
        indexPostFractAlong= -1
        indexWeight= -1
        indexDelay= -1
        
        id = -1
        preCellId = -1
        preSegId = 0
        preFractAlong= 0.5
        postCellId = -1
        postSegId = 0
        postFractAlong= 0.5
        
        type="projection"
        
        extraParamIndices = {}
        
        
        for attrName in d.attrs._v_attrnames:
            val = d.attrs.__getattr__(attrName)
            
            #self.log.debug("Val of attribute: "+ attrName + " is "+ str(val))
            
            if val == 'id' or val[0] == 'id':
                indexId = int(attrName[len('column_'):])
            elif val == 'pre_cell_id' or val[0] == 'pre_cell_id':
                indexPreCellId = int(attrName[len('column_'):])
            elif val == 'pre_segment_id' or val[0] == 'pre_segment_id':
                indexPreSegId = int(attrName[len('column_'):])
            elif val == 'pre_fraction_along' or val[0] == 'pre_fraction_along':
                indexPreFractAlong = int(attrName[len('column_'):])
            elif val == 'post_cell_id' or val[0] == 'post_cell_id':
                indexPostCellId = int(attrName[len('column_'):])
            elif val == 'post_segment_id' or val[0] == 'post_segment_id':
                indexPostSegId = int(attrName[len('column_'):])
            elif val == 'post_fraction_along' or val[0] == 'post_fraction_along':
                indexPostFractAlong = int(attrName[len('column_'):])
            elif val == 'weight' or val[0] == 'weight':
                indexWeight = int(attrName[len('column_'):])
            elif val == 'delay' or val[0] == 'delay':
                indexDelay = int(attrName[len('column_'):])
                
        if self.nml_doc_extra_elements:
            synapse_obj = self.nml_doc_extra_elements.get_by_id(self.currentSynapse)
        else:
            synapse_obj = None
        
            
        self.netHandler.handleProjection(self.currentProjectionId,
                                         self.currentProjectionPrePop,
                                         self.currentProjectionPostPop,
                                         self.currentSynapse,
                                         hasWeights=indexWeight>0, 
                                         hasDelays=indexDelay>0,
                                         type=self.currentProjectionType,
                                         synapse_obj = synapse_obj)
                
        
        self.log.debug("Cols: Id: %d precell: %d, postcell: %d, pre fract: %d, post fract: %d" % (indexId, indexPreCellId, indexPostCellId, indexPreFractAlong, indexPostFractAlong))
        
        self.log.debug("Extra cols: "+str(extraParamIndices) )
        
        
        for i in range(0, d.shape[0]):
            row = d[i,:]
            
            id =  int(row[indexId])
            
            preCellId =  int(row[indexPreCellId])
            
            if indexPreSegId >= 0:
              preSegId = int(row[indexPreSegId])
            if indexPreFractAlong >= 0:
              preFractAlong = row[indexPreFractAlong]
            
            postCellId =  int(row[indexPostCellId])
            
            if indexPostSegId >= 0:
              postSegId = int(row[indexPostSegId])
            if indexPostFractAlong >= 0:
              postFractAlong = row[indexPostFractAlong]
              
              
            if indexWeight >= 0:
                weight = row[indexWeight]
            else:
                weight=1
              
            if indexDelay >= 0:
                delay = row[indexDelay]
            else:
                delay = 0

            #self.log.debug("Connection %d from %f to %f" % (id, preCellId, postCellId))


            self.netHandler.handleConnection(self.currentProjectionId, \
                                            id, \
                                            self.currentProjectionPrePop, \
                                            self.currentProjectionPostPop, \
                                            self.currentSynapse, \
                                            preCellId, \
                                            postCellId, \
                                            preSegId, \
                                            preFractAlong, \
                                            postSegId, \
                                            postFractAlong,
                                            delay=delay,
                                            weight=weight)
                                            
    if self.currInputList!="":
        self.log.debug("Using data for input list: "+ self.currInputList)
        self.log.debug("Size is: "+str(d.shape[0])+" rows of: "+ str(d.shape[1])+ " entries")
        
        
        indexId = -1
        indexTargetCellId = -1
        indexSegId = -1
        indexFractAlong= -1
        
        segId = 0
        fractAlong= 0.5
        
        
        for attrName in d.attrs._v_attrnames:
            val = d.attrs.__getattr__(attrName)
            
            self.log.debug("Val of attribute: "+ attrName + " is "+ str(val))
            
            if val == 'id' or val[0] == 'id':
                indexId = int(attrName[len('column_'):])
            elif val == 'target_cell_id' or val[0] == 'target_cell_id':
                indexTargetCellId = int(attrName[len('column_'):])
            elif val == 'segment_id' or val[0] == 'segment_id':
                indexSegId = int(attrName[len('column_'):])
            elif val == 'fraction_along' or val[0] == 'fraction_along':
                indexFractAlong = int(attrName[len('column_'):])
        
        for i in range(0, d.shape[0]):
            
            if indexId >= 0:
                id_ = int(d[i,indexId])
            else:
                id_ = i
            
            tid = int(d[i,indexTargetCellId])
            
            if indexSegId >= 0:
              segId = int(d[i,indexSegId])
            
            if indexFractAlong >= 0:
              fractAlong = float(d[i,indexFractAlong])
              
            self.log.debug("Adding %s, %s, %s"%(tid,segId,fractAlong))

            self.netHandler.handleSingleInput(self.currInputList,
                                        id_,
                                        tid,         
                                        segId = segId,         
                                        fract = fractAlong)       
    
  def _get_node_size(self, g, name):
      
        size = -1
        # Peek ahead for size...
        for node in g:
            if self._is_dataset(node) and node.name == name:
              size = node.shape[0]

        if size == -1:
            size = g._v_attrs.size
            
        return size
    
  def start_group(self, g):
    self.log.debug("Going into a group: "+ g._v_name)
    
    
    if g._v_name == 'neuroml':
    
        self.netHandler.handleDocumentStart(self.get_str_attribute_group(g,'id'),
                                            self.get_str_attribute_group(g,'notes'))  
    
    if g._v_name == 'network':
        
        self.netHandler.handleNetwork(self.get_str_attribute_group(g,'id'),
                                      self.get_str_attribute_group(g,'notes'),
                                      temperature=self.get_str_attribute_group(g,'temperature'))
    
    if g._v_name.count('population_')>=1:
        # TODO: a better check to see if the attribute is a str or numpy.ndarray
        self.currPopulation = g._v_attrs.id[0]
        if (len(self.currPopulation)==1):          # i.e. it was a str and just took the first letter...
          self.currPopulation = g._v_attrs.id
        self.currentComponent = g._v_attrs.component[0]
        if (len(self.currentComponent)==1):
          self.currentComponent = g._v_attrs.component
        
        size = self._get_node_size(g,self.currPopulation)
        
        if self.nml_doc_extra_elements:
            component_obj = self.nml_doc_extra_elements.get_by_id(self.currentComponent)
        else:
            component_obj = None
              
        self.log.debug("Found a population: "+ self.currPopulation+", component: "+self.currentComponent+", size: "+ str(size))
        
        self.netHandler.handlePopulation(self.currPopulation, self.currentComponent, size, component_obj=component_obj)
        
    if g._v_name.count('projection_')>=1:
      
        self.currentProjectionId = g._v_attrs.id
        self.currentProjectionType = g._v_attrs.type if g._v_attrs.type else "projection"
        self.currentProjectionPrePop = g._v_attrs.presynapticPopulation
        self.currentProjectionPostPop = g._v_attrs.postsynapticPopulation
        self.currentSynapse = g._v_attrs.synapse
          
        self.log.debug("------    Found a projection: "+ self.currentProjectionId+ ", from "+ self.currentProjectionPrePop
        +" to "+ self.currentProjectionPostPop+" through "+self.currentSynapse)
        
    
    if g._v_name.count('inputList_')>=1 or g._v_name.count('input_list_')>=1: # inputList_ preferred
        # TODO: a better check to see if the attribute is a str or numpy.ndarray
        self.currInputList = g._v_attrs.id
        component = g._v_attrs.component
        population = g._v_attrs.population
        
        size = self._get_node_size(g,self.currInputList)
        
        if self.nml_doc_extra_elements:
            input_comp_obj = self.nml_doc_extra_elements.get_by_id(component)
        else:
            input_comp_obj = None
              
        self.log.debug("Found an inputList: "+ self.currInputList+", component: "+component+", population: "+population+", size: "+ str(size))
        
        self.netHandler.handleInputList(self.currInputList, population, component, size, input_comp_obj=input_comp_obj)
    
    
  def end_group(self, g):
    self.log.debug("Coming out of a group: "+ str(g))
  
    if g._v_name.count('population_')>=1:
        self.log.debug("End of population: "+ self.currPopulation+", cell type: "+self.currentComponent)  
        self.currPopulation =""
        self.currentComponent = ""
    
    if g._v_name.count('projection_')>=1:
        self.netHandler.finaliseProjection(self.currentProjectionId, self.currentProjectionPrePop, self.currentProjectionPostPop)
        self.currentProjectionId = ""
        self.currentProjectionType = ""
        self.currentProjectionPrePop = ""
        self.currentProjectionPostPop = ""
        self.currentSynapse = ""
        
    if g._v_name.count('inputList_')>=1 or g._v_name.count('input_list_')>=1: 
        self.currInputList =""
    
    

    
        
if __name__ == '__main__':


    file_name = '../examples/tmp/testh5.nml.h5'

    logging.basicConfig(level=logging.INFO, format="%(name)-19s %(levelname)-5s - %(message)s")

    from neuroml.hdf5.DefaultNetworkHandler import DefaultNetworkHandler

    nmlHandler = DefaultNetworkHandler()   

    currParser = NeuroMLHdf5Parser(nmlHandler) # The HDF5 handler knows of the structure of NetworkML and calls appropriate functions in NetworkHandler

    currParser.parse(file_name)
    
    print('-------------------------------\n\n')
    
    from neuroml.hdf5.NetworkBuilder import NetworkBuilder

    nmlHandler = NetworkBuilder()   

    currParser = NeuroMLHdf5Parser(nmlHandler) 
    
    currParser.parse(file_name)
    
    nml_doc = nmlHandler.get_nml_doc()

    nml_file = '../examples/tmp/testh5__.nml'
    import neuroml.writers as writers
    writers.NeuroMLWriter.write(nml_doc, nml_file)
    print("Written network file to: "+nml_file)

        
        
        
        
        
    