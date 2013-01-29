#Maps from neuroML element space (Key) to python object space (value)
#The class names are essnetially correct, the instance names need converting
#also attributes need fixing

import lxml
from lxml import objectify
import re

def remove_curlies(string):
    return re.sub("{.*}","",string)

def to_lowercase_with_underscores(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_camelback(string):
    string_list = list(string)
    i = 0
    for m in re.finditer('_', string):
        underscore_index = m.end()
        string_list[underscore_index - i] = string_list[underscore_index - i].capitalize()
        string_list.pop(underscore_index - (1 + i))
        i += 1
    string = ''.join(string_list)
    
    return str(string)

def traverse_doc(queue,rename):
    """Recursive function to traverse the nodes of a tree in 
    breadth-first order.

    The first argument should be the tree root; children
    should be a function taking as argument a tree node and
    returning an iterator of the node's children.
    """
    if len(queue) > 0:
        node = queue.pop()
        children = node.getchildren()
        rename(node)
        queue = queue + children
        traverse_doc(queue,rename)
    else:
        return None

def _node_to_python(node):

    tag = node.tag

    for attribute in node.attrib:
        nml_attribute = node.attrib.pop(attribute)
        print nml_attribute
        if nml_attribute[0].islower():
            print 'object detected'
            renamed_attribute = to_lowercase_with_underscores(nml_attribute)
            NameTable[nml_attribute] = renamed_attribute
   
filename = 'NeuroML_v2alpha.xsd'

doc = objectify.parse(filename)
root = doc.getroot()
queue = [root]

NameTable = {}

traverse_doc(queue,_node_to_python)

#filtering routine
disallowed_keywords = ['from']
for keyword in disallowed_keywords:
    try:
        NameTable.pop(keyword)
    except:
        pass

#
# Now we define the edge cases
#

#the following are edge cases (mainly where s's are needed): 
NameTable['cell'] = 'cells'
NameTable['segment'] = 'segments'
NameTable['segmentGroup'] = 'segment_groups'
