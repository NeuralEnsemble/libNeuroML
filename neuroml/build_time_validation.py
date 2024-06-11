#!/usr/bin/env python3
"""
Module handling the current state of the build time validation.

Setting ENABLED to False will disable build time validation when using the
`component_factory` and `add` functions. This setting overrides the `validate`
parameter of the two functions also.

Disabling build time validation is useful for certain cases where a new
component cannot necessarily be created in a valid state from the beginning.
For example, a population is usually created after a network, but a network
without a population would not be valid.

Please note that this should only be used sparingly, and not abused to turn
off build time validation completely.

Split out into a separate module so that all the parts of the code can
access/modify it without the creation of circular dependencies.

.. versionadded:: 0.6.0

File: build_time_validation.py

Copyright 2024 NeuroML contributors
"""

ENABLED = True
