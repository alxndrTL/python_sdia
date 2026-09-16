# Configuration file for the Sphinx documentation builder.
#
# Le code source se trouve dans ../../src : on l'ajoute au sys.path pour
# qu'autodoc puisse importer le package ``lab1``.

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Lab1 - SDIA Python'
copyright = '2026, Henry Fernandes--Strag, Alexandre Torres--Leguet'
author = 'Henry Fernandes--Strag, Alexandre Torres--Leguet'

version = '0.1'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # comprend les docstrings au format Google
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
