import unittest

import lxml.etree

from py_asciimath.grammar.asciimath_grammar import asciimath_grammar
from py_asciimath.parser.parser import ASCIIMath2MathML
from py_asciimath.utils.utils import httplib


class TestUtilsMat(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_asciimath2tex_ok_1(self):
        try:
            _ = ASCIIMath2MathML(
                asciimath_grammar,
                inplace=True,
                log=False,
                parser="lalr",
                lexer="contextual",
            ).translate(
                "floor root n x times a / b sum_(i=1)^n i^3=(frac (n(n+1)_2) 2)^2",
                displaystyle=True,
                dtd_validation=True,
                dtd="mathml1",
                pprint=False,
            )
            ok = True
        except lxml.etree.XMLSyntaxError:
            ok = False
        except httplib.HTTPException:
            ok = True
        self.assertTrue(ok)

    def test_asciimath2tex_ok_2(self):
        s = ASCIIMath2MathML(asciimath_grammar, log=True,).translate(
            "floor root n x times a / b sum_(i=1)^n i^3=(frac (n(n+1)_2) 2)^2",
            pprint=True,
            dtd=None,
            displaystyle=True,
            xml_pprint=False
        )
        self.assertEqual(
            s,
            """<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" "http://www.w3.org/Math/DTD/mathml3/mathml3.dtd"><math xmlns=\'http://www.w3.org/1998/Math/MathML\'><mstyle displaystyle="true"><mrow><mo>&lfloor;</mo><mrow><mrow><mroot><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></mroot></mrow></mrow><mo>&rfloor;</mo></mrow><mo>&times;</mo><mrow><mfrac><mrow><mi>a</mi></mrow><mrow><mi>b</mi></mrow></mfrac></mrow><mrow><msubsup><mrow><mo>&sum;</mo></mrow><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi></mrow></msubsup></mrow><mrow><msup><mrow><mi>i</mi></mrow><mrow><mn>3</mn></mrow></msup></mrow><mo>=</mo><mrow><msup><mrow><mo>(</mo><mrow><mfrac><mrow><mi>n</mi><mrow><munder><mrow><mo>(</mo><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mn>2</mn></mrow></munder></mrow></mrow><mrow><mn>2</mn></mrow></mfrac></mrow><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup></mrow></mstyle></math>""",
        )

    def test_asciimath2tex_ok_3(self):
        s = ASCIIMath2MathML(
            asciimath_grammar,
            inplace=True,
            log=False,
            parser="lalr",
            lexer="contextual",
        ).translate(
            "floor root n x times a / b sum_(i=1)^n i^3=(frac (n(n+1)_2) 2)^2",
            dtd="mathml2",
            displaystyle=False,
            pprint=False,
            xml_pprint=False
        )
        self.assertEqual(
            s,
            """<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/mathml2.dtd"><math xmlns=\'http://www.w3.org/1998/Math/MathML\'><mrow><mo>&lfloor;</mo><mrow><mrow><mroot><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></mroot></mrow></mrow><mo>&rfloor;</mo></mrow><mo>&times;</mo><mrow><mfrac><mrow><mi>a</mi></mrow><mrow><mi>b</mi></mrow></mfrac></mrow><mrow><msubsup><mrow><mo>&sum;</mo></mrow><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi></mrow></msubsup></mrow><mrow><msup><mrow><mi>i</mi></mrow><mrow><mn>3</mn></mrow></msup></mrow><mo>=</mo><mrow><msup><mrow><mo>(</mo><mrow><mfrac><mrow><mi>n</mi><mrow><munder><mrow><mo>(</mo><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mn>2</mn></mrow></munder></mrow></mrow><mrow><mn>2</mn></mrow></mfrac></mrow><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup></mrow></math>""",
        )

    def test_asciimath2tex_ok_4(self):
        s = ASCIIMath2MathML(
            asciimath_grammar,
            inplace=True,
            log=False,
            parser="lalr",
            lexer="contextual",
        ).translate(
            "langle [1,2], [2,int[3(x+1)]dx]:}",
            dtd="mathml1",
            displaystyle=True,
            pprint=False,
            xml_pprint=False
        )
        self.assertEqual(
            s,
            """<!DOCTYPE math SYSTEM "http://www.w3.org/Math/DTD/mathml1/mathml.dtd"><math><mstyle displaystyle="true"><mo>&langle;</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>2</mn></mtd><mtd><mo>&Integral;</mo><mo>[</mo><mn>3</mn><mo>(</mo><mi>x</mi><mo>+</mo><mn>1</mn><mo>)</mo><mo>]</mo><mi>dx</mi></mtd></mtr></mtable><mo></mo></mstyle></math>""",
        )


if __name__ == "__main__":
    unittest.main()
