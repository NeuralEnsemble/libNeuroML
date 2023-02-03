#!/usr/bin/env python3
"""
Enter one line description here.

File:

Copyright 2023 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest


from neuroml.l2validators import (L2Validator, SegmentGroupSelfIncludes,
                                  StandardTestSuper)
from neuroml import SegmentGroup, Include
from neuroml.utils import component_factory


class TestL2Validators(unittest.TestCase):

    """Docstring for TestL2Validators. """

    def test_l2validator(self):
        """Test L2Validtor

        tests that standard tests defined in the l2validators module are
        automatically registered.
        """

        self.l2validator = None
        self.l2validator = L2Validator()
        self.l2validator.list_tests()
        self.assertIn(SegmentGroupSelfIncludes, list(self.l2validator.tests["SegmentGroup"]))

    def test_l2validator_register(self):
        """Test l2validator test registration """
        class DummyTest(StandardTestSuper):

            """A dummy test"""
            test_id = "0001"
            target_class = "DummyClass"
            description = "DummyClass"
            level = 0

            @classmethod
            def run(self, obj):
                """Test runner method.

                :param obj: object to run tests on
                :type object: any neuroml.* object
                :returns: True if test passes, false if not.

                """
                return True

        self.l2validator = None
        self.l2validator = L2Validator()
        self.l2validator.register_test(DummyTest)
        self.l2validator.list_tests()
        self.assertIn(DummyTest, list(self.l2validator.tests["DummyClass"]))

    def test_l2validator_runs(self):
        """Test l2validator test running"""
        class DummyTest(StandardTestSuper):

            """A dummy test"""
            test_id = "0001"
            target_class = "DummyClass"
            description = "DummyClass"
            level = 0

            @classmethod
            def run(self, obj):
                """Test runner method.

                :param obj: object to run tests on
                :type object: any neuroml.* object
                :returns: True if test passes, false if not.

                """
                return True

        class DummyClass(object):

            """A dummy class"""

            name = "dummy"

        self.l2validator = None
        self.l2validator = L2Validator()
        self.l2validator.register_test(DummyTest)
        dummy = DummyClass()

        self.assertIn(DummyTest, list(self.l2validator.tests["DummyClass"]))
        self.assertTrue(self.l2validator.validate(dummy))

    def test_SegmentGroupSelfIncludes(self):
        """test SegmentGroupSelfIncludes class"""
        sg = component_factory(SegmentGroup, validate=True, id="dummy_group")
        sg.l2_validator.list_tests()
        with self.assertRaises(ValueError):
            sg.add(Include, segment_groups="dummy_group")
