# -*- coding: utf-8 -*-

from setuptools import setup

long_description = open("README.md").read()

for line in open("neuroml/__version__.py"):
    if line.startswith("__version__"):
        version = line.split("=")[1].strip()[1:-1]

setup(
    name="libNeuroML",
    version=version,
    packages=["neuroml", "neuroml.test", "neuroml.nml", "neuroml.hdf5"],
    package_data={"neuroml.test": ["*.nml"], "neuroml.nml": ["*.xsd"]},
    author="libNeuroML authors and contributors",
    author_email="vellamike@gmail.com, p.gleeson@gmail.com",
    description="A Python library for working with NeuroML descriptions of neuronal models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["lxml", "six", "networkx", "numpy"],
    tests_require=["pytest"],
    extras_require={
        "full": [
            "cython",
            "numexpr",
            "tables>=3.3.0",
        ]
    },
    license="BSD",
    url="http://libneuroml.readthedocs.org/en/latest/",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering",
    ],
)
