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

Any dynamical components (channels, synapses, abstract cell models) in `NeuroML v2.0`_ will have a definition "behind the scenes" in `LEMS`_.
However, all NeuroML files specify is that "element segment will contain element distal with attributes x, y, z,
diameter..." or "element izhikevichCell will have attributes a, b, c...".

For more on NeuroML 2 and LEMS see `here <http://www.neuroml.org/lems_dev>`_.


Serialisations
--------------

The XML serialisation will be the "natural" serialisation and will follow closely the NeuroML
object model. The format of the XML will be specified by the XML Schema definition (XSD file). Note: 
LEMS definitions of NeuroML ComponentTypes (defining what izhikevichCell does with a, b, c...)
and this XSD file (only saying the izhikevichCell element requires a, b, c...) are currently manually kept in line.

Other serialisations have been developed (HDF5, JSON, SWC). See 
`Vella et al. 2014 <http://journal.frontiersin.org/Journal/10.3389/fninf.2014.00038/abstract>`_ for more details.




.. _NeuroML v2.0: http://docs.neuroml.org
.. _LEMS: http://lems.github.io/LEMS/
.. _NeuroHDF: http://neurohdf.readthedocs.org/en/latest/

