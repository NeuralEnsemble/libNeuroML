from nml.nml import Morphology

#what we also need is an SWC class, Optimized morphology can then be passed this.

class OptimizedMorphology(Morphology):
    def __init__(self):
        super(OptimizedMorphology,self).__init__()
