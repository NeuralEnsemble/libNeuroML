"""
Set of methods to translate between naming conventions 
in neuroml to others such as pythonic.
"""

import re

def to_lowercase_with_underscores(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def remove_curlies(string):
    return re.sub("{.*}","",string)

def to_camelback(string):
    string_list = list(string)
    for m in re.finditer:
        underscore_index = m.end()
        string_list(underscore_index) = string_list(underscore_index).lower()
    return str(string_list)


#def capitalise_first(string):

