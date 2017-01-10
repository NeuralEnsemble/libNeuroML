"""

Utilities for checking generated code

"""
import os.path

import neuroml
import inspect

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
    
    
def add_all_to_document(nml_doc_src, nml_doc_tgt):
    
    membs = inspect.getmembers(nml_doc_src)

    for memb in membs:
        if isinstance(memb[1], list) and len(memb[1])>0 \
                and not memb[0].endswith('_'):
            for entry in memb[1]:
                if memb[0] != 'includes':
                    print("  Adding %s to list: %s" \
                        %(entry.id if hasattr(entry,'id') else entry.name, memb[0]))
                    getattr(nml_doc_tgt, memb[0]).append(entry)
                    
def append_to_element(parent, child):
    
        import inspect
        membs = inspect.getmembers(parent)
        print("Adding %s to element %s"%(child, parent))
        mappings = {}
        for mdi in parent.member_data_items_:
            mappings[mdi.data_type] = mdi.name
        added = False
        for memb in membs:
            if isinstance(memb[1], list) and not memb[0].endswith('_'):
                #print("Adding %s to %s in %s?"%(child.__class__.__name__, memb[0], parent.__class__.__name__))
                if mappings[child.__class__.__name__] == memb[0]:
                    for c in getattr(parent, memb[0]):
                        if c.id == child.id:
                            added = True
                    if not added:
                        getattr(parent, memb[0]).append(child)
                        added = True
                    
        if not added:
            raise Exception("Could not add %s to %s"%(child, parent))
        
                


