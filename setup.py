# -*- coding: utf-8 -*-

from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

long_description = open("README.md").read()

import neuroml
version = neuroml.__version__

setup(
    data_files=[("",['neuroml/test/Purk2M9s.nml'])],
    requires=required,
    install_requires=['lxml'],
    name = "libNeuroML",
    version = version,
    packages = ['neuroml', 'neuroml.test','neuroml.nml'],
    package_data = {'neuroml.test': ['*.nml'], 'neuroml.nml': ['*.xsd']},
    author = "libNeuroML authors and contributors",
    author_email = "vellamike@gmail.com",
    description = "A Python library for working with NeuroML descriptions of neuronal models",
    long_description = long_description,
    license = "BSD",
    url="http://libneuroml.readthedocs.org/en/latest/",
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering']
)
