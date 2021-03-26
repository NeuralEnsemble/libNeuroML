========
Examples
========

The examples in this section are intended to give in depth overviews of how to accomplish 
specific tasks with libNeuroML.

These examples are located in the neuroml/examples directory and can
be tested to confirm they work by running the run_all.py script.

.. contents:: Examples

Creating a NeuroML morphology
-----------------------------

.. literalinclude:: ../neuroml/examples/morphology_generation.py

Loading and modifying a file
----------------------------

.. literalinclude:: ../neuroml/examples/loading_modifying_writing.py
 

Building a network
------------------

.. literalinclude:: ../neuroml/examples/build_network.py

Building a 3D network
---------------------

.. literalinclude:: ../neuroml/examples/build_3D_network.py
 
Ion channels
------------

.. literalinclude:: ../neuroml/examples/ion_channel_generation.py

PyNN models
-----------

.. literalinclude:: ../neuroml/examples/write_pynn.py

Synapses
--------

.. literalinclude:: ../neuroml/examples/write_syns.py

Working with JSON serialization
-------------------------------

One thing to note is that the JSONWriter, unlike NeuroMLWriter, will
serializing using array-based (Arraymorph) representation if this has
been used.

.. literalinclude:: ../neuroml/examples/json_serialization.py


Working with arraymorphs
------------------------

.. literalinclude:: ../neuroml/examples/arraymorph_generation.py

Working with Izhikevich Cells
-----------------------------

These examples were kindly contributed by Steve Marsh

.. literalinclude:: ../neuroml/examples/single_izhikevich_reader.py
.. literalinclude:: ../neuroml/examples/single_izhikevich_writer.py
