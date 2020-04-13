from py_asciimath import PROJECT_ROOT
from py_asciimath.grammar.asciimath_grammar import asciimath_grammar
from py_asciimath.parser.parser import (
    ASCIIMath2MathML,
    ASCIIMath2Tex,
    MathML2Tex,
)


if __name__ == "__main__":
    asciimath2mathml = ASCIIMath2MathML(
        asciimath_grammar, log=False, inplace=True
    )
    parsed = asciimath2mathml.translate(
        PROJECT_ROOT + "/../examples/asciimath_exp.txt",
        dtd="mathml2",
        dtd_validation=True,
        network=True,
        displaystyle=True,
        pprint=False,
        xml_pprint=False,
        from_file=True,
    )
    print(parsed)
    asciimath2tex = ASCIIMath2Tex(asciimath_grammar, log=False, inplace=True)
    parsed = asciimath2mathml.translate(
        PROJECT_ROOT + "/../examples/asciimath_exp.txt",
        displaystyle=True,
        pprint=False,
        from_file=True,
    )
    print(parsed)
    mathml2tex = MathML2Tex()
    parsed = mathml2tex.translate(
        PROJECT_ROOT + "/../examples/mathml_exp.xml",
        network=False,
        from_file=True,
    )
    print(parsed)
