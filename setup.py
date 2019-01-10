# -*- coding: utf-8 -*-

from setuptools import setup

long_description = open("README.md").read()

for line in open('neuroml/__init__.py'):
    if line.startswith("__version__"):
        version = line.split("=")[1].strip()[1:-1]

setup(
    name = "libNeuroML",
    version = version,
    packages = ['neuroml', 'neuroml.test','neuroml.nml','neuroml.hdf5'],
    package_data = {'neuroml.test': ['*.nml'], 'neuroml.nml': ['*.xsd']},
    author = "libNeuroML authors and contributors",
    author_email = "vellamike@gmail.com, p.gleeson@gmail.com",
    description = "A Python library for working with NeuroML descriptions of neuronal models",
    long_description = long_description,
    install_requires=['lxml', 'six'],
    tests_require=["nose"],
    extras_require={"full": [
        "cython",
        "numpy",
        "pymongo",
        "numexpr",
        "simplejson; python_version < '3.5'",
        "tables>=3.3.0",
        "jsonpickle>=0.9.6"
    ]},
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
