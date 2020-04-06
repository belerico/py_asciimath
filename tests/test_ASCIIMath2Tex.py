import unittest
from py_asciimath.parser.const import asciimath_grammar
from py_asciimath.parser.parser import ASCIIMath2Tex, LatexTransformer


class TestUtilsMat(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.parser = ASCIIMath2Tex(
            asciimath_grammar,
            cache=True,
            inplace=True,
            parser="lalr",
            lexer="contextual",
            transformer=LatexTransformer(log=False),
        )

    # Returns True if the string contains 4 a.
    def test_asciimath2tex_ok_1(self):
        s = self.parser.asciimath2tex("[[int x dx], [log(x+1)]]")
        self.assertEqual(
            s,
            r"\left[\begin{matrix}\int x dx \\ \log \left(x + 1\right)\end{matrix}\right]",
        )

    def test_asciimath2tex_ok_2(self):
        s = self.parser.asciimath2tex(
            "((1,2))int sin{x^2}/4pidxroot(5)(x_1^2+x_2^2)"
        )
        self.assertEqual(
            s,
            r"\left(\left(1 , 2\right)\right) \int \sin \frac{x^{2}}{4} \pi dx \sqrt[5]{x_{1}^{2} + x_{2}^{2}}",
        )

    def test_asciimath2tex_ok_3(self):
        s = self.parser.asciimath2tex("lim_(N->oo) sum_(i=0)^N int_0^1 f(x)dx")
        self.assertEqual(
            s,
            r"\lim_{N \to \infty} \sum_{i = 0}^{N} \int_{0}^{1} f \left(x\right) dx",
        )

    def test_asciimath2tex_ok_4(self):
        s = self.parser.asciimath2tex(
            """uuu_{2(x+1)=1)^{n}
            min{
                2x|x^{y+2} in bbb(N) wedge arccos root(3}(frac{1}{3x}) < i rarr Omega < b, 5=x
            }"""
        )
        self.assertEqual(
            s,
            r"\bigcup_{2 \left(x + 1\right) = 1}^{n} \min \left\{2 x | x^{y + 2} \in \mathbb{N} \wedge \arccos \sqrt[3]{\frac{1}{3 x}} < i \rightarrow \Omega < b , 5 = x\right\}",
        )


if __name__ == "__main__":
    unittest.main()
