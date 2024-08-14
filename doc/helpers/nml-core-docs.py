#!/usr/bin/env python3
"""
Generate sphinx sources for the libNeuroML nml.py classes

File: helpers/nml-core-docs.py

Copyright 2023 NeuroML authors
"""

import json
import textwrap

print("Generating list of nml classes")

component_type_list = None
with open("../component-list.json", "r") as f:
    component_type_list = json.load(f)

component_type_list["Other"] = []

output_files = {}
comp_num_dict = {}

for ctype in component_type_list.keys():
    fwrite = open(f"../userdocs/{ctype}_list.rst", "w")
    output_files[ctype] = fwrite
    print(ctype, file=fwrite)
    print("#" * len(ctype), file=fwrite)
    print("\n", file=fwrite)
    print("\n", file=fwrite)
    print(
        f"This documentation is auto-generated from the `NeuroML schema <https://docs.neuroml.org/Userdocs/Schemas/{ctype}.html>`__.",
        file=fwrite,
    )
    print("\n", file=fwrite)
    print("\n", file=fwrite)
    print(".. Generated using nml-core-docs.py", file=fwrite)

    comp_num_dict[ctype] = 0

comp_to_file_map = {}
for file, ctypes in component_type_list.items():
    for ctype in ctypes:
        comp_to_file_map[ctype[0].capitalize() + ctype[1:]] = file

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
                    "^" * len(aclass),
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
                    "^" * len(aclass),
                    f,
                    aclass,
                )
            )
        try:
            category = comp_to_file_map[aclass]
        except KeyError:
            if "cell" in aclass.lower():
                category = "Cells"
            elif "gate" in aclass.lower():
                category = "Channels"
            else:
                category = "Other"
        else:
            comp_num_dict[category] += 1
            fwrite = output_files[category]
            print(towrite, file=fwrite)

print("Done")
print(comp_num_dict)

for comp, num in comp_num_dict.items():
    output_files[comp].close()
