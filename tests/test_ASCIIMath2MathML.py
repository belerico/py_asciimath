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
            """<mrow><mrow><mo>(</mo><mrow><msubsup><mi>a</mi> <mn>2</mn> <mn>3</mn></msubsup></mrow> <mrow><mo>+</mo></mrow> <mrow><msup><mi>b</mi> <mn>2</mn></msup></mrow><mo>)</mo></mrow></mrow> <mrow><mo>&#x22C5;</mo></mrow> <mrow><mn>2</mn></mrow>""",
        )

    def test_asciimath2tex_ok_2(self):
        s = ASCIIMath2MathML(
            asciimath_grammar, inplace=True, parser="lalr", lexer="contextual",
        ).translate("bigcup (a_2^3+b^2) * 2")
        self.assertEqual(
            s,
            """<mrow><mo>&#x22C3;</mo></mrow> <mrow><mrow><mo>(</mo><mrow><msubsup><mi>a</mi> <mn>2</mn> <mn>3</mn></msubsup></mrow> <mrow><mo>+</mo></mrow> <mrow><msup><mi>b</mi> <mn>2</mn></msup></mrow><mo>)</mo></mrow></mrow> <mrow><mo>&#x22C5;</mo></mrow> <mrow><mn>2</mn></mrow>""",
        )


if __name__ == "__main__":
    unittest.main()
