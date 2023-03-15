# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "flowmeter"
copyright = "2022, Coactum SA"
author = "Coactum SA"
release = "0.0.1"

# The master toctree document.
root_doc = "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.imgmath",
    "breathe",
    "sphinx.ext.graphviz",
    "sphinxcontrib.plantuml",
    "sphinx_copybutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# A list of glob-style patterns [1] that should be excluded when looking for source files.
exclude_patterns = ["build/", "**/*.puml", ".DS_Store"]

# The master toctree document.
master_doc = "index"

# -- Extension configuration -------------------------------------------------
# -- Options for autosectionlabel
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html

autosectionlabel_prefix_document = True

# -- Options for breathe -----------------------------------------------------
# https://github.com/breathe-doc/breathe

breathe_default_members = ("members", "undoc-members")

breathe_projects_source = {
    "hello": [
        os.path.abspath("../hello/"),
        [
            "include/hello/",
            "src",
        ],
    ]
}

breathe_show_include = False
breathe_show_define_initializer = True
breathe_domain_by_extension = {"h": "c", "c": "c"}
breathe_implementation_filename_extensions = []

breathe_projects = {}

# Automatically adds the path to the xml files of the projects specified in breathe_projects_source
# if they are not already given in breathe_projects
for key in breathe_projects_source:
    if key not in breathe_projects:
        breathe_projects[key] = f"build/doxygen/{key}/xml"

# Automatically define the default project as the first one defined in breathe_projects_source if it is not defined
if not "breathe_default_project" in locals():
    breathe_default_project = tuple(breathe_projects_source.keys())[0]

# -- Options for sphinxcontrib.plantuml --------------------------------------
# https://github.com/sphinx-contrib/plantuml/#configuration

plantuml_output_format = "svg_img"
plantuml_syntax_error_image = True
plantuml = f"plantuml -config {os.path.dirname(os.path.abspath(__file__))}/config.txt"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
# html_static_path = ["_static"]

pygments_style = "sphinx"
pygments_dark_style = "monokai"
