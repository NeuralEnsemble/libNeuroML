#!/usr/bin/env python3
"""
Enter one line description here.

File:

Copyright 2021 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import textwrap


excluded_classes = ['GDSParseError', 'MixedContainer', 'MemberSpec_',
                    'BlockTypes', 'Metric', 'PlasticityTypes', 'ZeroOrOne', 'allowedSpaces',
                    'channelTypes', 'gateTypes', 'networkTypes', 'populationTypes']
classes = []
with open("../../neuroml/nml/nml.py", 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith("class"):
            # get the class signature
            aclass = line[len("class "):]
            aclass = aclass.split('(')[0]
            if aclass not in excluded_classes:
                classes.append(aclass)


classes.sort()

with open("../userdocs/coreclasses_list.txt", 'w') as fwrite:
    print(".. Generated using nml-core-docs.py", file=fwrite)
    for aclass in classes:
        towrite = textwrap.dedent(
            """
            {}
            {}

            .. autoclass:: neuroml.nml.nml.{}
               :members:
               :undoc-members:
               :show-inheritance:

            """.format(
                aclass, "#" * len(aclass), aclass,
            )
        )
        print(towrite, file=fwrite)
