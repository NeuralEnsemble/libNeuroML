# -*- coding: utf-8 -*-
"""

Initial version of Python API for LEMS

Author: Padraig Gleeson

"""

import xml
import xml.sax
import sys

__version__ = "0.2"


class NeuroMLReader:

    def readNeuroML(self, filename):

        '''nmlFile = open()'''
        import v2
        
        try:
            nml2Doc = v2.parse(filename)
            print "Read in NeuroML 2 doc with id: %s"%nml2Doc.getId()

            return nml2Doc
        except Exception:
            print "Not a valid NeuroML 2 doc:", sys.exc_info()
            return None

