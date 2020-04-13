from py_asciimath.parser.parser import (
    ASCIIMath2MathML,
    ASCIIMath2Tex,
    MathML2Tex,
)


if __name__ == "__main__":
    print("ASCIIMath to MathML")
    asciimath2mathml = ASCIIMath2MathML(log=False, inplace=True)
    parsed = asciimath2mathml.translate(
        r"langle [bigcup Theta CC NN QQ RR ZZ 1,twoheadrightarrowtail cdot 2],"
        r"[rarr 2,int[3(x+1)]dx]:}",
        dtd="mathml2",
        dtd_validation=True,
        network=True,
        displaystyle=True,
        pprint=False,
        xml_pprint=False,
        from_file=False,
    )

    print(parsed, "\n\nMathML to LaTeX")
    mathml2tex = MathML2Tex()
    parsed = mathml2tex.translate(parsed, network=False, from_file=False,)

    print(parsed, "\n\nASCIIMath to LaTeX")
    asciimath2tex = ASCIIMath2Tex(log=False, inplace=True)
    parsed = asciimath2tex.translate(
        r"langle [bigcup Theta CC NN QQ RR ZZ 1,twoheadrightarrowtail cdot 2],"
        r"[rarr 2,int[3(x+1)]dx]:}",
        displaystyle=True,
        pprint=False,
        from_file=False,
    )
    print(parsed)
