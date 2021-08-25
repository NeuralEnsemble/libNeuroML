Regenerating documentation
==========================

Please create a virtual environment and use the `requirements.txt` file to install the necessary bits.

In most cases, running `make html` should be sufficient to regenerate the documentation.
However, if any changes to `nml.py` have been made, the `nml-core-docs.py` file in the `helpers` directory will also need to be run.
This script manually adds each class from `nml.py` to the documentation as a sub-section using the `autoclass` sphinx directive instead of the `automodule` directive which does not allow us to do this.
