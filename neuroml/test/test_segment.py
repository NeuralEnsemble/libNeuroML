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

    def test_distal_diameter(self):
        distal_point = Point3DWithDiam(diameter = 3.21)
        seg = Segment(distal = distal_point)

        self.assertEqual(seg.distal.diameter,3.21)

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
    Tests for helper properties for volume, area etc

    These are not part of the neuroML schema itself
    """
    def test_length(self):
        d=Point3DWithDiam(x=0.2,
                          y=2.4,
                          z=3.5,
                          diameter=0.6)
        p=Point3DWithDiam(x=0.5,
                          y=2.0,
                          z=1.8,
                          diameter=0.9)
        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.length, 1.7720, places=3)

    def test_area(self):
        d=Point3DWithDiam(x=0.2,
                          y=2.4,
                          z=3.5,
                          diameter=0.6)
        p=Point3DWithDiam(x=0.5,
                          y=2.0,
                          z=1.8,
                          diameter=0.9)
        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.area, 8.4691, places=3)

    def test_volume(self):
        d=Point3DWithDiam(x=0.2,
                          y=2.4,
                          z=3.5,
                          diameter=0.6)
        p=Point3DWithDiam(x=0.5,
                          y=2.0,
                          z=1.8,
                          diameter=0.9)
        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.volume, 3.1731, places=3)

class TestAttachedSegments(unittest.TestCase):
    pass
