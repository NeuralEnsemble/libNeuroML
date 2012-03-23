# -*- coding: utf-8 -*-
"""

Initial version of Python API for NeuroML 2

Author: Padraig Gleeson

"""

import xml
import xml.sax


from libneuroml.neuroml2 import *


class NeuroMLDocument(neuroml):


    def writeNeuroML(self, nml2File):

        newfile = open(nml2File,"w")
        self.export(newfile, 0,namespacedef_='xmlns="http://www.neuroml.org/schema/neuroml2" \n\
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \n\
    xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 http://neuroml.svn.sourceforge.net/viewvc/neuroml/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd"\n   ')

        newfile.close()