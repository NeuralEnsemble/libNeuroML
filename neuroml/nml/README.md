## Autogeneration of API, using generateds_config.py to ensure correct naming conventions.

NOTE: this requires the latest version of generateDS.py from https://bitbucket.org/dkuhlman/generateds

**For Python 3 compatibility, make sure this is >= version 2.20a**

All that is needed is the Schema - as long as generateds_config.py and helper_methods are present, nml.py should be generated correctly.

Unit tests should be run to confirm this.

generateDS.py should be invoked in this folder (so that generateds_config.py can be located) with the following command (namespace def here will be mended when it's become stable)

    generateDS.py -o nml.py --use-getter-setter=none --silence --user-methods=helper_methods NeuroML_v2beta5.xsd

You may have to add the current folder to your PYTHONPATH, i.e.

    export PYTHONPATH=$PYTHONPATH:.

