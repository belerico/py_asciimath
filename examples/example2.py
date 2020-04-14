from py_asciimath.parser.parser import (
    ASCIIMath2MathML,
    ASCIIMath2Tex,
    MathML2Tex,
)


if __name__ == "__main__":
    print("ASCIIMath to MathML")
    asciimath2mathml = ASCIIMath2MathML(log=False, inplace=True)
    parsed = asciimath2mathml.translate(
        r"e^x > 0 forall x in RR",
        dtd="mathml2",
        dtd_validation=True,
        network=True,
        displaystyle=True,
        pprint=False,
        xml_pprint=True,
        from_file=False,
    )

    print(parsed, "\n\nMathML to LaTeX")
    mathml2tex = MathML2Tex()
    parsed = mathml2tex.translate(parsed, network=False, from_file=False,)

    print(parsed, "\n\nASCIIMath to LaTeX")
    asciimath2tex = ASCIIMath2Tex(log=False, inplace=True)
    parsed = asciimath2tex.translate(
        r"e^x > 0 forall x in RR",
        displaystyle=True,
        pprint=False,
        from_file=False,
    )
    print(parsed)
