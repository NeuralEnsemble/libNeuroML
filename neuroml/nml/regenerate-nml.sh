#!/bin/bash

# Copyright 2021 NeuroML contributors
# File : regenerate-nml.sh
# Regenerate nml.py from the current schema version


echo "Note(1): Please remember to update the schema from the NeuroML2 repository"
echo "Note(2): Must be run in neuroml/nml/"
NEUROML_VERSION=$(grep -E 'current_neuroml_version.*' ../__init__.py | cut -d '=' -f 2 | tr -d '"' | tr -d ' ')
SCHEMA_FILE=NeuroML_${NEUROML_VERSION}.xsd

if command -v generateDS > /dev/null 2>&1
then
    echo "Rebuilding nml.py from ${SCHEMA_FILE} (Version: ${NEUROML_VERSION})"
    echo "generateds version:"
    generateDS --version

    rm -f nml.py
    export PYTHONPATH="$PYTHONPATH:." && generateDS -o nml.py --use-getter-setter=none --silence --user-methods=helper_methods.py $SCHEMA_FILE

    echo "Formatting new nml.py with black"
    black nml.py
else
    echo "GenerateDS not installed"
    echo "Run: pip install generateds"
    exit 1
fi

exit 0
