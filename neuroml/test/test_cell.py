"""
Unit tests for cells

"""

import neuroml
from neuroml import loaders

from neuroml import Segment
from neuroml import SegmentParent
from neuroml import SegmentGroup
from neuroml import Member
from neuroml import Include
from neuroml import Cell
from neuroml import Morphology
from neuroml import Point3DWithDiam

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestCell(unittest.TestCase):

    def test_cell_methods(self):

        cells = ['Purk2M9s','pyr_4_sym.cell']

        cells = ['pyr_4_sym']

        for cell_name in cells:

            local_path = '../examples/test_files/%s.cell.nml'%cell_name
            if os.path.isfile(local_path):
                test_file_path = local_path
            else:
                root_dir = os.path.dirname(neuroml.__file__)
                test_file_path = os.path.join(root_dir,'examples/test_files/%s.cell.nml'%cell_name)
            print('test file path is: '+test_file_path)

            doc = loaders.NeuroMLLoader.load(test_file_path)
            cell = doc.cells[0]
            self.assertEqual(cell.id,cell_name.split('.')[0])

            exp_num_segs = 9
            self.assertEqual(cell.morphology.num_segments,exp_num_segs)
            self.assertEqual(len(cell.get_segment_ids_vs_segments()),exp_num_segs)
            self.assertRaises(Exception, lambda: cell.get_segment(-1)) # Seg -1 doesn't exist...

            cell.summary()

            #cell.get_ordered_segments_in_groups = get_ordered_segments_in_groups

            for grp in ['soma_group', ['soma_group','basal_dends'],['dendrite_group'],['all']]:

                print("-----------------------------")
                print("   Testing %s..."%grp)

                segs, cuml, path_prox, path_dist = cell.get_ordered_segments_in_groups(
                    grp,
                    check_parentage=(grp==['all']),
                    include_cumulative_lengths=True,
                    include_path_lengths=True
                )

                print("Segs %s: %s"%(grp,segs))
                print("Cuml %s: %s"%(grp,cuml))
                print("Prox %s: %s"%(grp,path_prox))
                print("Dist %s: %s"%(grp,path_dist))

                for s in segs:
                    assert len(segs[s])==len(cuml[s])
                    ##assert len(segs[s])==len(path_prox[s])
                    ##assert len(segs[s])==len(path_dist[s])

                if grp=='soma_group':
                    assert len(segs['soma_group'])==1
                    soma_len = cuml['soma_group'][-1]
                    print("soma_len: %s"%soma_len)

                if grp==['all']:
                    assert len(segs['all'])==9
                    all_len = cuml['all'][-1]

                if grp==['dendrite_group']:
                    assert len(segs['dendrite_group'])==8
                    dend_len = cuml['dendrite_group'][-1]
                    print("dend_len: %s"%dend_len)

            assert all_len == soma_len+dend_len

    def test_cell_methods2(self):
        cell = Cell(id='cell0')

        diam = 1.
        d0=Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p=Point3DWithDiam(x=0, y=0, z=0, diameter=diam)

        seg0 = Segment(id=0, name='soma',proximal=p, distal=d0)

        d1=Point3DWithDiam(x=10, y=0, z=0, diameter=diam)

        cell.morphology = Morphology()
        cell.morphology.segments.append(seg0)

        seg1 = Segment(id=1, distal=d1, parent=SegmentParent(0))
        cell.morphology.segments.append(seg1)

        d2=Point3DWithDiam(x=20, y=0, z=0, diameter=diam)

        seg2 = Segment(id=2, proximal=d1, distal=d2, parent=SegmentParent(seg1.id))
        cell.morphology.segments.append(seg2)

        d3=Point3DWithDiam(x=20, y=10, z=0, diameter=diam)

        seg3 = Segment(id=3, distal=d3, parent=SegmentParent(seg2.id, fraction_along=1))
        cell.morphology.segments.append(seg3)

        sg1 = SegmentGroup(id='all')
        for seg in [seg0,seg1,seg2,seg3]:
            sg1.members.append(Member(seg.id))
        cell.morphology.segment_groups.append(sg1)

        sg2 = SegmentGroup(id='soma_group')
        for seg in [seg0]:
            sg2.members.append(Member(seg.id))
        cell.morphology.segment_groups.append(sg2)

        sg3 = SegmentGroup(id='dend_group')
        for seg in [seg1,seg2,seg3]:
            sg3.members.append(Member(seg.id))
        cell.morphology.segment_groups.append(sg3)

        sg4 = SegmentGroup(id='soma_dends')
        for sg in [sg2,sg3]:
            sg4.includes.append(Include(sg.id))
        cell.morphology.segment_groups.append(sg4)

        expected = {sg1.id:4,sg2.id:1,sg3.id:3,sg4.id:4}

        for sg in [sg1,sg2,sg3,sg4]:
            segs = cell.get_all_segments_in_group(sg.id)
            print('\nSeg group %s has segments: %s'%(sg,segs))
            self.assertEqual(expected[sg.id],len(segs))

            osegs = cell.get_ordered_segments_in_groups(sg.id)
            print('Seg group %s has ordered segments: %s'%(sg.id,osegs))
            self.assertEqual(expected[sg.id],len(osegs[sg.id]))

            ord_segs, cumulative_lengths, path_lengths_to_proximal, path_lengths_to_distal = cell.get_ordered_segments_in_groups(
                sg.id,
                include_cumulative_lengths=True,
                include_path_lengths=True
            )

            print('Seg group %s has cumulative_lengths: %s'%(sg.id,cumulative_lengths))
            self.assertEqual(expected[sg.id],len(cumulative_lengths[sg.id]))

            print('Seg group %s has path_lengths_to_proximal: %s'%(sg.id,path_lengths_to_proximal))
            self.assertEqual(expected[sg.id],len(path_lengths_to_proximal[sg.id]))

            print('Seg group %s has path_lengths_to_distal: %s'%(sg.id,path_lengths_to_distal))
            self.assertEqual(expected[sg.id],len(path_lengths_to_distal[sg.id]))

    def runTest(self):
        print("Running tests in TestCell")


if __name__ == '__main__':
    ta = TestCell()

    ta.test_cell_methods()
    ta.test_cell_methods2()
