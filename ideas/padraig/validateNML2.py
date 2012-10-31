###
#   Utility script to validate any file or folder of *.nml files against the NeuroML 2 schema
###

import sys

for file in sys.argv[1:]:


    from lxml import etree
    from urllib import urlopen

    loc = "http://neuroml.svn.sourceforge.net/viewvc/neuroml/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd"
    schema_file = urlopen(loc)

    xmlschema_doc = etree.parse(schema_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    print "Validating %s against %s" %(file, loc)

    doc = etree.parse(file)
    xmlschema.assertValid(doc)
    print "It's valid!"
