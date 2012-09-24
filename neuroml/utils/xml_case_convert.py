"""
Working on util to convert naming conventions from neuroml to something more Python-friendly
"""

import re

def to_lowercase_with_underscores(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def remove_curlies(string):
    return re.sub("{.*}","",string)

#def capitalise_first(string):

