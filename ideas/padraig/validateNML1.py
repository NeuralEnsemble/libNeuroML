###
#   Utility script to validate any file or folder of *.nml files against the NeuroML v1.8.1 schema
###

import sys

for file in sys.argv[1:]:


    from lxml import etree
    from urllib import urlopen

    file_loc = "http://neuroml.svn.sourceforge.net/viewvc/neuroml/trunk/web/NeuroMLFiles/Schemata/v1.8.1/Level3/NeuroML_Level3_v1.8.1.xsd"
    schema_file = urlopen(file_loc)

    xmlschema_doc = etree.parse(schema_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    print "Validating %s against %s" %(file, file_loc)

    doc = etree.parse(file)
    xmlschema.assertValid(doc)
    print "It's valid!"
