"""
Unit tests for cells

"""

import os

import neuroml
from neuroml import (
    Cell,
    Include,
    Member,
    Morphology,
    Point3DWithDiam,
    Segment,
    SegmentGroup,
    SegmentParent,
    loaders,
)

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestCell(unittest.TestCase):
    def test_cell_methods(self):
        cells = ["Purk2M9s", "pyr_4_sym.cell"]

        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            cell = doc.cells[0]
            self.assertEqual(cell.id, cell_name.split(".")[0])

            exp_num_segs = 9
            self.assertEqual(cell.morphology.num_segments, exp_num_segs)
            self.assertEqual(len(cell.get_segment_ids_vs_segments()), exp_num_segs)
            self.assertRaises(
                Exception, lambda: cell.get_segment(-1)
            )  # Seg -1 doesn't exist...

            cell.summary()

            # cell.get_ordered_segments_in_groups = get_ordered_segments_in_groups

            for grp in [
                "soma_group",
                ["soma_group", "basal_dends"],
                ["dendrite_group"],
                ["all"],
            ]:
                print("-----------------------------")
                print("   Testing %s..." % grp)

                segs, cuml, path_prox, path_dist = cell.get_ordered_segments_in_groups(
                    grp,
                    check_parentage=(grp == ["all"]),
                    include_cumulative_lengths=True,
                    include_path_lengths=True,
                )

                print("Segs %s: %s" % (grp, segs))
                print("Cuml %s: %s" % (grp, cuml))
                print("Prox %s: %s" % (grp, path_prox))
                print("Dist %s: %s" % (grp, path_dist))

                for s in segs:
                    assert len(segs[s]) == len(cuml[s])
                    ##assert len(segs[s])==len(path_prox[s])
                    ##assert len(segs[s])==len(path_dist[s])

                if grp == "soma_group":
                    assert len(segs["soma_group"]) == 1
                    soma_len = cuml["soma_group"][-1]
                    print("soma_len: %s" % soma_len)

                if grp == ["all"]:
                    assert len(segs["all"]) == 9
                    all_len = cuml["all"][-1]

                if grp == ["dendrite_group"]:
                    assert len(segs["dendrite_group"]) == 8
                    dend_len = cuml["dendrite_group"][-1]
                    print("dend_len: %s" % dend_len)

            assert all_len == soma_len + dend_len

    def test_cell_methods2(self):
        cell = Cell(id="cell0")

        diam = 1.0
        d0 = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)

        seg0 = Segment(id=0, name="soma", proximal=p, distal=d0)

        d1 = Point3DWithDiam(x=10, y=0, z=0, diameter=diam)

        cell.morphology = Morphology()
        cell.morphology.segments.append(seg0)

        seg1 = Segment(id=1, distal=d1, parent=SegmentParent(segments=0))
        cell.morphology.segments.append(seg1)

        d2 = Point3DWithDiam(x=20, y=0, z=0, diameter=diam)

        seg2 = Segment(
            id=2, proximal=d1, distal=d2, parent=SegmentParent(segments=seg1.id)
        )
        cell.morphology.segments.append(seg2)

        d3 = Point3DWithDiam(x=20, y=10, z=0, diameter=diam)

        seg3 = Segment(
            id=3, distal=d3, parent=SegmentParent(segments=seg2.id, fraction_along=1)
        )
        cell.morphology.segments.append(seg3)

        sg1 = SegmentGroup(id="all")
        for seg in [seg0, seg1, seg2, seg3]:
            sg1.members.append(Member(segments=seg.id))
        cell.morphology.segment_groups.append(sg1)

        sg2 = SegmentGroup(id="soma_group")
        for seg in [seg0]:
            sg2.members.append(Member(segments=seg.id))
        cell.morphology.segment_groups.append(sg2)

        sg3 = SegmentGroup(id="dend_group")
        for seg in [seg1, seg2, seg3]:
            sg3.members.append(Member(segments=seg.id))
        cell.morphology.segment_groups.append(sg3)

        sg4 = SegmentGroup(id="soma_dends")
        for sg in [sg2, sg3]:
            sg4.includes.append(Include(segment_groups=sg.id))
        cell.morphology.segment_groups.append(sg4)

        expected = {sg1.id: 4, sg2.id: 1, sg3.id: 3, sg4.id: 4}

        for sg in [sg1, sg2, sg3, sg4]:
            segs = cell.get_all_segments_in_group(sg.id)
            print("\nSeg group %s has segments: %s" % (sg, segs))
            self.assertEqual(expected[sg.id], len(segs))

            osegs = cell.get_ordered_segments_in_groups(sg.id)
            print("Seg group %s has ordered segments: %s" % (sg.id, osegs))
            self.assertEqual(expected[sg.id], len(osegs[sg.id]))

            (
                ord_segs,
                cumulative_lengths,
                path_lengths_to_proximal,
                path_lengths_to_distal,
            ) = cell.get_ordered_segments_in_groups(
                sg.id, include_cumulative_lengths=True, include_path_lengths=True
            )

            print(
                "Seg group %s has cumulative_lengths: %s" % (sg.id, cumulative_lengths)
            )
            self.assertEqual(expected[sg.id], len(cumulative_lengths[sg.id]))

            print(
                "Seg group %s has path_lengths_to_proximal: %s"
                % (sg.id, path_lengths_to_proximal)
            )
            self.assertEqual(expected[sg.id], len(path_lengths_to_proximal[sg.id]))

            print(
                "Seg group %s has path_lengths_to_distal: %s"
                % (sg.id, path_lengths_to_distal)
            )
            self.assertEqual(expected[sg.id], len(path_lengths_to_distal[sg.id]))

    def test_adjacency_list(self):
        """test get_segment_adjacency_list method"""
        cells = ["Purk2M9s", "pyr_4_sym.cell"]

        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            cell = doc.cells[0]  # type: neuroml.Cell
            self.assertEqual(cell.id, cell_name.split(".")[0])

            adlist = cell.get_segment_adjacency_list()
            self.assertIn(1, adlist[0])
            self.assertIn(7, adlist[6])
            self.assertIn(5, adlist[1])

    def test_cell_graph(self):
        """test get_graph method"""
        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            acell = doc.cells[0]  # type: neuroml.Cell
            self.assertEqual(acell.id, cell_name.split(".")[0])

            graph = acell.get_graph()
            print(graph)

    def test_get_distance(self):
        """test distance method"""
        cells = ["Purk2M9s", "pyr_4_sym.cell"]

        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            acell = doc.cells[0]  # type: neuroml.Cell
            self.assertEqual(acell.id, cell_name.split(".")[0])

            distance1 = acell.get_distance(dest=1)
            distance2 = acell.get_distance(dest=2)
            distance3 = acell.get_distance(dest=3)
            distance4 = acell.get_distance(dest=4)
            print(distance1, distance2, distance3, distance4)

            all_distances = acell.get_all_distances_from_segment()
            print(all_distances)

    def test_get_all_segments_at_distance(self):
        """test distance method"""
        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            acell = doc.cells[0]  # type: neuroml.Cell
            self.assertEqual(acell.id, cell_name.split(".")[0])

            distance1 = acell.get_distance(dest=1)
            distance2 = acell.get_distance(dest=2)
            distance3 = acell.get_distance(dest=3)
            distance4 = acell.get_distance(dest=4)
            print(distance1, distance2, distance3, distance4)

            adict = acell.get_segments_at_distance(distance=500)
            self.assertIn(3, list(adict.keys()))

    def test_get_branching_points(self):
        """test get_branching_points"""
        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            acell = doc.cells[0]  # type: neuroml.Cell
            self.assertEqual(acell.id, cell_name.split(".")[0])

            res = acell.get_branching_points()
            self.assertIn(0, res)
            self.assertIn(1, res)
            self.assertIn(6, res)
            print(res)

    def test_get_extremeties(self):
        """test get_extremeties"""
        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            acell = doc.cells[0]  # type: neuroml.Cell
            self.assertEqual(acell.id, cell_name.split(".")[0])

            res = acell.get_extremeties()
            keys = list(res.keys())
            self.assertIn(4, keys)
            self.assertIn(5, keys)
            self.assertIn(7, keys)
            self.assertIn(8, keys)
            print(res)

    def test_locate_segment(self):
        """test locate_segment method"""
        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            acell = doc.cells[0]  # type: neuroml.Cell
            self.assertEqual(acell.id, cell_name.split(".")[0])

            res = acell.get_segment_location_info(4)
            self.assertEqual("apical4", res["in_unbranched_segment_group"])
            self.assertEqual(0, res["distance_from_segment_group_root"])

    def test_get_morphology_root(self):
        """Test get_morphology_root method"""
        cells = ["pyr_4_sym"]

        for cell_name in cells:
            local_path = "../examples/test_files/%s.cell.nml" % cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(
                    root_dir, "examples/test_files/%s.cell.nml" % cell_name
                )
            print("test file path is: " + test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            acell = doc.cells[0]  # type: neuroml.Cell

            root = acell.get_morphology_root()
            self.assertEqual(0, root)

            # change the id and confirm if we get the new one
            root_seg = acell.get_segment(0)
            new_id = 99999
            root_seg.id = new_id
            # also update all descendents to ensure cell remains valid
            for seg in acell.morphology.segments:
                par = seg.parent
                if par is not None:
                    if par.segments == 0:
                        par.segments = new_id

            new_root = acell.get_morphology_root()
            self.assertEqual(new_id, new_root)

    def runTest(self):
        print("Running tests in TestCell")


if __name__ == "__main__":
    ta = TestCell()

    ta.test_cell_methods()
    ta.test_cell_methods2()
