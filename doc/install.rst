Installation
============

Using Pip
----------

On most systems with a Python installation, libNeuroML can be installed using the default Python package manager, Pip:

::

    pip install libNeuroML

It is recommended to use a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ when installing Python packages using `pip` to prevent these from conflicting with other system libraries.

This will support the default XML serialization.
To install all of requirements to include the other serialisations, use

::

    # On Ubuntu based systems
    sudo apt-get install libhdf5-dev
    pip install libNeuroML[full]

The ``apt`` line is required at time of writing because PyTables' wheels for python 3.7 depend on the system libhdf5.


On Fedora based systems
------------------------

On `Fedora <https://getfedora.org>`_ Linux systems, the `NeuroFedora <https://neuro.fedoraproject.org>`_ community provides libNeuroML in the `standard Fedora repos <https://src.fedoraproject.org/rpms/python-libNeuroML>`_ and can be installed using the following commands:

::

    sudo dnf install python3-libNeuroML


Install from source
--------------------

You can clone the `GitHub repository <https://github.com/NeuralEnsemble/libNeuroML/>`_ and also build libNeuroML from the sources.
For this, you will need `git`_:

::

    git clone git://github.com/NeuralEnsemble/libNeuroML.git
    cd libNeuroML


More details about the git repository and making your own branch/fork are `here <how_to_contribute.html>`_.
To build and install libNeuroML, you can use the standard install method for Python packages (preferably in a virtual environment):

::

    python setup.py install

To use the **latest development version of libNeuroML**, switch to the development branch:

::

    git checkout development
    sudo python setup.py install


Run an example
--------------

Some sample scripts are included in `neuroml/examples`, e.g. :

::

    cd neuroml/examples
    python build_network.py

The standard examples can also be found :doc:`examples`.

Unit tests
----------

To run unit tests cd to the directory `neuroml/test` and use the Python unittest module discover method:

::

    cd neuroml/test/
    python -m unittest discover

If all tests passed correctly, your output should look something like this:

::

    .......
    ----------------------------------------------------------------------
    Ran 55 tests in 40.1s
    
    OK

You can also use PyTest to run tests.

::

    pip install pytest
    pytest -v --strict -W all


To ignore some tests, like the MongoDB test which requires a MongoDB setup, run:

::

    pytest -v -k "not mongodb" --strict -W all


.. _Git: https://git-scm.com
