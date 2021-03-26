## Autogeneration of API, using generateds_config.py to ensure correct naming conventions.

This requires [generateDS.py](http://www.davekuhlman.org/generateDS.html), version >= 2.20a.

You can get it from [PyPi](http://pypi.python.org/pypi/generateDS/) or [Source Forge](https://sourceforge.net/projects/generateds/).

All that is needed is the Schema - as long as generateds_config.py and helper_methods are present, nml.py should be generated correctly.

Unit tests should be run to confirm this.

generateDS.py should be invoked in this folder (so that generateds_config.py can be located) with the following command (namespace def here will be mended when it's become stable)

    generateDS.py -o nml.py --use-getter-setter=none --silence --user-methods=helper_methods NeuroML_v2.1.xsd

You may have to add the current folder to your PYTHONPATH, i.e.

    export PYTHONPATH=$PYTHONPATH:.


Note that generateDS.py will import the generateds_config.py file and run it.
Your output should, therefore, include lines of the form:

    generateds_config.py is being processed
    Saving NameTable to csv file: name_table.csv
    Saving name changes table to csv file: changed_names.csv


If these are not included in the output, generateds_config.py has not run, and the generated nml.py file will be incorrect.

### Changelog

#### March 26, 2020

Author: @sanjayankur31

Generated using Python 3.9 for NeuroMLv2.1.xsd using generateDS.py 2.35.5

    # Generated Fri Mar 26 09:44:40 2021 by generateDS.py version 2.35.5.
    # Python 3.9.2 (default, Feb 20 2021, 00:00:00)  [GCC 11.0.0 20210210 (Red Hat 11.0.0-0)]
    # ~/.virtualenvs/generateds/bin/generateDS.py -o "nml.py" --use-getter-setter="none" --silence --user-methods="helper_methods.py" NeuroML_v2.1.xsd

#### February 2020

Author: @pgleeson

Retested & regenerated using Python 2.7 with generateDS.py v2.30.11- currently fails when generated with Python 3.
