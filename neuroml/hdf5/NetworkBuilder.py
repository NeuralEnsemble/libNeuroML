#
#
#   A class which stores the contents of a NeuroML file in libNeuroML classes
#   Used mainly to convert HDF5 representations of NeuroML to internal libNeuroML format
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council & Wellcome Trust
#
#

import logging
import sys

sys.path.append("../NeuroMLUtils")

import neuroml
from neuroml.hdf5.DefaultNetworkHandler import DefaultNetworkHandler


class NetworkBuilder(DefaultNetworkHandler):
    log = logging.getLogger("NetworkBuilder")

    populations = {}
    projections = {}
    projection_syns = {}
    projection_types = {}
    projection_syns_pre = {}
    input_lists = {}

    weightDelays = {}

    def get_nml_doc(self):
        return self.nml_doc

    #
    #  Overridden from DefaultNetworkHandler
    #
    def handle_document_start(self, id, notes):
        self.nml_doc = neuroml.NeuroMLDocument(id=id)
        if notes and len(notes) > 0:
            self.nml_doc.notes = notes

    #
    #  Overridden from DefaultNetworkHandler
    #
    def handle_network(self, network_id, notes, temperature=None):
        self.network = neuroml.Network(id=network_id)
        self.nml_doc.networks.append(self.network)
        if notes and len(notes) > 0:
            self.network.notes = notes
        if temperature is not None:
            self.network.temperature = temperature
            self.network.type = "networkWithTemperature"

    #
    #  Overridden from DefaultNetworkHandler
    #
    def handle_population(
        self,
        population_id,
        component,
        size,
        component_obj=None,
        properties={},
        notes=None,
    ):
        if component_obj:
            self.nml_doc.append(component_obj)

        pop = neuroml.Population(id=population_id, component=component, size=size)

        if notes and len(notes) > 0:
            pop.notes = notes

        self.populations[population_id] = pop
        self.network.populations.append(pop)
        for p in properties:
            pop.properties.append(neuroml.Property(tag=p, value=properties[p]))

        comp_obj_info = " (%s)" % type(component_obj) if component_obj else ""

        if size >= 0:
            sizeInfo = ", size " + str(size) + " cells"
            self.log.debug(
                "Creating population: "
                + population_id
                + ", cell type: "
                + component
                + comp_obj_info
                + sizeInfo
            )
        else:
            self.log.error(
                "Population: "
                + population_id
                + ", cell type: "
                + component
                + comp_obj_info
                + " specifies no size. May lead to errors!"
            )

    #
    #  Overridden from DefaultNetworkHandler
    #
    def handle_location(self, id, population_id, component, x, y, z):
        ##print('Loc: %s %s (%s,%s,%s)'%(id, population_id, x, y, z))
        self.print_location_information(id, population_id, component, x, y, z)

        if x is not None and y is not None and z is not None:
            inst = neuroml.Instance(id=id)

            inst.location = neuroml.Location(x=x, y=y, z=z)
            self.populations[population_id].instances.append(inst)
            self.populations[population_id].type = "populationList"
        else:
            self.log.warning(
                "Ignoring location: %s %s (%s,%s,%s)" % (id, population_id, x, y, z)
            )

    #
    #  Overridden from DefaultNetworkHandler
    #
    def handle_projection(
        self,
        id,
        prePop,
        postPop,
        synapse,
        hasWeights=False,
        hasDelays=False,
        type="projection",
        synapse_obj=None,
        pre_synapse_obj=None,
    ):
        if synapse_obj:
            self.nml_doc.append(synapse_obj)
        if pre_synapse_obj:
            self.nml_doc.append(pre_synapse_obj)

        proj = None

        if type == "projection":
            proj = neuroml.Projection(
                id=id,
                presynaptic_population=prePop,
                postsynaptic_population=postPop,
                synapse=synapse,
            )
            self.network.projections.append(proj)
        elif type == "electricalProjection":
            proj = neuroml.ElectricalProjection(
                id=id, presynaptic_population=prePop, postsynaptic_population=postPop
            )
            self.network.electrical_projections.append(proj)
            self.projection_syns[id] = synapse
        elif type == "continuousProjection":
            proj = neuroml.ContinuousProjection(
                id=id, presynaptic_population=prePop, postsynaptic_population=postPop
            )
            self.network.continuous_projections.append(proj)

            if synapse_obj != None:
                self.projection_syns[id] = synapse_obj.id
            else:
                self.projection_syns[id] = synapse

            if pre_synapse_obj == None:
                pre_synapse_obj = neuroml.SilentSynapse(id="silentSyn_%s" % id)
                self.nml_doc.silent_synapses.append(pre_synapse_obj)

            self.projection_syns_pre[id] = pre_synapse_obj.id

        self.projections[id] = proj
        self.projection_types[id] = type
        self.weightDelays[id] = hasWeights or hasDelays

        self.log.debug(
            "Projection: %s (%s) from %s to %s with syn: %s, weights: %s, delays: %s"
            % (id, type, prePop, postPop, synapse, hasWeights, hasDelays)
        )

    #
    #  Overridden from DefaultNetworkHandler
    #
    def finalise_projection(self, id, prePop, postPop, synapse=None, type=None):
        """
        Check whether handle_projection was not called, e.g. due to no connections present
        """
        if type == None:
            type = self.projection_types[id]

        self.log.debug(
            "Projection: %s (%s) from %s to %s completed" % (id, type, prePop, postPop)
        )

        if type == "projection":
            present = False
            for p in self.network.projections:
                if p.id == id:
                    present = True
            if not present:
                proj = neuroml.Projection(
                    id=id,
                    presynaptic_population=prePop,
                    postsynaptic_population=postPop,
                    synapse=synapse,
                )
                self.network.projections.append(proj)
        elif type == "electricalProjection":
            present = False
            for p in self.network.electrical_projections:
                if p.id == id:
                    present = True
            if not present:
                proj = neuroml.ElectricalProjection(
                    id=id,
                    presynaptic_population=prePop,
                    postsynaptic_population=postPop,
                )
                self.network.electrical_projections.append(proj)

    #
    #  Overridden from DefaultNetworkHandler
    #
    #  Assumes delay in ms
    #
    def handle_connection(
        self,
        proj_id,
        conn_id,
        prePop,
        postPop,
        synapseType,
        preCellId,
        postCellId,
        preSegId=0,
        preFract=0.5,
        postSegId=0,
        postFract=0.5,
        delay=0,
        weight=1,
    ):
        # self.printConnectionInformation(proj_id, conn_id, prePop, postPop, synapseType, preCellId, postCellId, weight)

        pre_cell_path = "../%s/%i/%s" % (
            prePop,
            preCellId,
            self.populations[prePop].component,
        )
        if self.populations[prePop].type == None:
            pre_cell_path = "../%s[%i]" % (prePop, preCellId)

        post_cell_path = "../%s/%i/%s" % (
            postPop,
            postCellId,
            self.populations[postPop].component,
        )
        if self.populations[postPop].type == None:
            post_cell_path = "../%s[%i]" % (postPop, postCellId)

        if isinstance(self.projections[proj_id], neuroml.ElectricalProjection):
            instances = False
            if (
                len(self.populations[prePop].instances) > 0
                or len(self.populations[postPop].instances) > 0
            ):
                instances = True

            if not instances:
                conn = neuroml.ElectricalConnection(
                    id=conn_id,
                    pre_cell="%s" % (preCellId),
                    pre_segment=preSegId,
                    pre_fraction_along=preFract,
                    post_cell="%s" % (postCellId),
                    post_segment=postSegId,
                    post_fraction_along=postFract,
                    synapse=self.projection_syns[proj_id],
                )

                self.projections[proj_id].electrical_connections.append(conn)

            else:
                if weight == 1:
                    conn = neuroml.ElectricalConnectionInstance(
                        id=conn_id,
                        pre_cell=pre_cell_path,
                        pre_segment=preSegId,
                        pre_fraction_along=preFract,
                        post_cell=post_cell_path,
                        post_segment=postSegId,
                        post_fraction_along=postFract,
                        synapse=self.projection_syns[proj_id],
                    )

                    self.projections[proj_id].electrical_connection_instances.append(
                        conn
                    )
                else:
                    conn = neuroml.ElectricalConnectionInstanceW(
                        id=conn_id,
                        pre_cell=pre_cell_path,
                        pre_segment=preSegId,
                        pre_fraction_along=preFract,
                        post_cell=post_cell_path,
                        post_segment=postSegId,
                        post_fraction_along=postFract,
                        synapse=self.projection_syns[proj_id],
                        weight=weight,
                    )

                    self.projections[proj_id].electrical_connection_instance_ws.append(
                        conn
                    )

        elif isinstance(self.projections[proj_id], neuroml.ContinuousProjection):
            instances = False
            if (
                len(self.populations[prePop].instances) > 0
                or len(self.populations[postPop].instances) > 0
            ):
                instances = True

            if not instances:
                if weight != 1:
                    raise Exception(
                        "Case not (yet) supported: weight!=1 when not an instance based population..."
                    )

                conn = neuroml.ContinuousConnection(
                    id=conn_id,
                    pre_cell="%s" % (preCellId),
                    pre_segment=preSegId,
                    pre_fraction_along=preFract,
                    post_cell="%s" % (postCellId),
                    post_segment=postSegId,
                    post_fraction_along=postFract,
                    pre_component=self.projection_syns_pre[proj_id],
                    post_component=self.projection_syns[proj_id],
                )

                self.projections[proj_id].continuous_connections.append(conn)

            else:
                if weight == 1:
                    conn = neuroml.ContinuousConnectionInstance(
                        id=conn_id,
                        pre_cell=pre_cell_path,
                        pre_segment=preSegId,
                        pre_fraction_along=preFract,
                        post_cell=post_cell_path,
                        post_segment=postSegId,
                        post_fraction_along=postFract,
                        pre_component=self.projection_syns_pre[proj_id],
                        post_component=self.projection_syns[proj_id],
                    )

                    self.projections[proj_id].continuous_connection_instances.append(
                        conn
                    )
                else:
                    conn = neuroml.ContinuousConnectionInstanceW(
                        id=conn_id,
                        pre_cell=pre_cell_path,
                        pre_segment=preSegId,
                        pre_fraction_along=preFract,
                        post_cell=post_cell_path,
                        post_segment=postSegId,
                        post_fraction_along=postFract,
                        pre_component=self.projection_syns_pre[proj_id],
                        post_component=self.projection_syns[proj_id],
                        weight=weight,
                    )

                    self.projections[proj_id].continuous_connection_instance_ws.append(
                        conn
                    )

        else:
            if not self.weightDelays[proj_id] and delay == 0 and weight == 1:
                connection = neuroml.Connection(
                    id=conn_id,
                    pre_cell_id=pre_cell_path,
                    pre_segment_id=preSegId,
                    pre_fraction_along=preFract,
                    post_cell_id=post_cell_path,
                    post_segment_id=postSegId,
                    post_fraction_along=postFract,
                )

                self.projections[proj_id].connections.append(connection)

            else:
                connection = neuroml.ConnectionWD(
                    id=conn_id,
                    pre_cell_id=pre_cell_path,
                    pre_segment_id=preSegId,
                    pre_fraction_along=preFract,
                    post_cell_id=post_cell_path,
                    post_segment_id=postSegId,
                    post_fraction_along=postFract,
                    weight=weight,
                    delay="%sms" % (delay),
                )

                self.projections[proj_id].connection_wds.append(connection)

    #
    #  Overridden from DefaultNetworkHandler
    #
    def handle_input_list(
        self, inputListId, population_id, component, size, input_comp_obj=None
    ):
        if input_comp_obj:
            self.nml_doc.append(input_comp_obj)

        input_list = neuroml.InputList(
            id=inputListId, component=component, populations=population_id
        )

        self.input_lists[inputListId] = input_list

        self.network.input_lists.append(input_list)

    #
    #  Overridden from DefaultNetworkHandler
    #
    def handle_single_input(
        self, inputListId, id, cellId, segId=0, fract=0.5, weight=1.0
    ):
        input_list = self.input_lists[inputListId]
        target_path = "../%s/%i/%s" % (
            input_list.populations,
            cellId,
            self.populations[input_list.populations].component,
        )

        if self.populations[input_list.populations].type == None:
            target_path = "../%s[%i]" % (input_list.populations, cellId)

        if weight == 1:
            input = neuroml.Input(id=id, target=target_path, destination="synapses")
            if segId != 0:
                input.segment_id = "%s" % (segId)
            if fract != 0.5:
                input.fraction_along = "%s" % (fract)
            input_list.input.append(input)
        else:
            input_w = neuroml.InputW(id=id, target=target_path, destination="synapses")
            if segId != 0:
                input_w.segment_id = "%s" % (segId)
            if fract != 0.5:
                input_w.fraction_along = "%s" % (fract)
            input_w.weight = weight
            input_list.input_ws.append(input_w)
