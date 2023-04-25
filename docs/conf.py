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

html_theme = 'classic'
html_static_path = ['_static']
html_favicon = '_static/favicon.ico'
autoclass_content = 'both'

latex_documents = [
    ('index', 'dcomex.tex', u'DComEX Documentation',
     author, 'howto'),
]
