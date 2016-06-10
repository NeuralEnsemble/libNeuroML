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


import tables   # pytables for HDF5 support

class NeuroMLHdf5Parser():
    
  log = logging.getLogger("NeuroMLHdf5Parser")
  
  currPopulation = ""
  currentComponent = ""
  totalInstances = 0
  
  currentProjectionId = ""
  currentProjectionPrePop = ""
  currentProjectionPostPop = ""
  currentSynapse = ""
  
  currInputList = ""
       
    
  def __init__ (self, netHandler): 
    self.netHandler = netHandler
    
    
  def parse(self, filename):
    h5file=tables.openFile(filename)
    
    self.log.debug("Opened HDF5 file: "+ h5file.filename)  
    
    self.parseGroup(h5file.root.neuroml)
    
    h5file.close()
    
    
    
  def parseGroup(self, g):
    self.log.debug("Parsing group: "+ str(g))
    
    self.startGroup(g)
    
    # Note this ensures groups are parsed before datasets. Important for synapse props
    
    # Ensure populations parsed first!
    for node in g:
      
        if node._c_classId == 'GROUP' and node._v_name.count('population_')>=1:
            self.log.debug("Sub node: "+ str(node)+ ", class: "+ node._c_classId)
            self.parseGroup(node)
          
    # Non populations!
    for node in g:
      
        if node._c_classId == 'GROUP' and node._v_name.count('population_')==0:
            self.log.debug("Sub node (ng): "+ str(node)+ ", class: "+ node._c_classId)
            self.parseGroup(node)
          
    for node in g:
        self.log.debug("Sub node: "+ str(node)+ ", class: "+ node._c_classId)
      
        if node._c_classId == 'ARRAY':
            self.parseDataset(node)
          
    self.endGroup(g)
    
    
  def parseDataset(self, d):
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
        weight = 1
        delay = 1
        
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
            
        self.netHandler.handleProjection(self.currentProjectionId,
                                         self.currentProjectionPrePop,
                                         self.currentProjectionPostPop,
                                         self.currentSynapse,
                                         hasWeights=indexWeight>0, 
                                         hasDelays=indexDelay>0)
                
        
        self.log.debug("Cols: Id: %d precell: %d, postcell: %d, pre fract: %d, post fract: %d" % (indexId, indexPreCellId, indexPostCellId, indexPreFractAlong, indexPostFractAlong))
        
        self.log.debug("Extra cols: "+str(extraParamIndices) )
        #print d[5,:]
        
        
        for i in range(0, d.shape[0]):
            row = d[i,:]
            '''
            localSynapseProps = {}
            synTypes = self.globalSynapseProps.keys()
            for synType in synTypes:
                localSynapseProps[synType] = self.globalSynapseProps[synType].copy()'''
            
            id =  int(row[indexId])
            
            preCellId =  row[indexPreCellId]
            
            if indexPreSegId >= 0:
              preSegId = int(row[indexPreSegId])
            if indexPreFractAlong >= 0:
              preFractAlong = row[indexPreFractAlong]
            
            postCellId =  row[indexPostCellId]
            
            if indexPostSegId >= 0:
              postSegId = int(row[indexPostSegId])
            if indexPostFractAlong >= 0:
              postFractAlong = row[indexPostFractAlong]
              
              
            if indexWeight >= 0:
              weight = row[indexWeight]
              
            if indexDelay >= 0:
              delay = row[indexDelay]

            '''
            if len(extraParamIndices)>0:
                for synType in localSynapseProps:
                   for paramName in extraParamIndices.keys():
                     if paramName.count(synType)>0:
                       self.log.debug(paramName +"->"+synType)
                       if paramName.count('weight')>0:
                          localSynapseProps[synType].weight = row[extraParamIndices[paramName]]
                       if paramName.count('internal_delay')>0:
                          localSynapseProps[synType].internalDelay = row[extraParamIndices[paramName]]
                       if paramName.count('pre_delay')>0:
                          localSynapseProps[synType].preDelay = row[extraParamIndices[paramName]]
                       if paramName.count('post_delay')>0:
                          localSynapseProps[synType].postDelay = row[extraParamIndices[paramName]]
                       if paramName.count('prop_delay')>0:
                          localSynapseProps[synType].propDelay = row[extraParamIndices[paramName]]
                       if paramName.count('threshold')>0:
                          localSynapseProps[synType].threshold = row[extraParamIndices[paramName]]'''
               
            
            
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
        
        for i in range(0, d.shape[0]):

            self.netHandler.handleSingleInput(self.currInputList,
                                        int(d[i,0]),         
                                        float(d[i,1]))       
    
    
  def startGroup(self, g):
    self.log.debug("Going into a group: "+ g._v_name)
    
    
    if g._v_name == 'neuroml':
    
        self.netHandler.handleDocumentStart(g._v_attrs.id,g._v_attrs.notes)  
    
    if g._v_name == 'network':
        
        self.netHandler.handleNetwork(g._v_attrs.id,g._v_attrs.notes)
    
    if g._v_name.count('population_')>=1:
        # TODO: a better check to see if the attribute is a str or numpy.ndarray
        self.currPopulation = g._v_attrs.id[0]
        if (len(self.currPopulation)==1):          # i.e. it was a str and just took the first letter...
          self.currPopulation = g._v_attrs.id
        self.currentComponent = g._v_attrs.component[0]
        if (len(self.currentComponent)==1):
          self.currentComponent = g._v_attrs.component
        
        size = -1
        # Peek ahead for size...
        for node in g:
            if node._c_classId == 'ARRAY' and node.name == self.currPopulation:
              size = node.shape[0]
              
        if size == -1:
            size = g._v_attrs.size
              
        self.log.debug("Found a population: "+ self.currPopulation+", component: "+self.currentComponent+", size: "+ str(size))
        
        self.netHandler.handlePopulation(self.currPopulation, self.currentComponent, size)
        
    if g._v_name.count('projection_')>=1:
      
        self.currentProjectionId = g._v_attrs.id
        self.currentProjectionPrePop = g._v_attrs.presynapticPopulation
        self.currentProjectionPostPop = g._v_attrs.postsynapticPopulation
        self.currentSynapse = g._v_attrs.synapse
          
        self.log.debug("------    Found a projection: "+ self.currentProjectionId+ ", from "+ self.currentProjectionPrePop
        +" to "+ self.currentProjectionPostPop+" through "+self.currentSynapse)
        
    
    if g._v_name.count('input_list_')>=1:
        # TODO: a better check to see if the attribute is a str or numpy.ndarray
        self.currInputList = g._v_attrs.id
        component = g._v_attrs.component
        population = g._v_attrs.population
        
        size = -1
        # Peek ahead for size...
        for node in g:
            if node._c_classId == 'ARRAY' and node.name == self.currInputList:
              size = node.shape[0]
              
        if size == -1:
            size = g._v_attrs.size
              
        self.log.debug("Found an inputList: "+ self.currInputList+", component: "+component+", population: "+population+", size: "+ str(size))
        
        self.netHandler.handleInputList(self.currInputList, population, component, size)
    
    
    
  def endGroup(self, g):
    self.log.debug("Coming out of a group: "+ str(g))
  
    if g._v_name.count('population_')>=1:
        self.log.debug("End of population: "+ self.currPopulation+", cell type: "+self.currentComponent)  
        self.currPopulation =""
        self.currentComponent = ""
    
    if g._v_name.count('projection_')>=1:
        self.netHandler.finaliseProjection(self.currentProjectionId, self.currentProjectionPrePop, self.currentProjectionPostPop)
        self.currentProjectionId = ""
        self.currentProjectionPrePop = ""
        self.currentProjectionPostPop = ""
        self.currentSynapse = ""
        
    if g._v_name.count('input_list_')>=1:
        self.currInputList =""
    
    

        
        
        
if __name__ == '__main__':


    file_name = '../examples/tmp/testh5.nml.h5'

    logging.basicConfig(level=logging.DEBUG, format="%(name)-19s %(levelname)-5s - %(message)s")

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

        
        
        
        
        
    