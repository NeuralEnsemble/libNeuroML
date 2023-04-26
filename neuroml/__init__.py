from .nml.nml import *  # allows importation of all neuroml classes
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version__info__
from .__version__ import current_neuroml_version as current_neuroml_version


def print_(text, verbose=True):
    if verbose:
        prefix = "libNeuroML >>> "
        # if not isinstance(text, str): text = text.decode('ascii')
        if verbose:
            print("%s%s" % (prefix, text.replace("\n", "\n" + prefix)))
