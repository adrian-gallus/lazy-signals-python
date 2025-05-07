# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'lazy-signals'
copyright = '2025, Adrian Gallus'
author = 'Adrian Gallus'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'autoapi.extension',
    'sphinx_mdinclude',
]

autoapi_dirs = ['../src/']
autoapi_add_toctree_entry = False
autosummary_generate = True
add_module_names = False
#autodoc_default_options = {
#    'members': True,
#    'undoc-members': True,  # Include members without docstrings
#    'show-inheritance': True,
#    'special-members': '__init__',  # Include special methods if needed
#    'inherited-members': True,  # Include inherited methods
#}

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
