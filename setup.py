# -*- coding: utf-8 -*-

from distutils.core import setup

long_description = open("README").read()

setup(
    name = "libNeuroML",
    version = '0.1.0dev',
    packages = ['neuroml', 'neuroml.test'],
    author = "libNeuroML authors and contributors",
    author_email = "<...>",
    description = "A Python library for working with NeuroML descriptions of neuronal models",
    long_description = long_description,
    license = "BSD",
    url='https://github.com/NeuralEnsemble/libNeuroML',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering']
)



