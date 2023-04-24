#!/usr/bin/env python3
"""
Generate sphinx sources for the libNeuroML nml.py classes

File: helpers/nml-core-docs.py

Copyright 2023 NeuroML authors
"""


import textwrap

print("Generating list of nml classes")

classes = {}
files = {
    "generatedssupersuper.py": [],
    "generatedscollector.py": [],
    "nml.py": [
        "GDSParseError",
        "MixedContainer",
        "MemberSpec_",
        "BlockTypes",
        "Metric",
        "PlasticityTypes",
        "ZeroOrOne",
        "allowedSpaces",
        "channelTypes",
        "gateTypes",
        "networkTypes",
        "populationTypes",
        "_FixedOffsetTZ",
        "GdsCollector_",
        "GeneratedsSuperSuper",
    ],
}

for f, excluded_classes in files.items():
    classlist = []
    with open("../../neuroml/nml/" + f, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("class "):
                # get the class signature
                aclass = line[len("class ") :]
                # for classes that are of form class A():
                aclass = aclass.split("(")[0]
                # for classes that are of form class A:
                aclass = aclass.split(":")[0]
                if aclass not in excluded_classes:
                    classlist.append(aclass)
    classlist.sort()
    classes[f] = classlist

with open("../userdocs/coreclasses_list.txt", "w") as fwrite:
    print(".. Generated using nml-core-docs.py", file=fwrite)
    for module, clist in classes.items():
        f = module.split(".")[0]
        for aclass in clist:
            # do not print all the internal methods in GeneratedsSuper
            if aclass == "GeneratedsSuper":
                towrite = textwrap.dedent(
                    """
                    {}
                    {}

                    .. autoclass:: neuroml.nml.{}.{}
                       :show-inheritance:

                    """.format(
                        aclass,
                        "#" * len(aclass),
                        f,
                        aclass,
                    )
                )
            else:
                towrite = textwrap.dedent(
                    """
                    {}
                    {}

                    .. autoclass:: neuroml.nml.{}.{}
                       :members:
                       :undoc-members:
                       :show-inheritance:
                       :inherited-members:

                    """.format(
                        aclass,
                        "#" * len(aclass),
                        f,
                        aclass,
                    )
                )
            print(towrite, file=fwrite)

print("Saved to userdocs/coreclasses_list.txt")
