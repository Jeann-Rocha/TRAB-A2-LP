# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_rtd_theme
import os
import sys
sys.path.insert(0, os.path.abspath('../'))

project = 'Documentação Jogo Spacial Game'
copyright = '2023, Alessandra Belló, Guilherme Ferrari, Jeann Rocha e Edgard Junio'
author = 'Alessandra Belló, Guilherme Ferrari, Jeann Rocha e Edgard Junio'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.githubpages', 'sphinx_rtd_theme']

templates_path = ['templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

language = 'pt_BR'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['static']
html_extra_path = ['static']