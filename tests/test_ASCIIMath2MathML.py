import unittest

from py_asciimath import PROJECT_ROOT
from py_asciimath.translator.translator import ASCIIMath2MathML


class TestASCIIMath2MathML(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_asciimath2mathml_ok_1(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            r"floor root n (f(x)) times a / b "
            r"sum_(i=1)^n i^3=(frac (n(n+1)_2) 2)^2",
            displaystyle=True,
            dtd_validation=True,
            dtd="mathml3",
            network=False,
            pprint=False,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            '<!DOCTYPE math SYSTEM "'
            + PROJECT_ROOT
            + '/dtd/mathml3/mathml3.dtd">\n<math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"><mstyle displaystyle="true"><mrow><mo>&lfloor;</mo><mrow><mrow><mroot><mrow><mrow><mo>f</mo><mrow><mo>(</mo><mrow><mi>x</mi></mrow><mo>)</mo></mrow></mrow></mrow><mrow><mi>n</mi></mrow></mroot></mrow></mrow><mo>&rfloor;</mo></mrow><mo>&times;</mo><mrow><mfrac><mrow><mi>a</mi></mrow><mrow><mi>b</mi></mrow></mfrac></mrow><mrow><msubsup><mrow><mo>&sum;</mo></mrow><mrow><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow></mrow><mrow><mi>n</mi></mrow></msubsup></mrow><mrow><msup><mrow><mi>i</mi></mrow><mrow><mn>3</mn></mrow></msup></mrow><mo>=</mo><mrow><msup><mrow><mrow><mo>(</mo><mrow><mrow><mfrac><mrow><mrow><mi>n</mi><mrow><msub><mrow><mrow><mo>(</mo><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow><mrow><mn>2</mn></mrow></msub></mrow></mrow></mrow><mrow><mn>2</mn></mrow></mfrac></mrow></mrow><mo>)</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mrow></mstyle></math>',
        )

    def test_asciimath2mathml_ok_2(self):
        s = ASCIIMath2MathML(log=True,).translate(
            "floor root n (f(x)) times a / b sum_(i=1)^n i^3=(frac (n(n+1)_2) 2)^2",
            pprint=True,
            dtd=None,
            displaystyle=True,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            '<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle displaystyle="true"><mrow><mo>&lfloor;</mo><mrow><mrow><mroot><mrow><mrow><mo>f</mo><mrow><mo>(</mo><mrow><mi>x</mi></mrow><mo>)</mo></mrow></mrow></mrow><mrow><mi>n</mi></mrow></mroot></mrow></mrow><mo>&rfloor;</mo></mrow><mo>&times;</mo><mrow><mfrac><mrow><mi>a</mi></mrow><mrow><mi>b</mi></mrow></mfrac></mrow><mrow><msubsup><mrow><mo>&sum;</mo></mrow><mrow><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow></mrow><mrow><mi>n</mi></mrow></msubsup></mrow><mrow><msup><mrow><mi>i</mi></mrow><mrow><mn>3</mn></mrow></msup></mrow><mo>=</mo><mrow><msup><mrow><mrow><mo>(</mo><mrow><mrow><mfrac><mrow><mrow><mi>n</mi><mrow><msub><mrow><mrow><mo>(</mo><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow><mrow><mn>2</mn></mrow></msub></mrow></mrow></mrow><mrow><mn>2</mn></mrow></mfrac></mrow></mrow><mo>)</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mrow></mstyle></math>',
        )

    def test_asciimath2mathml_ok_3(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            "floor root n (f(x)) times a / b sum_(i=1)^n i^3=(frac (n(n+1)_2) 2)^2",
            dtd="mathml2",
            displaystyle=False,
            pprint=False,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            '<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mo>&lfloor;</mo><mrow><mrow><mroot><mrow><mrow><mo>f</mo><mrow><mo>(</mo><mrow><mi>x</mi></mrow><mo>)</mo></mrow></mrow></mrow><mrow><mi>n</mi></mrow></mroot></mrow></mrow><mo>&rfloor;</mo></mrow><mo>&times;</mo><mrow><mfrac><mrow><mi>a</mi></mrow><mrow><mi>b</mi></mrow></mfrac></mrow><mrow><msubsup><mrow><mo>&sum;</mo></mrow><mrow><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow></mrow><mrow><mi>n</mi></mrow></msubsup></mrow><mrow><msup><mrow><mi>i</mi></mrow><mrow><mn>3</mn></mrow></msup></mrow><mo>=</mo><mrow><msup><mrow><mrow><mo>(</mo><mrow><mrow><mfrac><mrow><mrow><mi>n</mi><mrow><msub><mrow><mrow><mo>(</mo><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow><mrow><mn>2</mn></mrow></msub></mrow></mrow></mrow><mrow><mn>2</mn></mrow></mfrac></mrow></mrow><mo>)</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mrow></math>',
        )

    def test_asciimath2mathml_ok_4(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            "langle [1,2], [2,int[3(x+1)]dx]:}",
            dtd="mathml1",
            dtd_validation=True,
            displaystyle=True,
            pprint=False,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            '<!DOCTYPE math SYSTEM "'
            + PROJECT_ROOT
            + '/dtd/mathml1/mathml1.dtd">\n<math><mstyle displaystyle="true"><mrow><mo>&langle;</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>2</mn></mtd><mtd><mo>&Integral;</mo><mrow><mo>[</mo><mrow><mn>3</mn><mrow><mo>(</mo><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow><mo>]</mo></mrow><mi>dx</mi></mtd></mtr></mtable><mo/></mrow></mstyle></math>',
        )


if __name__ == "__main__":
    unittest.main()
