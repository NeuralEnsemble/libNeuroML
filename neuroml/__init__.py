import logging

from . import build_time_validation
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version__info__
from .__version__ import current_neuroml_version as current_neuroml_version
from .nml.nml import *  # allows importation of all neuroml classes

logging.basicConfig(
    format="libNeuroML >>> %(levelname)s - %(message)s",
    level=logging.WARN,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def print_(text, verbose=True):
    if verbose:
        prefix = "libNeuroML >>> "
        # if not isinstance(text, str): text = text.decode('ascii')
        if verbose:
            print("%s%s" % (prefix, text.replace("\n", "\n" + prefix)))


def disable_build_time_validation():
    """Disable build time validation.

    This will disable the validation of components when they are being created
    using the factory functions, such as component_factory, and add.

    This is useful for certain cases where a new component cannot necessarily
    be created in a valid state from the beginning. For example, a population
    is usually created after a network, but a network without a population
    would not be valid.

    This switch provides a convenient way to disable this check.

    Please note that this should only be used sparingly, and not abused to turn
    off build time validation completely.

    .. versionadded:: 0.6.0
    """
    build_time_validation.ENABLED = False
    logger.warning("Build time validation has been disabled.")


def enable_build_time_validation():
    """Enable build time validation

    .. versionadded:: 0.6.0
    """
    build_time_validation.ENABLED = True
    logger.info("Build time validation has been enabled.")


def get_build_time_validation() -> bool:
    """Get build time validation

    .. versionadded:: 0.6.0

    :returns: state of build time validation
    :rtype: bool
    """
    return build_time_validation.ENABLED
