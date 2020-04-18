[![Build Status](https://travis-ci.com/belerico/py_asciimath.svg?branch=master)](https://travis-ci.com/belerico/py_asciimath) [![Documentation Status](https://readthedocs.org/projects/py-asciimath/badge/?version=latest)](https://py-asciimath.readthedocs.io/en/latest/?badge=latest) [![Coverage Status](https://coveralls.io/repos/github/belerico/py_asciimath/badge.svg?branch=master)](https://coveralls.io/github/belerico/py_asciimath?branch=master) [![PyPI](https://img.shields.io/pypi/v/py_asciimath?color=light%20green)](https://pypi.org/project/py-asciimath/0.2.2/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py_asciimath)](https://www.python.org/)

py_asciimath is a simple yet powerful Python module that:

* converts an ASCIIMath string to LaTeX or MathML
* converts a MathML string to LaTeX (the conversion is done thank to the [XSLT MathML Library](https://sourceforge.net/projects/xsltml/). Please report any unexpected behavior)
* exposes a single translation method `translate(exp, **kwargs)`, which semantic depends on the py_asciimath translator one wish to use
* exposes a MathML parser

<div align="center">
  <img src="_static/images/py_asciimath_translations.png">
</div>