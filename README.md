## Introduction

This package provides Python libNeuroML, for working with neuronal models specified in NeuroML 2 (http://neuroml.org/neuromlv2).

For more about libNeuroML see:

Michael Vella, Robert C. Cannon, Sharon Crook, Andrew P. Davison, Gautham Ganapathy, Hugh P. C. Robinson, R. Angus Silver and Padraig Gleeson,
**libNeuroML and PyLEMS: using Python to combine procedural and declarative modeling approaches in computational neuroscience**
[Frontiers in Neuroinformatics 2014](http://journal.frontiersin.org/Journal/10.3389/fninf.2014.00038/abstract), doi: 10.3389/fninf.2014.00038

_**PLEASE CITE THE PAPER ABOVE IF YOU USE libNeuroML!**_


Documentation is available at http://readthedocs.org/docs/libneuroml/en/latest/

For installation instructions, see http://readthedocs.org/docs/libneuroml/en/latest/install.html

For details on how to contribute, see http://readthedocs.org/docs/libneuroml/en/latest/how_to_contribute.html

## Travis integration

libNeuroML is integrated with the the [Travis Continuous Integration service](http://travis-ci.org/).

[![Build Status](https://api.travis-ci.org/NeuralEnsemble/libNeuroML.png)](https://travis-ci.org/NeuralEnsemble/libNeuroML)

##Changelog

###version 0.2.18
 - Updated to use the final stable Schema for NeuroML v2beta4
 - Tested with Python 3

###version 0.2.4
 - Updated to use the Schema for NeuroML v2beta4

###version 0.2.2
 - Updated to use the Schema for NeuroML v2beta3
 - Ensures numpy & pytables are only required when using non-XML loaders/writers 

###version 0.2.0
 - Updated to use the Schema for NeuroML v2beta2

###version 0.1.9
 - Minor release: Update to latest schema

###version 0.1.8

 - Several Bug fixes and small enhamcements
 - Support for latest NeuroML schema (see change outline)
 - JSON serialization
 - MongoDB backend
 - HDF5 serialization
 - Improved installation process
 - All usage examples are now run on the Travis-CI continuous integration server to confirm that that they do not error.
 - Schema validation utility
 - Improved documentation and documentation new look

:copyright: Copyright 2012 by the libNeuroML team, see AUTHORS.
:license: Modified BSD License, see LICENSE for details.
