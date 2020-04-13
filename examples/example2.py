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
        r"langle [bigcup Theta CC NN QQ RR ZZ 1,twoheadrightarrowtail cdot 2], "
        r"[rarr 2,int[3(x+1)]dx]:}",
        dtd="mathml2",
        dtd_validation=True,
        network=True,
        displaystyle=True,
        pprint=False,
        xml_pprint=False,
        from_file=False,
    )
    print(parsed)
    asciimath2tex = ASCIIMath2Tex(asciimath_grammar, log=False, inplace=True)
    parsed = asciimath2mathml.translate(
        r"langle [bigcup Theta CC NN QQ RR ZZ 1,twoheadrightarrowtail cdot 2], "
        r"[rarr 2,int[3(x+1)]dx]:}",
        displaystyle=True,
        pprint=False,
        from_file=False,
    )
    print(parsed)
    mathml2tex = MathML2Tex()
    parsed = mathml2tex.translate(parsed, network=False, from_file=False,)
    print(parsed)
