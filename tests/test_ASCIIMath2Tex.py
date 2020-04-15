import unittest
from py_asciimath.translator.translator import ASCIIMath2Tex


class TestASCIIMath2Tex(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    # Returns True if the string contains 4 a.
    def test_asciimath2tex_ok_1(self):
        s = ASCIIMath2Tex(
            inplace=True, parser="lalr", lexer="contextual",
        ).translate("[[int x dx], [log(x+1)]]")
        self.assertEqual(
            s,
            r"$\left[\begin{matrix}"
            r"\int x \mathrm{dx}  \\  \log \left(x + 1\right)"
            r"\end{matrix}\right]$",
        )

    def test_asciimath2tex_ok_2(self):
        s = ASCIIMath2Tex(
            inplace=True, parser="lalr", lexer="contextual",
        ).translate(
            "((1,2))int sin{x^2}/4pidxroot(5)(x_1^2+x_2^2)", displaystyle=True
        )
        self.assertEqual(
            s,
            r"\[\left(\left(1 , 2\right)\right) \int \sin "
            r"\frac{x^{2}}{4} \pi \mathrm{dx} \sqrt[5]{x_{1}^{2} + x_{2}^{2}}\]",
        )

    def test_asciimath2tex_ok_3(self):
        s = ASCIIMath2Tex(
            inplace=True, parser="lalr", lexer="contextual",
        ).translate("lim_(N->oo) sum_(i=0)^N int_0^1 f(x)dx 3.14")
        self.assertEqual(
            s,
            r"$\lim_{N \to \infty} \sum_{i = 0}^{N} "
            r"\int_{0}^{1} f \left(x\right) \mathrm{dx} 3.14$",
        )

    def test_asciimath2tex_ok_4(self):
        s = ASCIIMath2Tex(
            inplace=True, parser="lalr", lexer="contextual",
        ).translate(
            """uuu_{2(x+1)=1)^{n}
            min{
                2x|x^{y+2} in bbb(N) wedge arccos root(3}(frac{1}{3x}) < i
                rarr Omega < b, 5=x
            }"""
        )
        self.assertEqual(
            s,
            r"$\bigcup_{2 \left(x + 1\right) = 1}^{n} "
            r"\min \left\{2 x | x^{y + 2} \in \mathbb{N} \wedge "
            r"\arccos \sqrt[3]{\frac{1}{3 x}} < i \rightarrow "
            r"\Omega < b , 5 = x\right\}$",
        )

    def test_asciimath2tex_ok_5(self):
        parser = ASCIIMath2Tex()
        s = parser.translate(
            """uuu_{2(x+1)=1)^{n}
            min{
                2x|x^{y+2} in bbb(N) wedge arccos root(3}(frac{1}{3x}) < i
                rarr Omega < b, 5=x
            }""",
            pprint=True,
        )
        self.assertEqual(
            s,
            r"$\bigcup_{2 \left(x + 1\right) = 1}^{n} "
            r"\min \left\{2 x | x^{y + 2} \in \mathbb{N} \wedge "
            r"\arccos \sqrt[3]{\frac{1}{3 x}} < i \rightarrow "
            r"\Omega < b , 5 = x\right\}$",
        )

    def test_asciimath2tex_ok_6(self):
        parser = ASCIIMath2Tex(log=True)
        s = parser.translate(
            "[(1,2), (2^|: 3 :|, (dstyle int x^{2(x-n)})), (2,4)]"
        )
        self.assertEqual(
            s,
            r"$\left[\begin{matrix}1  &  2  \\  2^{\left\vert3\right\vert}  "
            r"&  \left(\displaystyle{\int} x^{2 \left(x - n\right)}\right)  "
            r"\\  2  &  4\end{matrix}\right]$",
        )

    def test_asciimath2tex_ok_7(self):
        parser = ASCIIMath2Tex(log=True)
        s = parser.translate("langle [1,2], [2,int[3(x+1)]dx]:}")
        self.assertEqual(
            s,
            r"$\left\langle \begin{matrix}1  &  2  \\  2  "
            r"&  \int \left[3 \left(x + 1\right)\right] "
            r"\mathrm{dx}\end{matrix}\right.$",
        )


if __name__ == "__main__":
    unittest.main()
