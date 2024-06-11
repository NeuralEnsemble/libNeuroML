"""
libNeuroML version information

File: neuroml/__version__.py

Copyright 2023 NeuroML contributors
"""

try:
    import importlib.metadata

    __version__ = importlib.metadata.version("libNeuroML")
except ImportError:
    import importlib_metadata

    __version__ = importlib_metadata.version("libNeuroML")

__version_info__: tuple = tuple(int(i) for i in __version__.split("."))


current_neuroml_version: str = "v2.3.1"
