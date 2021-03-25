Multicompartmental Python API Meeting
=====================================

Organisation
------------

Dates: 25 & 26 June 2012

Location: Room 336, Rockefeller building, UCL, London

Attendees: Sandra Berger, Andrew Davison, Padraig Gleeson, Mike Hull, Steve Marsh, Michele Mattioni, Eugenio Piasini, Mike Vella

Sponsors: This meeting was generously supported by the `INCF Multi Scale Modelling Program <http://www.incf.org/programs/modeling>`_.

Minutes
-------

Agreeing on terminology (segments, etc.) & scope
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An introduction to the background to the project and the projected scope is here:

:doc:`scope_of_project`

A discussion on the definitions of the key terms Node, Segment and Section is here, and was the basis for discussions on
these definitions at the meeting:

:doc:`nodes_segments_sections`

**Agreements**

The Python libNeuroML API will use Node as a key building block for morphologies.

Segment is agreed on as the basis for defining morphologies in NeuroML and will be a top level object in libNeuroML,
where it will be
the part of a neurite between two Nodes (proximal & distal).

Segment Group will be the basis for the grouping of these, and will be used to define dendrites, axons, etc.

Section is a term for the cable-like building block in NEURON, and will not be formally used in NeuroML or libNeuroML.

There was a discussion on whether it would be useful to be able to include this concept "by the back door" to enable
lossless import & export of morphologies from NEURON. Padraig's proposal was to add an attribute (e.g. primary) to the
segmentGroup element to flag a core set of non overlapping segmentGroups, which are continuous (all children are
connected to distal point of parent) which would correspond to the old "cable" concept in NeuroML v1.x.

There was much discussion on the usefulness of this concept and whether it should be a different element/object in the
API from segmentGroup. The outcome was not fully resolved, but as a first test of this concept, Padraig will add the
new attribute to NeuroML, Mike V will add a flag (boolean?) to the API, and at a later point, when the API begins to
interact with native simulators, we can reevaluate the usefulness of the term.



Mike Vella's current implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is under development at: https://github.com/NeuralEnsemble/libNeuroML/tree/master/neuroml

Mike will continue on this (almost) full time for the next 2 months.

Following the meeting, he will perform a refactoring operation on the code base to better reflect the names used in NeuroML, e.g.

    neuroml_doc

        cells

            morphology # not entirely sure how this works- contains segment groups and is itself a segment group?

                segments

                segment_groups

                    segment_groups

            biophysical_properties

            notes

        morphologies

        networks

        point currents

        ion channels

        synapses

        extracellular properties

It was also decided that certain SegmentGroup names should have reserved names in libNeuroML, the exact implementation of this is undecided:

Segment groups with reserved names:
    |    soma_group
    |    axon_group
    |    apical_dendrite_group
    |    basal_dendrite_group

It was also decided that a segment should only be able to connect to the root of a morphology, the syntax should be something along the lines of:

segment can only connect to root of a morphology

    connect syntax examples:

        morph2.attach(2,cell2,0.5) (default frac along = None)

        and:

        morph[2].attach(cell2,0.5)

Mike V was asked to add a clone method to a morphology.

It was decided that fraction_along should be a property of segment.

The syntax for segment groups should be as follows:
group=morph.segment_groups['axon_group'] 
(in connect merge groups should be false by default - throw an exception, tell the user setting merge_groups = True or rename group will fix this)

This was a subject of great debate and has not been completely settled.

Morphforge latest developments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mike Hull gave a brief overview of the latest developments with Morphforge:

https://github.com/mikehulluk/morphforge

He pointed out that it's still undergoing refactoring, but it can be used by other interested parties, and there is
detailed documentation online regarding installation, examples, etc.

Neuronvisio latest developments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Michele Mattioni gave a status update on Neuronvisio:

http://neuronvisio.org

The application has been closely linked to the NEURON simulator but hopefully use of libNeuroML will allow it to be used independently of
NEURON.

Michele showed Neuronvisio's native HDF5 format as just one possible way to encode model structure + simulation results:
https://github.com/NeuralEnsemble/libNeuroML/blob/master/hdf5Examples/Neuronvisio_medium_cell_example_10ms.h5


Current Python & NeuroML support in MOOSE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Skype call/Google Hangout was held on Tues at 9:30 to get an update from Bangalore.

The slides from this discussion are here:

https://github.com/NeuralEnsemble/libNeuroML/blob/master/doc/2012_06_26_neuroml_with_pymoose.pdf

As outlined there there are a number of areas in which MOOSE and Moogli import/export NeuroML version 1.x. A number of issues
and desired features missing in v1.x were highlighted, most of which are implemented or planned for NeuroML v2.0.

There was general enthusiasm about the libNeuroML project, and it was felt that MOOSE should eventually transition to
using libNeuroML to import NeuroML models. This will happen in parallel with updating of the MOOSE PyNN implementation.

The MOOSE developers were also keen to see how the new ComponentTypes in NeuroML 2 will map to inbuilt objects in MOOSE
(e.g. Integrate-and-Fire neurons, Markov channel, Izhikevich). They will add simple examples to the latest MOOSE code to
demonstrate their current implementation and discussion can continue on the mailing lists.

Saving to & loading from XML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There was not any detailed discussion on the various strategies for reading/saving XML in Python.

Padraig's suggestion based on `generateDS.py <http://www.rexx.com/~dkuhlman/generateDS.html>`_: https://github.com/NeuralEnsemble/libNeuroML/tree/master/ideas/padraig/generatedFromV2Schema
produces a very big file, which while usable as an API, e.g. see:

https://github.com/NeuralEnsemble/libNeuroML/blob/master/hhExample/hh_NEUROML2.py

could do with a lot of refactoring. It was felt that a version of this with a very efficient description of morphologies (and network instances)
based on the current work of Mike V is the way forward.

Storing simulation data as HDF5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The examples at: https://github.com/NeuralEnsemble/libNeuroML/tree/master/hdf5Examples have been updated.

The long term aim would be to arrive at a common format here that can be saved by simulators and that
visualisation packages like Moogli and Neuronvisio can read and display. This may be based on Neo: http://packages.python.org/neo/,
but that package's current lack of ability to deal with data with nonuniform time points (e.g. produced by variable time step
simulations) may be a limiting factor.


General PyNN & NeuroML v2.0 interoperability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There was agreement that libNeuroML will form the basis of the multicompartmental neuron support in PyNN. The extra functionality needed
to interact with simulators is currently termed "Pyramidal", but this will eventually be fully merged into PyNN.

http://neuralensemble.org/trac/PyNN
http://www.neuroml.org/NeuroML2CoreTypes/PyNN.html
http://www.neuroml.org/pynn.php