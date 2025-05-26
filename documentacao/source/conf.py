# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  

project = 'teste sphinx'
copyright = '2025, luiz'
author = 'luiz'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.napoleon']
autodoc_typehints = "description" 

templates_path = ['_templates']
exclude_patterns = []

language = 'pt'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'


html_baseurl = 'https://nerodrakar.github.io/teste_sphinx/'
html_static_path = ['_static']
html_css_files = [
    'pydoctheme.css',  # Se você quiser forçar o CSS manualmente (geralmente não precisa)
]
