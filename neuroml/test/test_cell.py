"""
Unit tests for cells

"""

import neuroml
from neuroml import loaders
import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestCell(unittest.TestCase):
    
    def test_cell_methods(self):
        
        cells = ['Purk2M9s','pyr_4_sym.cell']
        cells = ['pyr_4_sym.cell']
        for cell_name in cells:

            root_dir = os.path.dirname(neuroml.__file__)
            test_file_path = os.path.join(root_dir,'examples/test_files/%s.nml'%cell_name)
            print('test file path is: '+test_file_path)
            f = open(test_file_path,'r')

            doc = loaders.NeuroMLLoader.load(test_file_path)
            
            cell = doc.cells[0]
            self.assertEqual(cell.id,cell_name.split('.')[0])
            
            cell.summary()
            
            def get_ordered_segments_in_groups(self, group_list, check_parentage=False, include_cumulative_lengths=False):
                
                unord_segs = {}
                other_segs = {}
                
                segments = self.get_segment_ids_vs_segments()
                
                for sg in self.morphology.segment_groups:
                    if sg.id in group_list:
                        unord_segs[sg.id] = []
                        for member in sg.members:
                            unord_segs[sg.id].append(segments[member.segments])
                    else:
                        other_segs[sg.id] = []
                        for member in sg.members:
                            other_segs[sg.id].append(segments[member.segments])
                
                for sg in self.morphology.segment_groups:
                    if sg.id in group_list:
                        for include in sg.includes:
                            if include.segment_groups in unord_segs:
                                for s in unord_segs[include.segment_groups]:
                                    unord_segs[sg.id].append(s)
                            if include.segment_groups in other_segs:
                                for s in other_segs[include.segment_groups]:
                                    unord_segs[sg.id].append(s)
                ord_segs = {}     
                
                from operator import attrgetter
                for key in unord_segs.keys():          
                    segs = unord_segs[key]
                    if len(segs)==1 or len(segs)==0:
                        ord_segs[key]=segs
                    else:
                        ord_segs[key]=sorted(segs,key=attrgetter('id'),reverse=False) 
                        
                if check_parentage:
                    # check parent ordering
                    
                    for key in ord_segs.keys():   
                        existing_ids = []
                        for s in ord_segs[key]:
                            if s.id != ord_segs[key][0].id:
                                if not s.parent or not s.parent.segments in existing_ids:
                                    raise Exception("Problem with finding parent of seg: "+str(s)+" in list: "+str(ord_segs))
                            existing_ids.append(s.id)
                            
                            
                if include_cumulative_lengths:
                    import math
                    cumulative_lengths = {}
                    for key in ord_segs.keys():   
                        cumulative_lengths[key] = []
                        tot_len = 0
                        for seg in ord_segs[key]:       
                            d = seg.distal
                            p = seg.proximal
                            if not p:
                                parent_seg = segments[seg.parent.segments]
                                p = parent_seg.distal
                            length = math.sqrt( (d.x-p.x)**2 + (d.y-p.y)**2 + (d.z-p.z)**2 )
                            tot_len += length
                            cumulative_lengths[key].append(tot_len)
                    
                    return ord_segs, cumulative_lengths

                return ord_segs
                    
                
            #cell.get_ordered_segments_in_groups = get_ordered_segments_in_groups
            
            for grp in [ ['soma_group','basal_dends'],['dendrite_group'],['all'] ]:
                
                print("-----------------------------")
                a, b = get_ordered_segments_in_groups(cell,grp,check_parentage=(grp in ['basal_dends']),include_cumulative_lengths=True)
                print("LLL %s:"%(grp))
                for k in b.keys():
                    v = b[k]
                    print("  %s: %s"%(k,a[k]))
                    print("  %s: %s"%(k,v))
                
                cc = cell.get_ordered_segments_in_groups(grp,check_parentage=(grp in ['basal_dends']),include_cumulative_lengths=True)
                print("CCC %s: %s"%(grp,cc))
            
            
