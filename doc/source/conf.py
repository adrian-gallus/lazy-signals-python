# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path

sys.path.append(str(Path('../../src/').resolve()))

project = 'signals'
copyright = '2025, Adrian Gallus'
author = 'Adrian Gallus'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = []

autosummary_generate = True
#autodoc_default_options = {
#    'members': True,
#    'undoc-members': True,  # Include members without docstrings
#    'show-inheritance': True,
#    'special-members': '__init__',  # Include special methods if needed
#    'inherited-members': True,  # Include inherited methods
#}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'furo'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


