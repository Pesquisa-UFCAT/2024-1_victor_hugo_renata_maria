"""Sphinx configuration for the carbonation durability / PCE surrogate project."""

import os
import sys
from datetime import date

# functions.py lives at the repository root, one level above docs/
sys.path.insert(0, os.path.abspath('..'))

# -- Project information ---------------------------------------------------

project   = 'Carbonation Durability Surrogates'
author    = 'Victor Hugo, Renata Maria, Wanderlei Malaquias Pereira Junior'
copyright = f'{date.today().year}, {author}'
release   = '0.1.0'
version   = '0.1'

# -- General configuration -------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',       # pull docstrings out of functions.py
    'sphinx.ext.napoleon',      # tolerate Google/NumPy style if it shows up later
    'sphinx.ext.viewcode',      # [source] links next to each object
    'sphinx.ext.intersphinx',   # cross-link numpy/pandas/scipy/sklearn types
    'sphinx.ext.mathjax',       # math in docstrings
    'sphinx_copybutton',        # copy button on code blocks
    'myst_parser',              # allows .md pages alongside .rst
]

templates_path   = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language         = 'en'

# -- autodoc ---------------------------------------------------------------

autodoc_member_order    = 'bysource'
autodoc_typehints       = 'description'
autodoc_typehints_format = 'short'
autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
}

# The docstrings are written in reStructuredText field style (:param:/:return:),
# so napoleon only needs to stay out of the way.
napoleon_google_docstring = False
napoleon_numpy_docstring  = False

# -- MyST (the .md pages) --------------------------------------------------

# The narrative pages are Markdown; Sphinx directives are written as
# ```{directive} fences. These extensions add $math$ and definition lists.
myst_enable_extensions = [
    'dollarmath',
    'deflist',
    'colon_fence',
]

# -- intersphinx -----------------------------------------------------------

intersphinx_mapping = {
    'python':  ('https://docs.python.org/3', None),
    'numpy':   ('https://numpy.org/doc/stable/', None),
    'pandas':  ('https://pandas.pydata.org/docs/', None),
    'scipy':   ('https://docs.scipy.org/doc/scipy/', None),
    'sklearn': ('https://scikit-learn.org/stable/', None),
}

# -- HTML output -----------------------------------------------------------

html_theme       = 'furo'
html_title       = 'Carbonation Durability Surrogates'
html_static_path = ['_static']
