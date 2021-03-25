Useful tools
============

Below is a list of tools which are built in or use Python and which would benefit from a standard library to access,
modify and save detailed neuronal morphologies. Developers from most of these initiatives are involved with the
libNeuroML project.

Neuronvisio
-----------

Neuronvisio is a Graphical User Interface for NEURON simulator environment with 3D capabilities.

http://neuronvisio.org (GitHub: https://github.com/mattions/neuronvisio)

PyNN
----

PyNN is a is a simulator-independent language for building neuronal network models.

http://neuralensemble.org/trac/PyNN

Morphforge
----------

A Python library for simulating small networks of multicompartmental neurons

https://github.com/mikehulluk/morphforge

CATMAID
-------

We reconstruct neuronal circuits (morphology in 3D, synaptic connectivity) as skeletons, surfaces, volumes in CATMAID.
We want to be able to export the data into an object model (data format), complement it with ion channel distribution of
several types & synaptic mechanisms, and simulate the membrane voltage time series and do virtual current injection etc.
on standard simulators. All of this with a easy-to-use, intuitive Python API in a few lines of code.

http://www.catmaid.org

NEURON
------

A widely used simulation platform for biophysically detailed neurons and networks which has recently added a Python interface.

http://www.neuron.yale.edu/neuron

For more information on Python & NEURON, see Andrew Davison's guide here: http://www.davison.webfactional.com/notes/installation-neuron-python/

MOOSE & Moogli
--------------

MOOSE is the Multiscale Object-Oriented Simulation Environment. It is the base and numerical core for large, detailed simulations including Computational Neuroscience and Systems Biology.

http://moose.sourceforge.net

**PyMOOSE**


The latest version of MOOSE with a Python interface can be installed as follows:

::

    svn co http://moose.svn.sourceforge.net/svnroot/moose/moose/branches/dh_branch moose
    cd moose
    make pymoose
    sudo cp -r python/moose /usr/lib/python2.7/dist-packages

replacing `/usr/lib/python2.7/dist-packages` with the appropriate location for your Python packages. More details can be found `here <http://moose.sourceforge.net/component/option%2ccom_wrapper/Itemid%2c86/index.html>`_.

An example of the HH squid mode can be run with:

::

    cd Demos/squid/
    python squid_demo.py 

**Moogli**

Moogli (a sister project of MOOSE) is a simulator independent OpenGL based visualization tool for neural simulations.
Moogli can visualize morphology of single/multiple neurons or network of neurons, and can also visualize activity in these cells.

http://moose.ncbs.res.in/moogli/


neuroConstruct
--------------

neuroConstruct generates native simulator code for NEURON, MOOSE and other simulators. It would be a great benefit to be
able to generate pure NeuroML descriptions of the model components and run (nearly) identical Python code on these
simulators to load the NeuroML and execute the simulations. This scenario is implemented already for a limited number of
model types by generating PyNN based scripts which can run on NEURON, Brian and NEST.

http://www.neuroConstruct.org
