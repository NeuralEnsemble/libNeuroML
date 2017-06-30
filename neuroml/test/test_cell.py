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
        
        cells = ['pyr_4_sym']
        
        for cell_name in cells:

            root_dir = os.path.dirname(neuroml.__file__)
            test_file_path = os.path.join(root_dir,'examples/test_files/%s.cell.nml'%cell_name)
            print('test file path is: '+test_file_path)
            f = open(test_file_path,'r')

            doc = loaders.NeuroMLLoader.load(test_file_path)
            
            cell = doc.cells[0]
            self.assertEqual(cell.id,cell_name.split('.')[0])
            
            cell.summary()
      
                
            #cell.get_ordered_segments_in_groups = get_ordered_segments_in_groups
            
            for grp in ['soma_group', ['soma_group','basal_dends'],['dendrite_group'],['all'] ]:
                
                print("-----------------------------")
                print("   Testing %s..."%grp)
            
                segs, cuml, path_prox, path_dist = cell.get_ordered_segments_in_groups(grp,
                                                      check_parentage=(grp==['all']),
                                                      include_cumulative_lengths=True,
                                                      include_path_lengths=True)
                
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
            
