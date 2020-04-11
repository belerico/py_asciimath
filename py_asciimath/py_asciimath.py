"""py_asciimath: a simple ASCIIMath converter.

Usage:
  py_asciimath.py ASCIIMATH ... (-o latex | --output=latex)
            [--log] [--dstyle]
  py_asciimath.py ASCIIMATH ... (-o mathml | --output=mathml)
            [--log] [--dstyle] [--pprint] [--validate-xml=MathMLDTD]
  py_asciimath.py (-h | --help)
  py_asciimath.py --version

Options:
  -h --help                     Show this screen.
  -o OLANG --output=OLANG       Output language.
  --log                         Log the transformation process.
  --dstyle                      Add display style
  --pprint                      Pretty print
  --validate-xml=MathMLDTD      Validate against a MathML DTD. MathMLDTD can be: mathml1, mathml2 or mathml3
  --version                     Show version.
"""
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

# from future import standard_library
# standard_library.install_aliases()
import sys

from docopt import docopt

from . import __version__
from .grammar.asciimath_grammar import asciimath_grammar
from .parser.parser import ASCIIMath2MathML, ASCIIMath2Tex


def main():
    arguments = docopt(__doc__, version="py_asciimath " + __version__)
    if arguments["--output"]:
        olang = arguments["--output"].lower()
        if olang == "latex":
            print("Translating ...")
            if arguments["--pprint"]:
                print("Ignoring option --pprint")
            if arguments["--validate-xml"]:
                print("Ignoring option --validate-xml")
            print(
                ASCIIMath2Tex(
                    asciimath_grammar, log=arguments["--log"],
                ).translate(
                    " ".join(arguments["ASCIIMATH"]),
                    displaystyle=arguments["--dstyle"],
                    pprint=False,
                )
            )
        elif olang == "mathml":
            validate = (
                True if arguments["--validate-xml"] is not None else False
            )
            print("Translating ...")
            s = ASCIIMath2MathML(
                asciimath_grammar, log=arguments["--log"],
            ).translate(
                " ".join(arguments["ASCIIMATH"]),
                displaystyle=arguments["--dstyle"],
                dtd=arguments["--validate-xml"],
                dtd_validation=validate,
                pprint=False,
                xml_pprint=arguments["--pprint"],
            )
            print(s)
        else:
            print("SUPPORTED OLANG: 'latex', 'mathml'", file=sys.stderr)
            sys.exit(1)
    else:
        print(arguments)
