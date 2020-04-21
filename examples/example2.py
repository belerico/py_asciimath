from py_asciimath.translator.translator import (
    ASCIIMath2MathML,
    ASCIIMath2Tex,
    MathML2Tex,
    Tex2ASCIIMath
)


if __name__ == "__main__":
    print("ASCIIMath to MathML")
    asciimath2mathml = ASCIIMath2MathML(log=False, inplace=True)
    parsed = asciimath2mathml.translate(
        r"e^x > 0 forall x in RR",
        displaystyle=True,
        dtd="mathml2",
        dtd_validation=True,
        from_file=False,
        output="string",
        network=True,
        pprint=False,
        to_file=None,
        xml_declaration=True,
        xml_pprint=True,
    )

    print(parsed, "\n\nMathML to LaTeX")
    mathml2tex = MathML2Tex()
    parsed = mathml2tex.translate(parsed, network=False, from_file=False,)

    print(parsed, "\n\nASCIIMath to LaTeX")
    asciimath2tex = ASCIIMath2Tex(log=False, inplace=True)
    parsed = asciimath2tex.translate(
        r"e^x > 0 forall x in RR",
        displaystyle=True,
        from_file=False,
        pprint=False,
    )

    print(parsed, "\n\nLaTeX to ASCIIMath")
    tex2asciimath = Tex2ASCIIMath(log=False, inplace=True)
    parsed = tex2asciimath.translate(
        parsed,
        from_file=False,
        pprint=False,
    )
    print(parsed)
