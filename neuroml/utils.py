"""

Utilities for checking generated code

"""
import os.path
import sys

import neuroml
import inspect


def validate_neuroml2(file_name):

    from lxml import etree
    try:
        from urllib2 import urlopen  # Python 2
    except:
        from urllib.request import urlopen # Python 3
        
    xsd_file = os.path.join(os.path.dirname(__file__), 'nml/NeuroML_%s.xsd'%neuroml.current_neuroml_version)
   
    with open(xsd_file) as schema_file:
        xmlschema = etree.XMLSchema(etree.parse(schema_file))
        print("Validating %s against %s" %(file_name, xsd_file))
        if not xmlschema.validate(etree.parse(file_name)):
            xmlschema.assertValid(etree.parse(file_name)) # print reason if file is invalid
            return
        print("It's valid!")

# Return True if .nml file is valid else false
def is_valid_neuroml2(file_name):
    from lxml import etree
    try:
        from urllib2 import urlopen  # Python 2
    except:
        from urllib.request import urlopen  # Python 3

    xsd_file = os.path.join(os.path.dirname(__file__), 'nml/NeuroML_%s.xsd' % neuroml.current_neuroml_version)

    with open(xsd_file) as schema_file:
        xmlschema = etree.XMLSchema(etree.parse(schema_file))
        return (xmlschema.validate(etree.parse(file_name)))
    return False


def print_summary(nml_file_name):
    
    print(get_summary(nml_file_name))
    
    
def get_summary(nml_file_name):
    
    from neuroml.loaders import read_neuroml2_file
    nml_doc = read_neuroml2_file(nml_file_name,include_includes=True, verbose=False, optimized=True)
    
    return nml_doc.summary(show_includes=False)

    
def add_all_to_document(nml_doc_src, nml_doc_tgt, verbose=False):
    
    membs = inspect.getmembers(nml_doc_src)

    for memb in membs:
        if isinstance(memb[1], list) and len(memb[1])>0 \
                and not memb[0].endswith('_'):
            for entry in memb[1]:
                if memb[0] != 'includes':
                    
                    added = False
                    for c in getattr(nml_doc_tgt, memb[0]):
                        if hasattr(c,'id') and c.id == entry.id:
                            added = True
                    if not added:
                        #print("  Adding %s to list: %s" \
                        #    %(entry.id if hasattr(entry,'id') else entry.name, memb[0]))
                        getattr(nml_doc_tgt, memb[0]).append(entry)
                        added = True
                        
                    if not added:
                        raise Exception("Could not add %s from %s to %s"%(entry, nml_doc_src, nml_doc_tgt))
                    
def append_to_element(parent, child):
    
        import inspect
        membs = inspect.getmembers(parent)
        #print("Adding %s to element %s"%(child, parent))
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
                        #print("Adding %s to %s in %s?"%(child.__class__.__name__, memb[0], parent.__class__.__name__))
                        added = True
                    
        if not added:
            raise Exception("Could not add %s to %s"%(child, parent))
        
def has_segment_fraction_info(connections):
    if not connections:
        return False
    no_seg_fract_info = True
    i=0
    while no_seg_fract_info and i<len(connections):
        conn = connections[i]
        no_seg_fract_info = conn.pre_segment_id==0 and conn.post_segment_id == 0 and conn.pre_fraction_along == 0.5 and conn.post_fraction_along ==0.5
        i+=1
    #print("Checked connections: [%s,...], no_seg_fract_info: %s"%(connections[0],no_seg_fract_info))
    return not no_seg_fract_info

                
def main():
    if len(sys.argv)!=2:
        print("Please specify the name of the NeuroML2 file...")
        exit(1)
        
    print_summary(sys.argv[1])

if __name__ == '__main__':
    main()

