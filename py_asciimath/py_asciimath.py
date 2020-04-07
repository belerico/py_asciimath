"""py_asciimath: a simple ASCIIMath converter.

Usage:
  py_asciimath.py ASCIIMATH ... (-o OLANG | --output=OLANG) [--log]
  py_asciimath.py (-h | --help)
  py_asciimath.py --version

Options:
  -h --help                     Show this screen.
  -o OLANG --output=OLANG       Output language.
  --log                         Log the transformation process.
  --version                     Show version.
"""
import re
import sys

from docopt import docopt

from .parser.parser import ASCIIMath2Tex
from .transformer.const import asciimath_grammar
from .transformer.transformer import LatexTransformer

version = re.search(
    r'^__version__\s*=\s*"(.*)"', open("py_asciimath/__init__.py").read()
).group(1)


def main():
    arguments = docopt(__doc__, version="py_asciimath " + version)
    if arguments["--output"]:
        if arguments["--output"].lower() == "latex":
            print("Translating ...")
            print(
                ASCIIMath2Tex(
                    asciimath_grammar,
                    transformer=LatexTransformer(log=arguments["--log"]),
                ).asciimath2tex(" ".join(arguments["ASCIIMATH"]))
            )
        else:
            print("SUPPORTED OLANG: 'latex'", file=sys.stderr)
            sys.exit(1)
    else:
        print(arguments)
