# -*- coding: utf-8 -*-
#
# libNeuroML documentation build configuration file, created by
# sphinx-quickstart on Wed Mar 21 08:17:12 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

sys.path.insert(0, os.path.abspath('../neuroml'))
sys.path.insert(0, os.path.abspath('..'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo',
              'sphinxcontrib.bibtex']

bibtex_bibfiles = ['refs.bib']

# Include TODOs in docs
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'libNeuroML'
copyright = u'2021, libNeuroML authors and contributors'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ""
for aline in open('../neuroml/__init__.py'):
    # space here is important since __version__ is used in generation of
    # version_info also
    if '__version__ =' in aline:
        version = aline.split("\"")[1]
# The full version, including alpha/beta/rc tags.
release = version

# autodoc_class_signature = "separated"
autoclass_content = "both"

# gds specific members to exclude from nml.py doc
autodoc_default_options = {
    "exclude-members": "build, buildAttributes, buildChildren, exportAttributes, export, exportChildren, factory, hasContent_, member_data_items_, subclass, superclass, warn_count, validate_allowedSpaces, validate_BlockTypes, validate_channelTypes, validate_DoubleGreaterThanZero, validate_gateTypes, validate_MetaId, validate_MetaId_patterns_, validate_Metric, validate_networkTypes, validate_NeuroLexId, validate_NeuroLexId_patterns_, validate_Nml2Quantity, validate_Nml2Quantity_capacitance, validate_Nml2Quantity_capacitance_patterns_, validate_Nml2Quantity_concentration, validate_Nml2Quantity_concentration_patterns_, validate_Nml2Quantity_conductance, validate_Nml2Quantity_conductanceDensity, validate_Nml2Quantity_conductanceDensity_patterns_, validate_Nml2Quantity_conductance_patterns_, validate_Nml2Quantity_conductancePerVoltage, validate_Nml2Quantity_conductancePerVoltage_patterns_, validate_Nml2Quantity_current, validate_Nml2Quantity_currentDensity, validate_Nml2Quantity_currentDensity_patterns_, validate_Nml2Quantity_current_patterns_, validate_Nml2Quantity_length, validate_Nml2Quantity_length_patterns_, validate_Nml2Quantity_none, validate_Nml2Quantity_none_patterns_, validate_Nml2Quantity_patterns_, validate_Nml2Quantity_permeability, validate_Nml2Quantity_permeability_patterns_, validate_Nml2Quantity_pertime, validate_Nml2Quantity_pertime_patterns_, validate_Nml2Quantity_resistance, validate_Nml2Quantity_resistance_patterns_, validate_Nml2Quantity_rhoFactor, validate_Nml2Quantity_rhoFactor_patterns_, validate_Nml2Quantity_specificCapacitance, validate_Nml2Quantity_specificCapacitance_patterns_, validate_Nml2Quantity_temperature, validate_Nml2Quantity_temperature_patterns_, validate_Nml2Quantity_time, validate_Nml2Quantity_time_patterns_, validate_Nml2Quantity_voltage, validate_Nml2Quantity_voltage_patterns_, validate_NmlId, validate_NmlId_patterns_, validate_NonNegativeInteger, validate_Notes, validate_PlasticityTypes, validate_populationTypes, validate_PositiveInteger, validate_ZeroOrOne, validate_ZeroToOne"
}

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'pydata_sphinx_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "github_url": "https://github.com/NeuralEnsemble/libNeuroML",
    "use_edit_page_button": True,
    "show_toc_level": 1,
    "external_links": [
        {
            "name": "NeuroML Documentation", "url": "https://docs.neuroml.org"
        },
    ]
}

html_context = {
    "github_user": "NeuralEnsemble",
    "github_repo": "libNeuroML",
    "github_version": "development",
}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/neuroml_logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'libNeuroMLdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ('index', 'libNeuroML.tex', 'libNeuroML Documentation',
     'libNeuroML authors and contributors', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'libneuroml', 'libNeuroML Documentation',
     ['libNeuroML authors and contributors'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'libNeuroML', 'libNeuroML Documentation',
     'libNeuroML authors and contributors', 'libNeuroML', 'This package provides libNeuroML for working with neuronal models specified in NeuroML 2.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'
