Nodes, Segments and Sections
============================

An attempt to clarify these interrelated terms used in describing morphologies. Names in **bold type** are used for elements of the
NeuroML object model.

Nodes
-------

A node is a 3D point with diameter information which forms the basis for 3D morphological reconstructions.

These nodes (or points) are the fundamental building blocks in the SWC and Neurolucida formats. This method of description
is based on the assumption that each node is physically connected to another node.



Segments
--------------

A **segment** (according to NeuroML v1&2) is a part of a neuronal tree between two 3D points with diameters (**proximal** & **distal**).
The term node isn't used in NeuroML but the above description describes perfectly well the **proximal** & **distal** points.
Cell **morphology** elements consist of lists of **segments** (each with unique integer id, and optional name).

All segments, apart from the root segment, have a **parent** segment. If the **proximal** point of the segment is not specified,
the **distal** point of the parent segment is used for the **proximal** point of the child.

A special case is defined where **proximal** == **distal**, and the **segment** is assumed to be a sphere at that location
with the specified diameter.

Segments can be grouped into **segmentGroups** in NeuroML v2.0. These can be used to specify "apical_dendrites", "axon_group",
etc., which in turn can be used for placing channels on the cell.

An example of a NeuroML v2.0 cell is `here <http://sourceforge.net/apps/trac/neuroml/browser/NeuroML2/examples/NML2_SimpleMorphology.nml>`_.

libNeuroML will allow low level access to create and modify morphologies by handling nodes. Segments will also be top
level objects in the API. The XML serialisation will only specify **segments** with **proximal** & **distal** points, but
the HDF5 version may have an efficient serialisation of nodes & segments.


Sections
--------

The concept of section is fundamentally important in NEURON. A section in this simulator is an unbranched cable which can have multiple
3D points outlining the structure of a neurite in 3D. These points are used to determine the surface area along the section. NEURON
can vary the spatial discretisation of the neurite by varying the "nseg" value of the section, e.g. a section with 20 3D
points and nseg =4 will be split into 4 parts of equal length for simulating (as isopotential compartments), with the surface area (and so total channel
conductance) of each determined by the set of 3D points in that part.

There was a similar concept to this in NeuroML v1.x, the **cable**. Each **segment** had an attribute for the cable id, and these were used for mapping
to and from NEURON. Cables were unbranched, and so all segments after the first in the cable only had distal points, see
`this example <http://www.neuroml.org/NeuroMLValidator/ViewNeuroMLFile.jsp?localFile=NeuroMLFiles/Examples/ChannelML/PyramidalCell.xml>`_.

The cable concept was removed in NeuroML v2.0, as this is was seen as imposing concepts from compartmental modelling
on the basic morphological descriptions of cells. There is only a **segmentGroup** element for grouping segments, though
a **segment** can belong to multiple **segmentGroups**, which don't need to be unbranched (unlike **cables**). There may need to be a
new attribute in **segmentGroup** (e.g. primary or unbranched or cable="true") which defines a nonoverlapping set of
unbranched segmentGroups, which can be used as the basis for sections in any parsing application which is interested
in them, or be ignored by any other application.

In libNeuroML, a section-like concept can be added at API level, to facilitate building cells, to facilitate import/export
to/from simulators supporting this concept, and to serve as a basis for recompartmentalisation of cells. 



Issues
------

Dendrites in space
~~~~~~~~~~~~~~~~~~

One major issue to address is that in many neuronal reconstructions, the soma is not included (or perhaps just an outline
of the soma is given), only the dendrites are. These dendrites' 3D start points are on the edge of the soma membrane "floating in space".
Normal procedure for a modeller in this case is to create a spherical soma at this central point and electrically attach the
dendrites to the centre of this.

In this case (and many others) the physical location of the start of the child segments do not correspond to the electrical (or logical)
connection point on the parent. This has advantages and disadvantages:

(+) It allows the real 3D points of the neuronal reconstruction to be retained (useful for visualisation)

(-) This is not unambiguously captured in the simplest morphological formats like SWC, which assume physical connectivity between nodes/points

This scenario is supported in NeuroML v1&2, where a child **segment** has the option to redefine its start point (by adding a **proximal**)
with the child <-> parent relationship defining the electrical connection. This allows lossless import & export from NEURON and
removes the ambiguity of more compact formats like SWC and Neurolucida.

Connections mid segment
~~~~~~~~~~~~~~~~~~~~~~~

Another option for electrical connections (also influences by NEURON sections) is the ability for **segments** to
(electrically/logically) connect to a point inside a **segment**. This is specified by adding a fractionAlong attribute
to the **parent** element, i.e.

::

    <parent segment="2" fractionAlong="0.5"/>

This is not possible in a node based format, but represents a logically consistent description of what the modeller
wants. 


What to do?
~~~~~~~~~~~

Two options are available then for a serialisation format or API: should it try to support all of these scenarios, or try to
enforce "best practice"?

PG: I'd argue for the first approach, as it retains as much as possible of what the original reconstructor/simulator specified.
An API which enforces a policy when it encounters a non optimal morphology (e.g. moving all dendrites to connection points,
inserting new nodes) will alter the original data in perhaps unintended ways, and that information will be lost by subsequent readers.
It should be up to each parsing application to decide what to do with the extra information when it reads in a file.