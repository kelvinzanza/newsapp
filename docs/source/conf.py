import os
import sys
import django

# Add project root to Python path (so Django can be imported)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'billboard.settings'

# Setup Django
django.setup()

# -- Project information -----------------------------------------------------
project = 'newsapp'
copyright = '2025, Kelvin'
author = 'Kelvin'
release = '000.000.001'

# -- General configuration ---------------------------------------------------
# Add Sphinx extensions for docstrings
extensions = [
    'sphinx.ext.autodoc',          # Generate documentation from docstrings
    'sphinx.ext.napoleon',         # Support Google-style and NumPy docstrings
    'sphinx_autodoc_typehints'     # Show type hints in documentation
]

# Templates path (optional)
templates_path = ['_templates']

# Files or patterns to ignore
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# Use Read the Docs theme for nicer HTML
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']