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
        ).translate("(a_2^3+b^2) * 2")
        self.assertEqual(
            s,
            """<mo>(</mo><msubsup><mrow><mi>a</mi></mrow><mrow><mn>2</mn></mrow><mrow><mn>3</mn></mrow></msubsup><mo>+</mo><msup><mrow><mi>b</mi></mrow><mrow><mn>2</mn></mrow></msup><mo>)</mo><mo>&#x22C5;</mo><mn>2</mn>""",
        )

    def test_asciimath2tex_ok_2(self):
        s = ASCIIMath2MathML(
            asciimath_grammar, inplace=True, parser="lalr", lexer="contextual",
        ).translate("root n x sum_(i=1)^n i^3=(frac (n(n+1)) 2)^2")
        self.assertEqual(
            s,
            """<mroot><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></mroot><msubsup><mrow><mo>&#x2211;</mo></mrow><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi></mrow></msubsup><msup><mrow><mi>i</mi></mrow><mrow><mn>3</mn></mrow></msup><mo>=</mo><msup><mrow><mo>(</mo><mfrac><mrow><mi>n</mi><mo>(</mo><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mn>2</mn></mrow></mfrac><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup>""",
        )


if __name__ == "__main__":
    unittest.main()
