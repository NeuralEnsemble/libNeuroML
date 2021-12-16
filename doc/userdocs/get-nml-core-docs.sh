#!/bin/bash

# Copyright 2021 Ankur Sinha
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com> 
# File :  get-nml-core-docs.sh
#
# Since automodule does not allow us to list each class as a sub-section, the
# NeuroML core class page becomes rather heavy and not easy to navigate.
# The only way around this is to not use automodule, and instead, use autoclass
# individuall for each class.

# This script will generate the rst file for use by sphinx.

grep -E '^class.*' ../neuroml/nml/nml.py | sed -e 's/^class //' -e 's/(.*)://' > classlist.txt


