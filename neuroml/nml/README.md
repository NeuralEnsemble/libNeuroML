## Autogeneration of API, using generateds_config.py to ensure correct naming conventions.

Please regenerate nml.py in a new branch and open a pull request against the `development` branch.

Please **do not** regenerate nml.py and push directly to the `master` branch because regeneration of `nml.py` may change the libNeuroML API, and so this could be a backwards incompatible change which must not be pushed to master without a corresponding release and sufficient testing.

### Requirements

- the Schema (XSD) file
- `generateds_config.py`: this includes the correct naming conventions
- `helper_methods.py`: this includes additional helper methods that we want to add to the API

The following packages are required.

- generateds
- black

They can be installed using the `requirements-dev.txt` file in the root directory:

```
pip install -r requirements-dev.txt
```

### Regenerating nml.py

- Run the `regenerate-nml.sh` script in the `neuroml/nml` folder.
- This will use the API version defined in `neuroml/__init__.py` to find the right schema XSD file and run generateds to regenerate the `nml.py` file.
- It will also run `black` on the newly generated file to reformat it.

The generateDS command that is invoked is of this form:

    generateDS.py -o nml.py --use-getter-setter=none --silence --user-methods=helper_methods.py NeuroML_v2.2.xsd

You will need to add the current folder to your PYTHONPATH so that the required files can be imported by generateDS.

    export PYTHONPATH=$PYTHONPATH:.


Your output should include lines of the form:

    generateds_config.py is being processed
    Saving NameTable to csv file: name_table.csv
    Saving name changes table to csv file: changed_names.csv


If these are not included in the output, generateDS has not run correctly, and the generated nml.py file will be incorrect.

### Testing

Please remember to:

- rebuild libNeuroML after regenerating `nml.py`
- run all unit tests
- run all examples

The CI on GitHub will always run these.

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
