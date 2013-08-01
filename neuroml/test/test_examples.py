"""
Testing that all examples run
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestExamples(unittest.TestCase):

    def test_build_network(self):
        from neuroml.examples import build_network
        build_network.run()

#    def test_ion_channel_generation(self):
#        from neuroml.examples import ion_channel_generati#on
#        ion_channel_generation.run()
        
    def test_morphology_generation(self):
        from neuroml.examples import morphology_generation
        morphology_generation.run()
