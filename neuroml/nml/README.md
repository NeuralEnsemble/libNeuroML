## Autogeneration of API, using generateds_config.py to ensure correct naming conventions.

This requires [generateDS.py](http://www.davekuhlman.org/generateDS.html), version >= 2.20a.

You can get it from [PyPi](http://pypi.python.org/pypi/generateDS/) or [Source Forge](https://sourceforge.net/projects/generateds/).

All that is needed is the Schema - as long as generateds_config.py and helper_methods are present, nml.py should be generated correctly.

Unit tests should be run to confirm this.

generateDS.py should be invoked in this folder (so that generateds_config.py can be located) with the following command (namespace def here will be mended when it's become stable)

    generateDS.py -o nml.py --use-getter-setter=none --silence --user-methods=helper_methods NeuroML_v2.2.xsd

You may have to add the current folder to your PYTHONPATH, i.e.

    export PYTHONPATH=$PYTHONPATH:.


Note that generateDS.py will import the generateds_config.py file and run it.
Your output should, therefore, include lines of the form:

    generateds_config.py is being processed
    Saving NameTable to csv file: name_table.csv
    Saving name changes table to csv file: changed_names.csv


If these are not included in the output, generateds_config.py has not run, and the generated nml.py file will be incorrect.

### Changelog

#### August 26, 2021

Author: @sanjayankur31

Generate with Python 3.9, generateDS version 2.39.9

- all tests pass
- `--use-getter-setter=none`, which causes test failures because of probable generateDS bug. See: https://sourceforge.net/p/generateds/tickets/20/
- also requires us to manually patch one or two conversions to work around https://sourceforge.net/p/generateds/tickets/13/

#### March 26, 2020

Author: @sanjayankur31

Resort to using Python 2.7 and generateDS.py 2.30.11 for the time being.

- all tests and examples pass

#### March 26, 2020

Author: @sanjayankur31

Generation attempt using Python 3.9 for NeuroMLv2.1.xsd using generateDS.py 2.38.3:

- generation requires updating of the generateds_config.py file
- generated nml.py seems to contain issues: https://sourceforge.net/p/generateds/tickets/13/
- after tweaking nml.py, json serialization example still fails.


#### February 2020

Author: @pgleeson

Retested & regenerated using Python 2.7 with generateDS.py v2.30.11- currently fails when generated with Python 3.
