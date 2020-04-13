"""py_asciimath: a simple ASCIIMath/MathML/LaTeX converter

Usage:
  py_asciimath.py <EXP> from <ILANG> to <OLANG> [options]
  py_asciimath.py <EXP> (-i <ILANG> | --input=ILANG)
                        (-o <OLANG> | --output=OLANG)
                        [options]
  py_asciimath.py from-file <PATH> from <ILANG> to <OLANG> [options]
  py_asciimath.py from-file <PATH> (-i <ILANG> | --input=ILANG)
                                   (-o <OLANG> | --output=OLANG) [options]
  py_asciimath.py (-h | --help)
  py_asciimath.py --version

Options:
  --dstyle                      Add display style
  -i <ILANG> --input=ILANG      Input language
                                Supported input language: asciimath, mathml
  --log                         Log the transformation process
  --network                     Works only with ILANG=mathnml or OLANG=mathml
                                Use network to validate XML against DTD
  -o <OLANG> --output=OLANG     Output language
                                Supported output language: latex, mathml
  --pprint                      Works only with OLANG=mathml. Pretty print
  --to-file=OPATH               Save translation to OPATH file
  --validate-xml=MathMLDTD      Works only with OLANG=mathml
                                Validate against a MathML DTD
                                MathMLDTD can be: mathml1, mathml2 or mathml3
  --version                     Show version
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

from .parser.parser import ASCIIMath2MathML, ASCIIMath2Tex, MathML2Tex

_supported_ilang = ["asciimath", "mathml"]
_supported_olang = ["latex", "mathml"]


def main():
    arguments = docopt(__doc__)
    ilang = arguments["<ILANG>"].lower()
    olang = arguments["<OLANG>"].lower()
    if ilang == olang:
        print("Same input and output language. Nothing to do")
        sys.exit(0)
    elif ilang not in _supported_ilang:
        print("Supported <ILANG>: 'asciimath', 'mathml'", file=sys.stderr)
        sys.exit(1)
    elif olang not in _supported_olang:
        print("Supported <OLANG>: 'latex', 'mathml'", file=sys.stderr)
        sys.exit(1)
    exp = (
        "".join(arguments["<PATH>"])
        if arguments["from-file"]
        else "".join(arguments["<EXP>"])
    )
    validate = True if arguments["--validate-xml"] is not None else False
    if ilang == "asciimath":
        if olang == "latex":
            parser = ASCIIMath2Tex(log=arguments["--log"], inplace=True)
        elif olang == "mathml":
            parser = ASCIIMath2MathML(log=arguments["--log"], inplace=True)
    elif ilang == "mathml":
        parser = MathML2Tex()
    print(
        parser.translate(
            exp,
            displaystyle=arguments["--dstyle"],
            dtd=arguments["--validate-xml"],
            dtd_validation=validate,
            network=arguments["--network"],
            pprint=False,
            xml_pprint=arguments["--pprint"],
            from_file=arguments["from-file"],
            to_file=arguments["--to-file"],
        )
    )
    sys.exit(0)
