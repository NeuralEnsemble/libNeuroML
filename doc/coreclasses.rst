:mod:`nml` Module (NeuroML Core classes)
-----------------------------------------

Note: This module is included in the top level of the `neuroml` package, so you can use these classes by importing neuroml:

::

    from neuroml import AdExIaFCell

..
    To get the list of all the validate* methods and members to add to the exlude list, use this:
    grep -Eo "def[[:space:]]*validate([[:alnum:]]|_)*|validate([[:alnum:]]|_)*patterns_" nml.py  | sed -e 's/^.*def validate/validate/' | sort -h | uniq | tr '\n' ','


.. automodule:: neuroml.nml.nml
    :members:
    :undoc-members:
    :exclude-members: build, buildAttributes, buildChildren, exportAttributes, export, exportChildren, factory, hasContent_, member_data_items_, subclass, superclass, warn_count, validate_allowedSpaces,validate_BlockTypes,validate_channelTypes,validate_DoubleGreaterThanZero,validate_gateTypes,validate_MetaId,validate_MetaId_patterns_,validate_Metric,validate_networkTypes,validate_NeuroLexId,validate_NeuroLexId_patterns_,validate_Nml2Quantity,validate_Nml2Quantity_capacitance,validate_Nml2Quantity_capacitance_patterns_,validate_Nml2Quantity_concentration,validate_Nml2Quantity_concentration_patterns_,validate_Nml2Quantity_conductance,validate_Nml2Quantity_conductanceDensity,validate_Nml2Quantity_conductanceDensity_patterns_,validate_Nml2Quantity_conductance_patterns_,validate_Nml2Quantity_conductancePerVoltage,validate_Nml2Quantity_conductancePerVoltage_patterns_,validate_Nml2Quantity_current,validate_Nml2Quantity_currentDensity,validate_Nml2Quantity_currentDensity_patterns_,validate_Nml2Quantity_current_patterns_,validate_Nml2Quantity_length,validate_Nml2Quantity_length_patterns_,validate_Nml2Quantity_none,validate_Nml2Quantity_none_patterns_,validate_Nml2Quantity_patterns_,validate_Nml2Quantity_permeability,validate_Nml2Quantity_permeability_patterns_,validate_Nml2Quantity_pertime,validate_Nml2Quantity_pertime_patterns_,validate_Nml2Quantity_resistance,validate_Nml2Quantity_resistance_patterns_,validate_Nml2Quantity_rhoFactor,validate_Nml2Quantity_rhoFactor_patterns_,validate_Nml2Quantity_specificCapacitance,validate_Nml2Quantity_specificCapacitance_patterns_,validate_Nml2Quantity_temperature,validate_Nml2Quantity_temperature_patterns_,validate_Nml2Quantity_time,validate_Nml2Quantity_time_patterns_,validate_Nml2Quantity_voltage,validate_Nml2Quantity_voltage_patterns_,validate_NmlId,validate_NmlId_patterns_,validate_NonNegativeInteger,validate_Notes,validate_PlasticityTypes,validate_populationTypes,validate_PositiveInteger,validate_ZeroOrOne,validate_ZeroToOne



