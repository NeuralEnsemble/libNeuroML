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

def _node_to_python(node,rename_attributes,rename_elements,rename_values):

    tag = node.tag

    if rename_elements:
        tag = xml_case_convert.remove_curlies(tag)
        tag = tag[0].capitalize()+tag[-len(tag)+1:]
        node.tag = tag
    
    new_attributes = {}
    for attribute in node.attrib:
        value = node.attrib.pop(attribute)
        if attribute in rename_values:
            value = value[0].capitalize()+value[-len(value)+1:]
        renamed_attribute = xml_case_convert.remove_curlies(attribute)
        renamed_attribute = xml_case_convert.to_lowercase_with_underscores(attribute)
        new_attributes[renamed_attribute] = value
    
    for attribute in new_attributes:
        new_attribute = new_attributes[attribute]
        node.set(attribute,new_attribute)

#INCOMPLETE
def _node_to_neuroml(node,rename_attributes,rename_elements,rename_values):

    tag = node.tag

    if rename_elements:
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

def rename_doc(queue,rename,rename_attributes,rename_elements,rename_values):
    """Traverse the nodes of a tree in breadth-first order.
    The first argument should be the tree root; children
    should be a function taking as argument a tree node and
    returning an iterator of the node's children.
    """
    if len(queue) > 0:
        node = queue.pop()
        children = node.getchildren()
        rename(node,rename_attributes,rename_elements,rename_values)
        queue = queue + children
        rename_doc(queue,rename,
                   rename_attributes,
                   rename_elements,
                   rename_values)
    else:
        return None

def rename_file(filename,new_file,to_format,
                rename_elements=False,
                rename_attributes=False,
                rename_values=False):

    doc = objectify.parse(filename)
    root = doc.getroot()
    queue = [root]

    if to_format == 'python':
        rename = _node_to_python
    if to_format == 'neuroml':
        rename = _node_to_neuroml
        
    rename_doc(queue,rename,
               rename_attributes=rename_attributes,
               rename_elements=rename_elements,
               rename_values=rename_values)

    if new_file == None: new_file = filename+'tmp'
    
    doc.write(new_file,
              pretty_print=True,
              xml_declaration=True,
              encoding='UTF-8')

def convert_xsd(input_file,output_file):
    """
    Still highly experimental, idea is to get the neuroml xsd and convert
    the naming convention such that all the classes are pythonically named.
    """
    rename_file(fn,to_file,'python',
                rename_attributes=False,
                rename_elements=False,
                rename_values=['name','ref'])
