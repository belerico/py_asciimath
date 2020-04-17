from py_asciimath import PROJECT_ROOT
from py_asciimath.translator.translator import (
    ASCIIMath2MathML,
    ASCIIMath2Tex,
    MathML2Tex,
)


if __name__ == "__main__":
    print("ASCIIMath to MathML")
    asciimath2mathml = ASCIIMath2MathML(log=False, inplace=True)
    parsed = asciimath2mathml.translate(
        PROJECT_ROOT + "/../examples/asciimath_exp.txt",
        displaystyle=True,
        dtd="mathml2",
        dtd_validation=True,
        from_file=True,
        output="string",
        network=True,
        pprint=False,
        to_file=None,
        xml_declaration=True,
        xml_pprint=True,
    )

    print(parsed, "\n\nASCIIMath to LaTeX")
    asciimath2tex = ASCIIMath2Tex(log=False, inplace=True)
    parsed = asciimath2tex.translate(
        PROJECT_ROOT + "/../examples/asciimath_exp.txt",
        displaystyle=True,
        from_file=True,
        pprint=False,
        to_file=None,
    )

    print(parsed, "\n\nMathML to LaTeX")
    mathml2tex = MathML2Tex()
    parsed = mathml2tex.translate(
        PROJECT_ROOT + "/../examples/mathml_exp.xml",
        from_file=True,
        network=False,
        to_file=None,
    )
    print(parsed)
