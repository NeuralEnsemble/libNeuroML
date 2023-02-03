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

    test_id = ""
    target_class = ""
    description = ""
    level = TEST_LEVEL.ERROR

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
    def validate(cls, obj, class_name=None, collector=None):
        """Main validate method that should include calls to all tests that are
        to be run on an object

        :param obj: object to be validated
        :type obj: an object to be validated
        :param class_name: name of class for which tests are to be run
            In most cases, this will be None, and the class name will be
            obtained from the object. However, in cases where a tests has been
            defined in an ancestor (BaseCell, which a Cell would inherit), one
            can pass the class name of the ancestor. This can be used to run L2
            test defined for ancestors for all descendents. In fact, tests for
            arbitrary classes can be run on any objects. It is for the
            developer to ensure that the appropriate tests are run.
        :type class_name: str
        :param collector: a GdsCollector instance for messages
        :type collector: neuroml.GdsCollector
        :returns: True if all validation tests pass, false if not
        """
        test_result = True
        class_name_ = class_name if class_name else obj.__class__.__name__
        # The collector looks for a local with name "self" in the stack frame
        # to figure out what the "caller" class is.
        # So, set "self" to the object that is being validated here.
        self = obj
        self._gds_collector = collector

        try:
            for test in cls.tests[class_name_]:
                test_result = test.run(obj)
        except KeyError:
            pass # no L2 tests have been defined

        if test_result is False:
            if self._gds_collector:
                self._gds_collector.add_message(f"Validation failed: {test.test_id}: {test.description}")
            else:
                if test.level == logging.WARNING:
                    logger.warn(f"Validation failed: {test.test_id}: {test.description}")
                else:
                    logger.error(f"Validation failed: {test.test_id}: {test.description}")

        return test_result

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
            if sginc.segment_groups == obj.id:
                return False
        return True
