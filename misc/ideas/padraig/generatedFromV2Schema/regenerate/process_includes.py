#!/usr/local/bin/python
"""
    python %prog [options] <in_schema.xsd>  <out_schema.xsd>
Synopsis:
    Prepare schema document.  Replace include and import elements.
Examples:
    python %prog myschema.xsd
    python %prog myschema.xsd newschema.xsd
    python %prog -f myschema.xsd newschema.xsd
    cat infile.xsd | python %prog > outfile.xsd
"""

#
# Imports

import sys
import os
import urllib2
import ftplib
import copy
import types
from optparse import OptionParser, Values
import itertools
from copy import deepcopy
from lxml import etree


#
# Globals and constants

#
# Do not modify the following VERSION comments.
# Used by updateversion.py.
##VERSION##
VERSION = '2.7b'
##VERSION##

Namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}
Xsd_namespace_uri = 'http://www.w3.org/2001/XMLSchema'


#
# Functions for external use

def process_include_files(infile, outfile, inpath=''):
    options = Values({
        'force': False,
        })
    prep_schema_doc(infile, outfile, inpath, options)


#
# Classes

class Params(object):
    members = ('base_url', 'already_processed', 'parent_url', )
    def __init__(self):
        self.base_url = None
        self.already_processed = set()
        self.parent_url = None
    def __setattr__(self, name, value):
        if name not in self.members:
            raise AttributeError('Class %s has no set-able attribute "%s"' % (
                self.__class__.__name__,  name, ))
        self.__dict__[name] = value


class SchemaIOError(IOError):
    pass

class RaiseComplexTypesError(Exception):
    pass

#
# Functions for internal use and testing


def clear_includes_and_imports(node):
    namespace = node.nsmap[node.prefix]
    child_iter1 = node.iterfind('{%s}include' % (namespace, ))
    child_iter2 = node.iterfind('{%s}import' % (namespace, ))
    for child in itertools.chain(child_iter1, child_iter2):
        repl = etree.Comment(etree.tostring(child))
        repl.tail = '\n'
        node.replace(child, repl)


def resolve_ref(node, params, options):
    content = None
    url = node.get('schemaLocation')
    if not url:
        msg = '*** Warning: missing "schemaLocation" attribute in %s\n' % (
            params.parent_url, )
        sys.stderr.write(msg)
        return None
    # Uncomment the next line to help track down missing schemaLocation etc.
    # print '(resolve_ref) url: %s\n    parent-url: %s' % (url, params.parent_url, )

    if params.base_url and not (
        url.startswith('/') or
        url.startswith('http:') or
        url.startswith('ftp:')
        ):
        locn = '%s/%s' % (params.base_url, url, )
        schema_name = locn
    else:
        locn = url
        schema_name = url
    if not (
        url.startswith('/') or
        url.startswith('http:') or
        url.startswith('ftp:')
        ):
        schema_name = os.path.abspath(locn)
    if locn is not None:
        if schema_name not in params.already_processed:
            params.already_processed.add(schema_name)
##             print 'trace --'
##             print '    url:        : %s' % (url, )
##             print '    base        : %s' % (params.base_url, )
##             print '    parent      : %s' % (params.parent_url, )
##             print '    locn        : %s' % (locn, )
##             print '    schema_name : %s\n' % (schema_name, )
            if locn.startswith('http:') or locn.startswith('ftp:'):
                try:
                    urlfile = urllib2.urlopen(locn)
                    content = urlfile.read()
                    urlfile.close()
                    params.parent_url = locn
                    params.base_url = os.path.split(locn)[0]
                except urllib2.HTTPError, exp:
                    msg = "Can't find file %s referenced in %s." % (
                        locn, params.parent_url, )
                    raise SchemaIOError(msg)
            else:
                if os.path.exists(locn):
                    infile = open(locn)
                    content = infile.read()
                    infile.close()
                    params.parent_url = locn
                    params.base_url = os.path.split(locn)[0]
                if content is None:
                    msg = "Can't find file %s referenced in %s." % (
                        locn, params.parent_url, )
                    raise SchemaIOError(msg)
##     if content is None:
##         msg = "Can't find file %s referenced in %s." % (
##             locn, params.parent_url, )
##         raise SchemaIOError(msg)
    return content


def collect_inserts(node, params, inserts, options):
    namespace = node.nsmap[node.prefix]
    child_iter1 = node.iterfind('{%s}include' % (namespace, ))
    child_iter2 = node.iterfind('{%s}import' % (namespace, ))
    for child in itertools.chain(child_iter1, child_iter2):
        collect_inserts_aux(child, params, inserts, options)


def collect_inserts_aux(child, params, inserts, options):
    save_base_url = params.base_url
    string_content = resolve_ref(child, params, options)
    if string_content is not None:
        root = etree.fromstring(string_content, base_url=params.base_url)
        for child1 in root:
            if not isinstance(child1, etree._Comment):
                namespace = child1.nsmap[child1.prefix]
                if (child1.tag != '{%s}include' % (namespace, ) and
                    child1.tag != '{%s' % (namespace, )):
                    comment = etree.Comment(etree.tostring(child))
                    comment.tail = '\n'
                    inserts.append(comment)
                    inserts.append(child1)
        collect_inserts(root, params, inserts, options)
    params.base_url = save_base_url


def make_file(outFileName, options):
    outFile = None
    if (not options.force) and os.path.exists(outFileName):
        reply = raw_input('File %s exists.  Overwrite? (y/n): ' % outFileName)
        if reply == 'y':
            outFile = open(outFileName, 'w')
    else:
        outFile = open(outFileName, 'w')
    return outFile


def prep_schema_doc(infile, outfile, inpath, options):
    doc1 = etree.parse(infile)
    root1 = doc1.getroot()
    params = Params()
    params.parent_url = infile
    params.base_url = os.path.split(inpath)[0]
    inserts = []
    collect_inserts(root1, params, inserts, options)
    root2 = copy.copy(root1)
    clear_includes_and_imports(root2)
    for insert_node in inserts:
        root2.append(insert_node)
    process_groups(root2)
    raise_anon_complextypes(root2)
    doc2 = etree.ElementTree(root2)
    doc2.write(outfile)
    return doc2


def prep_schema(inpath, outpath, options):
    if inpath:
        infile = open(inpath, 'r')
    else:
        infile = sys.stdin
    if outpath:
        outfile = make_file(outpath, options)
    else:
        outfile = sys.stdout
    if outfile is None:
        return
    prep_schema_doc(infile, outfile, inpath, options)
    if inpath:
        infile.close()
    if outpath:
        outfile.close()


def process_groups(root):
    # Get all the xs:group definitions at top level.
    defs = root.xpath('./xs:group', namespaces=Namespaces)
    defs = [node for node in defs if node.get('name') is not None]
    # Get all the xs:group references (below top level).
    refs = root.xpath('./*//xs:group', namespaces=Namespaces)
    refs = [node for node in refs if node.get('ref') is not None]
    # Create a dictionary of the named model groups (definitions).
    def_dict = {}
    for node in defs:
        def_dict[trim_prefix(node.get('name'))] = node
    replace_group_defs(def_dict, refs)


def replace_group_defs(def_dict, refs):
    for ref_node in refs:
        name = trim_prefix(ref_node.get('ref'))
        if name is None:
            continue
        def_node = def_dict.get(name)
        if def_node is not None:
            content = def_node.xpath('./xs:sequence|./xs:choice|./xs:all',
                namespaces=Namespaces)
            if content:
                content = content[0]
                parent = ref_node.getparent()
                for node in content:
                    new_node = deepcopy(node)
                    # Copy minOccurs and maxOccurs attributes to new node.
                    value = ref_node.get('minOccurs')
                    if value is not None:
                        new_node.set('minOccurs', value)
                    value = ref_node.get('maxOccurs')
                    if value is not None:
                        new_node.set('maxOccurs', value)
                    ref_node.addprevious(new_node)
                parent.remove(ref_node)


def raise_anon_complextypes(root):
    """ Raise each anonymous complexType to top level and give it a name.
    Rename if necessary to prevent duplicates.
    """
    element_tag = '{%s}element' % (Xsd_namespace_uri, )
    def_names = {}
    # Collect top level complexTypes.
    defs = root.xpath('./xs:complexType', namespaces=Namespaces)
    for node in defs:
        type_name = node.get('name')
        def_names[type_name] = node
    # Collect top level simpleTypes.
    defs = root.xpath('./xs:simpleType', namespaces=Namespaces)
    for node in defs:
        type_name = node.get('name')
        def_names[type_name] = node
    # Find all complexTypes below top level.
    #   Raise them to top level and name them.
    #   Re-name if there is a duplicate (simpleType, complexType, or
    #   previous renamed type).
    #   Change the parent (xs:element) so the "type" attribute refers to 
    #   the raised and renamed type.
    #   Collect the new types.
    el = etree.Comment(text="Raised anonymous complexType definitions")
    el.tail = "\n\n"
    root.append(el)
    defs = root.xpath('./*/*//xs:complexType', namespaces=Namespaces)
    for node in defs:
        parent = node.getparent()
        if parent.tag != element_tag:
            continue
        name = parent.get('name')
        if not name:
            continue
        type_name = '%sType' % (name, )
        type_name = unique_name(type_name, def_names)
        def_names[type_name] = node
        parent.set('type', type_name)
        node.set('name', type_name)
        # Move the complexType node to top level.
        root.append(node)

def unique_name(type_name, def_names):
    orig_type_name = type_name
    count = 0
    while count < 100:
        if type_name not in def_names:
            return type_name
        count += 1
        type_name = '%s%d' % (orig_type_name, count, )
    raise RaiseComplexTypesError('duplicate name count max (100) exceeded')


def trim_prefix(name):
    names = name.split(':')
    if len(names) == 1:
        return names[0]
    elif len(names) == 2:
        return names[1]
    else:
        return None


USAGE_TEXT = __doc__

def usage(parser):
    parser.print_help()
    sys.exit(1)


def main():
    parser = OptionParser(USAGE_TEXT)
    parser.add_option("-f", "--force", action="store_true",
        dest="force", default=False,
        help="force overwrite without asking")
    (options, args) = parser.parse_args()
    if len(args) == 2:
        inpath = args[0]
        outpath = args[1]
    elif len(args) == 1:
        inpath = args[0]
        outpath = None
    elif len(args) == 0:
        inpath = None
        outpath = None
    else:
        usage(parser)
    prep_schema(inpath, outpath, options)


if __name__ == "__main__":
    #import pdb; pdb.set_trace()
    main()

