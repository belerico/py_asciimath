# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "py_asciimath"
copyright = "2020, Federico Belotti"
author = "Federico Belotti"

# The full version, including alpha/beta/rc tags
release = "0.2.4"


# -- General configuration ---------------------------------------------------

master_doc = "index"
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosectionlabel",
    "m2r",
]

source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

html_sidebars = {
    "**": ["about.html", "globaltoc.html", "relations.html", "searchbox.html",]
}

html_theme_options = {
    "show_powered_by": False,
    "github_user": "belerico",
    "github_repo": "py_asciimath",
    "github_banner": True,
    "show_related": False,
    "note_bg": "#FFF59C",
}
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


def setup(app):
    print(os.getcwd())
    with open("../../README.md", "r+") as f:
        readme = f.read()
        readme = re.sub(r"docs/source/", "", readme)
        f.seek(0)
        f.write(readme)
        f.close()
