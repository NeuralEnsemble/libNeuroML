Introduction
============

This package provides Python libNeuroML, for working with neuronal models specified in `NeuroML 2  <http://docs.neuroml.org>`_.

.. warning:: **libNeuroML targets NeuroML v2.0**

   libNeuroML targets `NeuroML v2.0`_, which is described in `Cannon et al, 2014 <http://journal.frontiersin.org/Journal/10.3389/fninf.2014.00079/abstract>`_).
   NeuroML v1.8.1 (`Gleeson et al. 2010 <http://www.ploscompbiol.org/article/info:doi/10.1371/journal.pcbi.1000815>`_) is now deprecated and not supported by libNeuroML.

For a detailed description of libNeuroML see :cite:t:`Vella2014`.
*Please cite the paper if you use libNeuroML.*

NeuroML
-------

NeuroML provides an object model for describing neuronal morphologies, ion channels, synapses and 3D network structure.
For more information on NeuroML 2 and LEMS please see the `NeuroML documentation <https://docs.neuroml.org/Userdocs/NeuroMLv2.html>`_.


Serialisations
--------------

The XML serialisation will be the "natural" serialisation and will follow closely the NeuroML object model.
The format of the XML will be specified by the XML Schema definition (XSD file).

Other serialisations have been developed (HDF5, JSON, SWC).
Please see :cite:t:`Vella2014` for more details.


.. _NeuroML v2.0: http://docs.neuroml.org
.. _LEMS: http://lems.github.io/LEMS/
.. _NeuroHDF: http://neurohdf.readthedocs.org/en/latest/
