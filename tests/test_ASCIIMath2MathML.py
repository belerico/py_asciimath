import unittest
from py_asciimath.grammar.asciimath_grammar import asciimath_grammar
from py_asciimath.parser.parser import ASCIIMath2MathML


class TestUtilsMat(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    # Returns True if the string contains 4 a.
    def test_asciimath2tex_ok_1(self):
        s = ASCIIMath2MathML(
            asciimath_grammar, inplace=True, parser="lalr", lexer="contextual",
        ).translate("root n x times star prod ^^ cup bigcap a / b sum_(i=1)^n i^3=(frac (n(n+1)) 2)^2")
        self.assertEqual(
            s,
            """<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" "http://www.w3.org/Math/DTD/mathml3/mathml3.dtd"><math xmlns='http://www.w3.org/1998/Math/MathML'><mroot><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></mroot><mo>&times;</mo><mo>&Star;</mo><mo>&prod;</mo><mo>&wedge;</mo><mo>&cup;</mo><mo>&bigcap;</mo><mfrac><mrow><mi>a</mi></mrow><mrow><mi>b</mi></mrow></mfrac><msubsup><mrow><mo>&sum;</mo></mrow><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi></mrow></msubsup><msup><mrow><mi>i</mi></mrow><mrow><mn>3</mn></mrow></msup><mo>=</mo><msup><mrow><mo>(</mo><mfrac><mrow><mi>n</mi><mo>(</mo><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mn>2</mn></mrow></mfrac><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup></math>""",
        )

    def test_asciimath2tex_ok_2(self):
        s = ASCIIMath2MathML(
            asciimath_grammar, inplace=True, parser="lalr", lexer="contextual",
        ).translate("root n x sum_(i=1)^n i^3=(frac (n(n+1)) 2)^2")
        self.assertEqual(
            s,
            """<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" "http://www.w3.org/Math/DTD/mathml3/mathml3.dtd"><math xmlns='http://www.w3.org/1998/Math/MathML'><mroot><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></mroot><msubsup><mrow><mo>&sum;</mo></mrow><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi></mrow></msubsup><msup><mrow><mi>i</mi></mrow><mrow><mn>3</mn></mrow></msup><mo>=</mo><msup><mrow><mo>(</mo><mfrac><mrow><mi>n</mi><mo>(</mo><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mn>2</mn></mrow></mfrac><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup></math>""",
        )


if __name__ == "__main__":
    unittest.main()
