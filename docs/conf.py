import os
import sphinx.ext.autodoc
import sys

conf_file_abs_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(conf_file_abs_path, ".."))

import integration

project = 'DComEX Framework'
copyright = '2022, NTUA, ETHZ, CSCS'
author = 'NTUA, ETHZ, CSCS'

extensions = [
    'sphinx.ext.mathjax', 'sphinx.ext.autodoc', 'sphinx.ext.autosummary',
    'sphinx_automodapi.automodapi'
]

templates_path = ['_templates']
exclude_patterns = ['_build']
html_theme = 'alabaster'
html_static_path = ['_static']
autoclass_content = 'both'
