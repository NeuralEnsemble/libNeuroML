#!/usr/bin/env python3
"""
Gets type information from nml.py and generates a file of sed commands to be
used to modify nml.py to add some information about the types of all variables
in component type class constructors.

This must be run from the project root for all the imports to work correctly:

python -m neuroml.nml.annotate_nml

File: annotate_nml.py

Copyright 2022 NeuroML contributors
"""


import inspect
from . import nml


ignorelist = [
    "GeneratedsSuper",
    "GeneratedsSuperSuper",
]


def pred(c):
    return (inspect.isclass(c) and (c.__name__ not in ignorelist))


classes = inspect.getmembers(nml, pred)

with open("sed-script.txt", 'w') as f:
    for aclass, atype in classes:
        # print(f"Processing {aclass}")
        member_types = {}
        if getattr(atype, "get_members", False):
            members = atype().get_members()
            for amember in members:
                dtype = amember.get_data_type().replace("xs:", "").replace("string", "str")
                dname = amember.get_name()
                dreq = "required"

                if amember.get_optional() == 0:
                    dreq = "optional"

                regexstart = f"^class {aclass}"
                regexend = f"# end class {aclass}"

                # We add annotations as strings, just to help users better
                # understand what needs to be used.
                if amember.get_container() == 0:
                    print(
                        f"""/{regexstart}/,/{regexend}/ s/{dname}=None/{dname}: "one {dtype} ({dreq})" = None/""",
                        file=f
                    )
                else:
                    print(
                        f"""/{regexstart}/,/{regexend}/ s/{dname}=None/{dname}: "list of {dtype}(s) ({dreq})" = None/""",
                        file=f
                    )
