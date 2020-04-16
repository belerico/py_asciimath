import os
import unittest

import lxml.etree

from py_asciimath import PROJECT_ROOT
from py_asciimath.grammar.asciimath_grammar import asciimath_grammar
from py_asciimath.transformer.transformer import MathMLTransformer
from py_asciimath.translator.translator import (
    ASCIIMath2MathML,
    ASCIIMathTranslator,
    MathML2Tex,
)


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

    def test_asciimath2mathml_ok_5(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            '\\ "setminus with color" color(red)(x) root(n)(x)',
            dtd="mathml2",
            dtd_validation=False,
            network=False,
            output="string",
            xml_declaration=False,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mo>&setminus;</mo><mtext>setminus with color</mtext><mrow><mstyle mathcolor='red'><mrow><mrow><mi>x</mi></mrow></mrow></mstyle></mrow><mrow><mroot><mrow><mrow><mi>x</mi></mrow></mrow><mrow><mrow><mi>n</mi></mrow></mrow></mroot></mrow></math>",
        )

    def test_asciimath2mathml_xml_fields_ok_1(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            "1",
            dtd="mathml1",
            dtd_validation=False,
            network=True,
            xml_declaration=True,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            "<?xml version='1.0' encoding='UTF-8'?>\n<math><mn>1</mn></math>",
        )

    def test_asciimath2mathml_xml_fields_ok_2(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            "1",
            dtd="mathml1",
            dtd_validation=True,
            network=True,
            xml_declaration=True,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            "<?xml version='1.0' encoding='UTF-8'?>\n<!DOCTYPE math SYSTEM \"http://www.w3.org/Math/DTD/mathml1/mathml.dtd\">\n<math><mn>1</mn></math>",
        )

    def test_asciimath2mathml_xml_fields_ok_3(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            "1",
            dtd="mathml2",
            dtd_validation=True,
            network=True,
            xml_declaration=False,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/mathml2.dtd">\n<math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"><mn>1</mn></math>',
        )

    def test_asciimath2mathml_xml_fields_ok_4(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            "1",
            dtd="mathml2",
            dtd_validation=True,
            network=False,
            output="string",
            xml_declaration=False,
            xml_pprint=False,
        )
        self.assertEqual(
            s,
            '<!DOCTYPE math SYSTEM "'
            + PROJECT_ROOT
            + '/dtd/mathml2/mathml2.dtd">\n<math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"><mn>1</mn></math>',
        )

    def test_asciimath2mathml_output_1(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            "1",
            dtd="mathml2",
            dtd_validation=True,
            network=False,
            output="etree",
            xml_declaration=False,
            xml_pprint=False,
        )
        self.assertIsInstance(s, lxml.etree._Element)

    def test_asciimath2mathml_output_2(self):
        self.assertRaises(
            NotImplementedError,
            ASCIIMath2MathML(
                inplace=True, log=False, parser="lalr", lexer="contextual",
            ).translate,
            "1",
            dtd="mathml2",
            dtd_validation=True,
            network=False,
            output=None,
            xml_declaration=False,
            xml_pprint=False,
        )

    def test_asciimath2mathml_from_to_file_1(self):
        s = ASCIIMath2MathML(
            inplace=True, log=False, parser="lalr", lexer="contextual",
        ).translate(
            "a + b",
            dtd="mathml2",
            dtd_validation=False,
            network=False,
            output="string",
            xml_declaration=False,
            xml_pprint=False,
            to_file=PROJECT_ROOT + "/../mathml.xml",
        )
        s = self.assertEqual(
            s,
            '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>+</mo><mi>b</mi></math>',
        )
        self.assertTrue(os.path.exists(PROJECT_ROOT + "/../mathml.xml"))
        self.assertEqual(
            "$ a+b$",
            MathML2Tex().translate(
                PROJECT_ROOT + "/../mathml.xml", from_file=True
            ),
        )

    def test_asciimath2mathml_from_to_file_2(self):
        self.assertRaises(
            FileNotFoundError, MathML2Tex().translate, "$a+b$", from_file=True,
        )

    def test_asciimath2mathml_as_asciimathtranslator_1(self):
        self.assertEqual(
            "<mi>a</mi><mo>+</mo><mi>b</mi>",
            ASCIIMathTranslator(
                asciimath_grammar, MathMLTransformer(log=False)
            ).translate("a + b"),
        )


if __name__ == "__main__":
    unittest.main()
