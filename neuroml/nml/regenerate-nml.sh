#!/bin/bash

# Copyright 2023 NeuroML contributors
# File : regenerate-nml.sh
# Regenerate nml.py from the current schema version


echo "Note(1): Please remember to update the schema from the NeuroML2 repository"
echo "Note(2): Must be run in neuroml/nml/"
NEUROML_VERSION=$(grep -E 'current_neuroml_version.*' ../__version__.py | cut -d '=' -f 2 | tr -d '"' | tr -d ' ')
SCHEMA_FILE=NeuroML_${NEUROML_VERSION}.xsd
PYTHON_VERSION=$(python3 --version 2>&1)

regenerate () {
    if command -v generateDS > /dev/null 2>&1
    then
        echo "Rebuilding nml.py from ${SCHEMA_FILE} (Version: ${NEUROML_VERSION})"
        echo "generateds version:"
        generateDS --version
        echo "Python version: $PYTHON_VERSION"

        rm -f nml.py


        PYTHONPATH="$PYTHONPATH:." generateDS -o nml.py --use-getter-setter=none --user-methods=helper_methods.py --export="write validate" --custom-imports-template=gds_imports-template.py $SCHEMA_FILE
        # correct path to generatedssupersuper module file
        sed -i 's/from generatedssupersuper/from .generatedssupersuper/' nml.py
        sed -i 's/from generatedscollector/from .generatedscollector/' nml.py

        # replace default arguments (None) with some hint of what's expected
        # must be run from top level because of all the imports we
        # have---otherwise it errors
        echo "Modifying default arguments using annotate_nml and sed"
        pushd ../../
            # generates the sed-script.txt file
            python3 -m neuroml.nml.annotate_nml
            echo "Generated sed script"
            sed_lines=$(wc -l sed-script.txt | cut -f1 -d " ")
            if [ $sed_lines -eq 0 ]
            then
                echo "Something went wrong. No lines in sed script."
            else
                echo "${sed_lines} lines in sed script"
            fi
        popd
        # apply the sed transformations
        sleep 1 && sed -i -f ../../sed-script.txt nml.py
    else
        echo "GenerateDS not installed"
        echo "Run: pip install generateds"
        exit 1
    fi
}

reformat () {
    if command -v black > /dev/null 2>&1
    then
        echo "Formatting new nml.py with black"
        black nml.py
    else
        echo "black is not installed"
        echo "Run: pip install black"
    fi
}

usage () {
    echo "$0: Regenerate and reformat nml.py from the XSD schema file"
    echo
    echo "Usage: $0 [-arfh]"
    echo
    echo "-r: regenerate"
    echo "-f: reformat"
    echo "-a: regenerate and reformat"
    echo "-h: print this help text and exit"
}

if [ $# -lt 1 ]
then
    usage
    exit 1
fi

# parse options
while getopts "arfh" OPTION
do
    case $OPTION in
        r)
            regenerate
            exit 0
            ;;
        f)
            reformat
            exit 0
            ;;
        a)
            regenerate && reformat
            exit 0
            ;;
        h)
            usage
            exit 0
            ;;
        ?)
            usage
            exit 1
            ;;
    esac
done
