"""

Utilities for checking generated code

"""
import os.path

import neuroml

def validate_neuroml2(file_name):

    from lxml import etree
    try:
        from urllib2 import urlopen  # Python 2
    except:
        from urllib.request import urlopen # Python 3
        
    xsd_file = os.path.join(os.path.dirname(__file__), 'nml/NeuroML_%s.xsd'%neuroml.current_neuroml_version)
   
    schema_file = open(xsd_file)
    xmlschema = etree.XMLSchema(etree.parse(schema_file))
    
    print("Validating %s against %s" %(file_name, xsd_file))
    xmlschema.assertValid(etree.parse(file_name))
    print("It's valid!")


