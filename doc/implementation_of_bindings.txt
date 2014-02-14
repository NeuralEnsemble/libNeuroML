Implementation of XML bindings for libNeuroML
=============================================

The GenerateDS Python package is used to automatically generate the NeuroML XML-bindings in libNeuroML from the NeuroML Schema. This technique can be utilized for any XML Schema and is outlined in this section. The addition of helper methods and enforcement of correct naming conventions is also described. For more detail on how Python bindings for XML are generated, the reader is directed to the GenerateDS and libNeuroML documentation. In the following subsections it is assumed that all commands are executed in a top level directory nml and that GenerateDS is installed. It should be noted that enforcement of naming conventions and addition of helper methods are not required by GenerateDS and default values may be used.

Correct naming conventions
--------------------------
A module named generateds_config.py is placed in the nml directory.
This module contains a Python dictionary called NameTable which maps
the original names specified in the XML Schema to user-specified ones.
The NameTable dictionary can be defined explicitly or generated
programmatically, for example using regular expressions.

Addition of helper methods
--------------------------

Helper methods associated with a class can be added to a Python module as string objects. In the case of libNeuroML the module is called helper_methods.py. The precise implementation details are esoteric and the user is referred to the GenerateDS documentation for details of how this functionality is implemented.

Generation of bindings
----------------------
Once generateds_config.py and a helper methods module are present in the nml directory a valid XML Schema is required by GenerateDS. The following command generates the nml.py module which contains the XML-bindings:

::

    $ generateDS.py -o nml.py --use-getter-setter=none --user-methods=helper_methods NeuroML_v2beta1.xsd

The -o flag sets the file which the module containing the bindings is to be written to. The --use-getter-setter=none option disables getters and setters for class attributes. The --user-methods flag indicates the name of the helper methods module (See section “Addition of helper methods”). The final parameter (NeuroML_v2beta1.xsd) is the name of the XML Schema used for generating the bindings.
