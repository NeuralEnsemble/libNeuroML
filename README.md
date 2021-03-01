## Introduction

[![Travis CI](https://travis-ci.org/NeuralEnsemble/libNeuroML.svg?branch=master)](https://travis-ci.org/NeuralEnsemble/libNeuroML)
[![PyPI](https://img.shields.io/pypi/v/libNeuroML)](https://pypi.org/project/libNeuroML/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/libNeuroML)](https://pypi.org/project/libNeuroML/)
[![GitHub](https://img.shields.io/github/license/NeuralEnsemble/libNeuroML)](https://github.com/NeuralEnsemble/libNeuroML/blob/master/LICENSE)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/NeuralEnsemble/libNeuroML)](https://github.com/NeuralEnsemble/libNeuroML/pulls)
[![GitHub issues](https://img.shields.io/github/issues/NeuralEnsemble/libNeuroML)](https://github.com/NeuralEnsemble/libNeuroML/issues)
[![GitHub Org's stars](https://img.shields.io/github/stars/NeuralEnsemble?style=social)](https://github.com/NeuralEnsemble)
[![Twitter Follow](https://img.shields.io/twitter/follow/NeuroML?style=social)](https://twitter.com/NeuroML)

This package provides Python libNeuroML, for working with neuronal models specified in [NeuroML 2](http://neuroml.org/neuromlv2).

For more about libNeuroML see:

Michael Vella, Robert C. Cannon, Sharon Crook, Andrew P. Davison, Gautham Ganapathy, Hugh P. C. Robinson, R. Angus Silver and Padraig Gleeson,
**libNeuroML and PyLEMS: using Python to combine procedural and declarative modeling approaches in computational neuroscience**
[Frontiers in Neuroinformatics 2014](http://journal.frontiersin.org/Journal/10.3389/fninf.2014.00038/abstract), doi: 10.3389/fninf.2014.00038

_**PLEASE CITE THE PAPER ABOVE IF YOU USE libNeuroML!**_

Documentation is available at http://readthedocs.org/docs/libneuroml/en/latest/

For installation instructions, see http://readthedocs.org/docs/libneuroml/en/latest/install.html

For an overview of all NeuroML related libraries/documentation/publications see https://neuroml.org/getneuroml.

## pyNeuroML

A related package, **[pyNeuroML](https://github.com/NeuroML/pyNeuroML)** builds on this and provides functionality, scripts and modules for reading, writing, **simulating** and analysing NeuroML2/LEMS models.

pyNeuroML builds on: [libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) & [PyLEMS](https://github.com/LEMS/pylems) and wraps functionality from [jNeuroML](https://github.com/NeuroML/jNeuroML).


## Development process for libNeuroML

Most of the work happens in the [development branch](https://github.com/NeuralEnsemble/libNeuroML/tree/development). That branch is kept up to date with the development branches for [NeuroML 2](https://github.com/NeuroML/NeuroML2/tree/development) and related libraries. See https://neuroml.org/getneuroml for an overview of the various NeuroML libraries.

## Changelog

### version 0.2.54
 - Using Schema for NeuroML v2.1. Better compatibility with Python 3

 ### version 0.2.50
  - Updated to use the final stable Schema for NeuroML v2.0

### version 0.2.47
 - Updated to use the final stable Schema for NeuroML v2beta5

### version 0.2.18
 - Updated to use the final stable Schema for NeuroML v2beta4
 - Tested with Python 3

### version 0.2.4
 - Updated to use the Schema for NeuroML v2beta4

### version 0.2.2
 - Updated to use the Schema for NeuroML v2beta3
 - Ensures numpy & pytables are only required when using non-XML loaders/writers

### version 0.2.0
 - Updated to use the Schema for NeuroML v2beta2

### version 0.1.9
 - Minor release: Update to latest schema

### version 0.1.8

 - Several Bug fixes and small enhamcements
 - Support for latest NeuroML schema (see change outline)
 - JSON serialization
 - MongoDB backend
 - HDF5 serialization
 - Improved installation process
 - All usage examples are now run on the Travis-CI continuous integration server to confirm that that they do not error.
 - Schema validation utility
 - Improved documentation and documentation new look


:copyright: Copyright 2020 by the libNeuroML team, see [AUTHORS](AUTHORS). Modified BSD License, see [LICENSE](LICENSE) for details.


[![Build Status](https://api.travis-ci.org/NeuralEnsemble/libNeuroML.png)](https://travis-ci.org/NeuralEnsemble/libNeuroML)
