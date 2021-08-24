:mod:`nml` Module (NeuroML Core classes)
-----------------------------------------

These NeuroML core classes are Python representations of the Component Types defined in the NeuroML standard at https://docs.neuroml.org/Userdocs/NeuroMLv2.html.
These can be used to build NeuroML models in Python, and these models can then be exported to the standard XML NeuroML representation.
These core classes also contain some utility functions to make it easier for users to carry out common tasks.

Each NeuroML Component Type is represented here as a Python class.
Due to implementation limitations, whereas NeuroML Component Types use `lower camel case naming <https://en.wikipedia.org/wiki/Camel_case>`_, the Python classes here use `upper camel case naming <https://en.wikipedia.org/wiki/Camel_case>`__.
So, for example, the `adExIaFCell` Component Type in the NeuroML schema becomes the `AdExIaFCell` class here, and `expTwoSynapse` becomes the `ExpTwoSynapse` class.

The `child` and `children` elements that NeuroML Component Types can have are represented in the Python classes as variables.
The variable names, to distinguish them from class names, use `snake case <https://en.wikipedia.org/wiki/Snake_case>`__.
So for example, the `cell` NeuroML Component Type has a corresponding `Cell` Python class here.
The `biophysicalProperties` child Component Type in `cell` is represented as the `biophysical_properties` list variable in the `Cell` Python class.
The class signatures list all the child/children elements and text fields that the corresponding Component Type possesses.
To again use the `Cell` class as an example, the construction signature is this:

::

    class neuroml.nml.nml.Cell(neuro_lex_id=None, id=None, metaid=None, notes=None, properties=None, annotation=None, morphology_attr=None, biophysical_properties_attr=None, morphology=None, biophysical_properties=None, extensiontype_=None, **kwargs_)

As can be seen here, it includes both the `biophysical_properties` and `morphology` child elements as variables.

Please see the examples in the `NeuroML documentation <>`__ to see usage examples of libNeuroML.
Please also note that this module is also included in the top level of the `neuroml` package, so you can use these classes by importing neuroml:

::

    from neuroml import AdExIaFCell

..
    To get the list of all the validate* methods and members to add to the exlude list, use this:
    grep -Eo "def[[:space:]]*validate([[:alnum:]]|_)*|validate([[:alnum:]]|_)*patterns_" nml.py  | sed -e 's/^.*def validate/validate/' | sort -h | uniq | tr '\n' ','


.. automodule:: neuroml.nml.nml
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: build, buildAttributes, buildChildren, exportAttributes, export, exportChildren, factory, hasContent_, member_data_items_, subclass, superclass, warn_count, validate_allowedSpaces,validate_BlockTypes,validate_channelTypes,validate_DoubleGreaterThanZero,validate_gateTypes,validate_MetaId,validate_MetaId_patterns_,validate_Metric,validate_networkTypes,validate_NeuroLexId,validate_NeuroLexId_patterns_,validate_Nml2Quantity,validate_Nml2Quantity_capacitance,validate_Nml2Quantity_capacitance_patterns_,validate_Nml2Quantity_concentration,validate_Nml2Quantity_concentration_patterns_,validate_Nml2Quantity_conductance,validate_Nml2Quantity_conductanceDensity,validate_Nml2Quantity_conductanceDensity_patterns_,validate_Nml2Quantity_conductance_patterns_,validate_Nml2Quantity_conductancePerVoltage,validate_Nml2Quantity_conductancePerVoltage_patterns_,validate_Nml2Quantity_current,validate_Nml2Quantity_currentDensity,validate_Nml2Quantity_currentDensity_patterns_,validate_Nml2Quantity_current_patterns_,validate_Nml2Quantity_length,validate_Nml2Quantity_length_patterns_,validate_Nml2Quantity_none,validate_Nml2Quantity_none_patterns_,validate_Nml2Quantity_patterns_,validate_Nml2Quantity_permeability,validate_Nml2Quantity_permeability_patterns_,validate_Nml2Quantity_pertime,validate_Nml2Quantity_pertime_patterns_,validate_Nml2Quantity_resistance,validate_Nml2Quantity_resistance_patterns_,validate_Nml2Quantity_rhoFactor,validate_Nml2Quantity_rhoFactor_patterns_,validate_Nml2Quantity_specificCapacitance,validate_Nml2Quantity_specificCapacitance_patterns_,validate_Nml2Quantity_temperature,validate_Nml2Quantity_temperature_patterns_,validate_Nml2Quantity_time,validate_Nml2Quantity_time_patterns_,validate_Nml2Quantity_voltage,validate_Nml2Quantity_voltage_patterns_,validate_NmlId,validate_NmlId_patterns_,validate_NonNegativeInteger,validate_Notes,validate_PlasticityTypes,validate_populationTypes,validate_PositiveInteger,validate_ZeroOrOne,validate_ZeroToOne



