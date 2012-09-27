"""
This is currently an experimental module

Some example code (use own nml files):


>>> rename_elements('/home/mike/dev/libNeuroML/testFiles/NML2_FullCell.nml',
>>>                 '/home/mike/temp/pythonic.nml',
>>>                 to_format = 'python')
>>> 
>>> #now lets go back:
>>> 
>>> rename_elements('/home/mike/temp/pythonic.nml',
>>>                 '/home/mike/temp/neuromlic.nml',
>>>                 to_format = 'neuroml')

"""

import lxml
from lxml import objectify
import xml_case_convert

def _rename_to_python(node):
    tag = node.tag
    tag = xml_case_convert.remove_curlies(tag)
    tag = tag[0].capitalize()+tag[-len(tag)+1:]
    node.tag = tag
    
    new_attributes = {}
    for attribute in node.attrib:
        value = node.attrib.pop(attribute)
        renamed_attribute = xml_case_convert.remove_curlies(attribute)
        renamed_attribute = xml_case_convert.to_lowercase_with_underscores(attribute)
        new_attributes[renamed_attribute] = value
    
    for attribute in new_attributes:
        new_attribute = new_attributes[attribute]
        node.set(attribute,new_attribute)

def _rename_to_neuroml(node):
    tag = node.tag
    tag = xml_case_convert.remove_curlies(tag)
    tag = tag[0].lower()+tag[-len(tag)+1:]
    node.tag = tag
    
    new_attributes = {}
    for attribute in node.attrib:
        value = node.attrib.pop(attribute)
        renamed_attribute = xml_case_convert.remove_curlies(attribute)
        renamed_attribute = xml_case_convert.to_camelback(attribute)
        new_attributes[renamed_attribute] = value
    
    for attribute in new_attributes:
        new_attribute = new_attributes[attribute]
        node.set(attribute,new_attribute)

def rename_xml(queue,rename):
    """Traverse the nodes of a tree in breadth-first order.
    The first argument should be the tree root; children
    should be a function taking as argument a tree node and
    returning an iterator of the node's children.
    """
    if len(queue) > 0:
        node = queue.pop()
        children = node.getchildren()
        rename(node)
        queue = queue + children
        rename_xml(queue,rename)
    else:
        return None
    
def rename_elements(filename,new_file,to_format='python'):

    doc = objectify.parse(filename)
    root = doc.getroot()
    queue = [root]

    if to_format == 'python':
        rename = _rename_to_python
    if to_format == 'neuroml':
        rename = _rename_to_neuroml
        
    rename_xml(queue,rename)

    if new_file == None: new_file = filename+'tmp'
    
    doc.write(new_file,
              pretty_print=True,
              xml_declaration=True,
              encoding='UTF-8')
