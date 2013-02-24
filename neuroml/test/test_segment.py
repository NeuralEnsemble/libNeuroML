"""
Unit tests for the Segment class


"""

from neuroml import Segment
from neuroml import Point3DWithDiam

try:
    import unittest2 as unittest
except ImportError:
    import unittest
    

class TestSingleSegment(unittest.TestCase):

    def test_proximal_diameter(self):
        proximal_point = Point3DWithDiam(diameter = 3.21)
        seg = Segment(proximal = proximal_point)
        self.assertEqual(seg.proximal.diameter, 3.21)

    def test_proximal_diameter(self):
        distal_point = Point3DWithDiam(diameter = 3.21)
        seg = Segment(distal = distal_point)
        self.assertEqual(seg.distal.diameter, 3.21)

    def test_proximal_coordinates(self):
        proximal_point = Point3DWithDiam(x=0.1, y=0.2, z=0.3)
        seg = Segment(proximal = proximal_point)
        self.assertEqual(seg.proximal.x, 0.1)
        self.assertEqual(seg.proximal.y, 0.2)
        self.assertEqual(seg.proximal.z, 0.3)

    def test_distal_coordinates(self):
        distal_point = Point3DWithDiam(x=0.1, y=0.2, z=0.3)
        seg = Segment(distal = distal_point)
        self.assertEqual(seg.distal.x, 0.1)
        self.assertEqual(seg.distal.y, 0.2)
        self.assertEqual(seg.distal.z, 0.3)

class TestHelperProperties(unittest.TestCase):
    """
    When helper properties are developed (for volume, area etc, this
    will be used to test them.
    """
#    def test_length(self):
#        seg = Segment(length=10.7, proximal_diameter=3.21, distal_diameter=2.46)
#        self.assertAlmostEqual(seg.length, 10.7, places=7)
#
#    def test_index(self):
#        seg = Segment(length=10.7, proximal_diameter=3.21, distal_diameter=2.46)
#        self.assertEqual(seg.index, (seg.proximal, seg.distal))
#
#    def test_morphology(self):
#        seg = Segment(length=10.7, proximal_diameter=3.21, distal_diameter=2.46)
#        self.assertIsInstance(seg.morphology, SegmentGroup)
#        # add test that SegmentGroup contains seg...
#
#    def test_slant_height(self):
#        seg = Segment(length=4.0, proximal_diameter=2.0, distal_diameter=8.0)
#        self.assertAlmostEqual(seg.slant_height, 5.0, places=7)
#
#    def test_lateral_area(self):
#        cyl_seg = Segment(length=4.0, proximal_diameter=5.0, distal_diameter=5.0)
#        self.assertAlmostEqual(cyl_seg.lateral_area, 20*math.pi, places=7)
#        conical_frustrum_seg = Segment(length=4.0, proximal_diameter=2.0, distal_diameter=8.0)
#        # sum of radii = 5.0, slant_height = 5.0
#        self.assertAlmostEqual(conical_frustrum_seg.lateral_area, 25*math.pi, places=7)
#
#    def test_total_area(self):
#        conical_frustrum_seg = Segment(length=4.0, proximal_diameter=2.0, distal_diameter=8.0)
#        # sum of radii = 5.0, slant_height = 5.0
#        self.assertAlmostEqual(conical_frustrum_seg.total_area, (25+1+16)*math.pi, places=7)
#
#    def test_parent(self):
#        seg = Segment(length=4.0, proximal_diameter=2.0, distal_diameter=8.0)
#        self.assertEqual(seg.parent, None)
#
#    def test_parent_id(self):
#        seg = Segment(length=4.0, proximal_diameter=2.0, distal_diameter=8.0)
#        self.assertEqual(seg.parent_id, -1)
#
#    def test_volume(self):
#        conical_frustrum_seg = Segment(length=4.0, proximal_diameter=2.0, distal_diameter=8.0)
#        # sum of radii = 5.0, slant_height = 5.0
#        self.assertAlmostEqual(conical_frustrum_seg.volume, math.pi*4*(1+4+16)/3)
#
#    #def test_attach(self):
#    #    self.fail()
    pass

class TestAttachedSegments(unittest.TestCase):
    pass
