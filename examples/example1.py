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
        dtd="mathml2",
        dtd_validation=True,
        network=True,
        displaystyle=True,
        pprint=False,
        xml_pprint=False,
        from_file=True,
    )
    print(parsed, "\n\nASCIIMath to LaTeX")
    asciimath2tex = ASCIIMath2Tex(log=False, inplace=True)
    parsed = asciimath2mathml.translate(
        PROJECT_ROOT + "/../examples/asciimath_exp.txt",
        displaystyle=True,
        pprint=False,
        from_file=True,
    )
    print(parsed, "\n\nMathML to LaTeX")
    mathml2tex = MathML2Tex()
    parsed = mathml2tex.translate(
        PROJECT_ROOT + "/../examples/mathml_exp.xml",
        network=False,
        from_file=True,
    )
    print(parsed)
