"""
Unit tests for the Segment class


"""

import math

from neuroml import Cell, Morphology, Point3DWithDiam, Segment, SegmentParent

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestSingleSegment(unittest.TestCase):
    def test_proximal_diameter(self):
        proximal_point = Point3DWithDiam(diameter=3.21)
        seg = Segment(proximal=proximal_point)

        self.assertEqual(seg.proximal.diameter, 3.21)

    def test_distal_diameter(self):
        distal_point = Point3DWithDiam(diameter=3.21)
        seg = Segment(distal=distal_point)

        self.assertEqual(seg.distal.diameter, 3.21)

    def test_proximal_coordinates(self):
        proximal_point = Point3DWithDiam(x=0.1, y=0.2, z=0.3)
        seg = Segment(proximal=proximal_point)

        self.assertEqual(seg.proximal.x, 0.1)
        self.assertEqual(seg.proximal.y, 0.2)
        self.assertEqual(seg.proximal.z, 0.3)

    def test_distal_coordinates(self):
        distal_point = Point3DWithDiam(x=0.1, y=0.2, z=0.3)
        seg = Segment(distal=distal_point)

        self.assertEqual(seg.distal.x, 0.1)
        self.assertEqual(seg.distal.y, 0.2)
        self.assertEqual(seg.distal.z, 0.3)


class TestHelperProperties(unittest.TestCase):
    """
    Tests for helper properties for volume, area etc

    These are not part of the neuroML schema itself
    """

    def test_length0(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam)

        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.length, 1, places=7)

    def test_length(self):
        d = Point3DWithDiam(x=0.2, y=2.4, z=3.5, diameter=0.6)
        p = Point3DWithDiam(x=0.5, y=2.0, z=1.8, diameter=0.9)

        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.length, 1.772004514, places=7)

    def test_area0(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam)

        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.surface_area, math.pi * diam * len, places=7)

    def test_area1(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam * 1.01)

        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.surface_area, 3.15734008, places=7)

    def test_area(self):
        d = Point3DWithDiam(x=0.2, y=2.4, z=3.5, diameter=0.6)
        p = Point3DWithDiam(x=0.5, y=2.0, z=1.8, diameter=0.9)

        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.surface_area, 4.19011944, places=7)

    def test_volume0(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam)
        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.volume, math.pi * (diam / 2) ** 2 * len, places=7)

    def test_volume1(self):
        diam = 1.0
        len = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=len, z=0, diameter=diam * 1.01)
        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.volume, 0.793278324, places=7)

    def test_volume(self):
        d = Point3DWithDiam(x=0.2, y=2.4, z=3.5, diameter=0.6)
        p = Point3DWithDiam(x=0.5, y=2.0, z=1.8, diameter=0.9)
        seg = Segment(proximal=p, distal=d)

        self.assertAlmostEqual(seg.volume, 0.7932855820702964, places=7)

    def test_spherical(self):
        diam = 1.0
        d = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)

        seg = Segment(id=0, proximal=p, distal=d)

        self.assertEqual(seg.length, 0)
        self.assertEqual(seg.surface_area, math.pi)

    def test_cell_with_segs(self):
        cell = Cell(id="cell0")

        diam = 1.0
        d0 = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)
        p = Point3DWithDiam(x=0, y=0, z=0, diameter=diam)

        seg0 = Segment(id=0, proximal=p, distal=d0)

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

        d3 = Point3DWithDiam(x=15, y=10, z=0, diameter=diam)

        seg3 = Segment(
            id=3, distal=d3, parent=SegmentParent(segments=seg2.id, fraction_along=0.5)
        )
        cell.morphology.segments.append(seg3)
        for f in [0, 0.25, 0.5, 0.75, 1]:
            seg3.parent.fraction_along = f
            print(
                "Fract: %s, length: %s, proximal: %s"
                % (
                    f,
                    cell.get_segment_length(seg3.id),
                    cell.get_actual_proximal(seg3.id),
                )
            )

        self.assertEqual(seg0.length, 0)
        self.assertEqual(cell.get_segment_length(seg0.id), 0)

        self.assertRaises(Exception, lambda: seg1.length)  # No proximal
        self.assertEqual(cell.get_segment_length(seg1.id), 10)

        self.assertEqual(seg2.length, 10)
        self.assertEqual(cell.get_segment_length(seg2.id), 10)

        self.assertEqual(seg0.surface_area, math.pi)
        self.assertEqual(cell.get_segment_surface_area(seg0.id), math.pi)
        self.assertRaises(Exception, lambda: seg1.surface_area)  # No proximal
        self.assertEqual(cell.get_segment_surface_area(seg1.id), math.pi * 10)
        self.assertEqual(seg2.surface_area, math.pi * 10)
        self.assertEqual(cell.get_segment_surface_area(seg2.id), math.pi * 10)

        v = 4.0 / 3 * math.pi * (diam / 2) ** 3
        self.assertEqual(seg0.volume, v)
        self.assertEqual(cell.get_segment_volume(seg0.id), v)
        v = (
            math.pi
            * seg2.proximal.diameter
            / 2
            * seg2.proximal.diameter
            / 2
            * seg2.length
        )
        self.assertRaises(Exception, lambda: seg1.volume)  # No proximal
        self.assertAlmostEqual(cell.get_segment_volume(seg1.id), v, places=7)
        self.assertAlmostEqual(seg2.volume, v, places=7)
        self.assertAlmostEqual(cell.get_segment_volume(seg2.id), v, places=7)

        # Break the sphere...
        seg0.distal.diameter = diam * 2
        self.assertRaises(Exception, lambda: seg0.surface_area)
        self.assertRaises(Exception, lambda: seg0.volume)

        print("Passed...")
        """  """

    def runTest(self):
        print("Running tests in TestHelperProperties")


class TestAttachedSegments(unittest.TestCase):
    pass


if __name__ == "__main__":
    ta = TestHelperProperties()

    ta.test_length0()
    ta.test_length()

    ta.test_area0()
    ta.test_area1()
    ta.test_area()

    ta.test_volume0()
    ta.test_volume1()
    ta.test_volume()

    ta.test_spherical()
    ta.test_cell_with_segs()
