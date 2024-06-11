#!/usr/bin/env python3
"""
Test global validation toggles

File: test_global_validation.py

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import neuroml
from neuroml import (
    disable_build_time_validation,
    enable_build_time_validation,
    get_build_time_validation,
)
from neuroml.utils import component_factory


class TestGlobalValidationToggle(unittest.TestCase):
    def test_global_validation_toggle(self):
        """Test enabling and disabling build time validation"""
        self.assertTrue(get_build_time_validation())
        with self.assertRaises(ValueError):
            anet = component_factory(neuroml.Network, id="anet")

        disable_build_time_validation()
        self.assertFalse(get_build_time_validation())
        anet = component_factory(neuroml.Network, id="anet")

        enable_build_time_validation()
        with self.assertRaises(ValueError):
            anet = component_factory(neuroml.Network, id="anet")
