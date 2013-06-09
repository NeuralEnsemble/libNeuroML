# -*- coding: utf-8 -*-

from distutils.core import setup

long_description = open("README").read()

setup(
    data_files=[("",['neuroml/test/Purk2M9s.nml'])],
    name = "libNeuroML",
    version = '0.1.6',
    packages = ['neuroml', 'neuroml.test','neuroml.nml','neuroml.examples'],
    package_data = {'neuroml.test': ['*.nml']},
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



