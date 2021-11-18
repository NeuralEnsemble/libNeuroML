:mod:`nml` Module (NeuroML Core classes)
-----------------------------------------

These NeuroML core classes are Python representations of the Component Types defined in the `NeuroML standard <https://docs.neuroml.org/Userdocs/NeuroMLv2.html>`__ .
These can be used to build NeuroML models in Python, and these models can then be exported to the standard XML NeuroML representation.
These core classes also contain some utility functions to make it easier for users to carry out common tasks.

Each NeuroML Component Type is represented here as a Python class.
Due to implementation limitations, whereas NeuroML Component Types use `lower camel case naming <https://en.wikipedia.org/wiki/Camel_case>`_, the Python classes here use `upper camel case naming <https://en.wikipedia.org/wiki/Camel_case>`__.
So, for example, the :code:`adExIaFCell` Component Type in the NeuroML schema becomes the :code:`AdExIaFCell` class here, and :code:`expTwoSynapse` becomes the :code:`ExpTwoSynapse` class.

The :code:`child` and :code:`children` elements that NeuroML Component Types can have are represented in the Python classes as variables.
The variable names, to distinguish them from class names, use `snake case <https://en.wikipedia.org/wiki/Snake_case>`__.
So for example, the :code:`cell` NeuroML Component Type has a corresponding :code:`Cell` Python class here.
The :code:`biophysicalProperties` child Component Type in :code:`cell` is represented as the :code:`biophysical_properties` list variable in the :code:`Cell` Python class.
The class signatures list all the child/children elements and text fields that the corresponding Component Type possesses.
To again use the :code:`Cell` class as an example, the construction signature is this:

::

    class neuroml.nml.nml.Cell(neuro_lex_id=None, id=None, metaid=None, notes=None, properties=None, annotation=None, morphology_attr=None, biophysical_properties_attr=None, morphology=None, biophysical_properties=None, extensiontype_=None, **kwargs_)

As can be seen here, it includes both the :code:`biophysical_properties` and :code:`morphology` child elements as variables.

Please see the examples in the `NeuroML documentation <https://docs.neuroml.org/Userdocs/GettingStarted.html>`__ to see usage examples of libNeuroML.
Please also note that this module is also included in the top level of the `neuroml` package, so you can use these classes by importing neuroml:

::

    from neuroml import AdExIaFCell

..
    To get the list of all the validate* methods and members to add to the exlude list, use this:
    grep -Eo "def[[:space:]]*validate([[:alnum:]]|_)*|validate([[:alnum:]]|_)*patterns_" nml.py  | sed -e 's/^.*def validate/validate/' | sort -h | uniq | tr '\n' ','



List of Component classes
~~~~~~~~~~~~~~~~~~~~~~~~~~

This documentation is auto-generated from the `NeuroML schema <https://docs.neuroml.org/Userdocs/NeuroMLv2.html>`__.
In case of issues, please refer to the schema documentation for clarifications.
If the schema documentation does not resolve the issue, please `contact us <https://docs.neuroml.org/NeuroMLOrg/CommunicationChannels.html>`__.

.. include:: coreclasses_list.txt
