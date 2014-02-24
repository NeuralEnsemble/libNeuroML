"""

Utilities for checking generated code

"""

def validate_neuroml2(file_name):

    from lxml import etree
    try:
        from urllib2 import urlopen  # Python 2
    except:
        from urllib.request import urlopen # Python 3
        
    #schema_file = urlopen("https://raw.github.com/NeuroML/NeuroML2/master/Schemas/NeuroML2/NeuroML_v2beta.xsd")
    schema_file = urlopen("https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta2.xsd")
    xmlschema = etree.XMLSchema(etree.parse(schema_file))
    print("Validating %s against %s" %(file_name, schema_file.geturl()))
    xmlschema.assertValid(etree.parse(file_name))
    print("It's valid!")


