#!/usr/bin/env python3
"""
"Level 2" validators: extra tests in addition to the validation tests included
in the standard/schema

File: neuroml/l2validators.py

Copyright 2023 NeuroML contributors
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""

import inspect
import importlib
import typing
from abc import ABC, abstractmethod
from enum import Enum
import logging
logger = logging.getLogger(__name__)


class TEST_LEVEL(Enum):
    WARNING = logging.WARNING
    ERROR = logging.ERROR


class StandardTestSuper(ABC):

    """Class implementing a standard test.

    All tests should extend this class. `L2Validator` will automatically
    register any classes in this module that extend this class.
    """

    test_id = None
    target_class = None
    description = None
    level = None

    @abstractmethod
    def run(self, obj):
        """Implementation of test to run.
        :param obj: object to run test on
        :returns: True if test passes, false if not
        """
        pass


class L2Validator(object):

    """Main validator class."""
    tests: typing.Dict[str, typing.Any] = {}

    def __init__(self):
        """Register all classes that extend StandardTestSuper """
        this_module = importlib.import_module(__name__)
        for name, obj in inspect.getmembers(this_module):
            if inspect.isclass(obj):
                if StandardTestSuper in obj.__mro__:
                    if obj != StandardTestSuper:
                        self.register_test(obj)

    @classmethod
    def validate(cls, obj, collector=None):
        """Main validate method that should include calls to all tests that are
        to be run on an object

        :param obj: object to be validated
        :type obj: an object to be validated
        :param collector: a GdsCollector instance for messages
        :type collector: neuroml.GdsCollector
        :returns: True if all validation tests pass, false if not
        """
        for test in cls.tests[obj.__class__.__name__]:
            if not test.run(obj):
                if collector:
                    collector.add_message(f"Validation failed: {test.test_id}: {test.description}")
                else:
                    if test.level == logging.WARN:
                        logger.warn(f"Validation failed: {test.test_id}: {test.description}")
                    else:
                        logger.error(f"Validation failed: {test.test_id}: {test.description}")
                return False

        return True

    @classmethod
    def register_test(cls, test):
        """Register a test class

        :param test: test class to register
        :returns: None

        """
        try:
            if test not in cls.tests[test.target_class]:
                cls.tests[test.target_class].append(test)
        except KeyError:
            cls.tests[test.target_class] = [test]

    @classmethod
    def list_tests(cls):
        """List all registered tests."""
        print("Registered tests:")
        for key, val in cls.tests.items():
            print(f"* {key}")
            for t in val:
                print(f"\t* {t.test_id}: {t.description}")
            print()


class SegmentGroupSelfIncludes(StandardTestSuper):

    """Segment groups should not include themselves"""
    test_id = "0001"
    target_class = "SegmentGroup"
    description = "Segment group includes itself"
    level = TEST_LEVEL.ERROR

    @classmethod
    def run(self, obj):
        """Test runner method.

        :param obj: object to run tests on
        :type object: any neuroml.* object
        :returns: True if test passes, false if not.

        """
        for sginc in obj.includes:
            print(f"{sginc.segment_groups}, {obj.id}")
            if sginc.segment_groups == obj.id:
                return False
        return True
