# -*- coding: utf-8 -*-
"""

Initial version of Python API for NeuroML 2

Author: Padraig Gleeson

"""

import xml
import xml.sax


from neuroml.v2 import *


class NeuroMLDocument(neuroml):


    def writeNeuroML(self, nml2File):

        newfile = open(nml2File,"w")
        self.export(newfile, 0,namespacedef_='xmlns="http://www.neuroml.org/schema/neuroml2" \n\
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \n\
    xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 http://neuroml.svn.sourceforge.net/viewvc/neuroml/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd"\n   ')

        newfile.close()


# Helper function
def validateNml2(nml2file):
    from lxml import etree
    from urllib import urlopen

    schema_file = urlopen("http://neuroml.svn.sourceforge.net/viewvc/neuroml/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd")
    xmlschema_doc = etree.parse(schema_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    print "Validating %s against %s" %(nml2file, schema_file.geturl())

    doc = etree.parse(nml2file)
    xmlschema.assertValid(doc)
    print "It's valid!"