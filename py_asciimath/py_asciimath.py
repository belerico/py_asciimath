"""py_asciimath: a simple ASCIIMath converter.

Usage:
  py_asciimath.py ASCIIMATH ... (-o OLANG | --output=OLANG)
            [--log] [--pprint] [--to-file]
  py_asciimath.py (-h | --help)
  py_asciimath.py --version

Options:
  -h --help                     Show this screen.
  -o OLANG --output=OLANG       Output language.
  --log                         Log the transformation process.
  --pprint                      Pretty print
  --to-file                     Save output to file
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
from .transformer.transformer import LatexTransformer, MathMLTransformer


def main():
    arguments = docopt(__doc__, version="py_asciimath " + __version__)
    if arguments["--output"]:
        olang = arguments["--output"].lower()
        if olang == "latex":
            print("Translating ...")
            print(
                ASCIIMath2Tex(
                    asciimath_grammar,
                    transformer=LatexTransformer(log=arguments["--log"]),
                ).translate(
                    " ".join(arguments["ASCIIMATH"]), arguments["--pprint"]
                )
            )
        elif olang == "mathml":
            print("Translating ...")
            print(
                ASCIIMath2MathML(
                    asciimath_grammar,
                    transformer=MathMLTransformer(log=arguments["--log"]),
                ).translate(
                    " ".join(arguments["ASCIIMATH"]),
                    pprint=arguments["--pprint"],
                )
            )
        else:
            print("SUPPORTED OLANG: 'latex', 'mathml'", file=sys.stderr)
            sys.exit(1)
    else:
        print(arguments)
