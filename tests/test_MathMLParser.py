import unittest

from py_asciimath import PROJECT_ROOT
from py_asciimath.parser.parser import MathMLParser


class TestMathMLParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_mathmlparser_get_doctype(self):
        for network in [True, False]:
            for mml in ["mathml1", "mathml2", "mathml3"]:
                doctype = MathMLParser.get_doctype(mml, network)
                if network:
                    self.assertEqual(
                        doctype,
                        '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML {}.0//EN" '
                        '"http://www.w3.org/Math/DTD/{}/{}.dtd">'.format(
                            mml[-1], mml, mml
                        )
                        if mml != "mathml1"
                        else "<!DOCTYPE math SYSTEM "
                        '"http://www.w3.org/Math/DTD/mathml1/mathml.dtd">',
                    )
                else:
                    self.assertEqual(
                        doctype,
                        '<!DOCTYPE math SYSTEM "'
                        + PROJECT_ROOT
                        + '/dtd/{}/{}.dtd">'.format(mml, mml),
                    )
        self.assertRaises(
            NotImplementedError, MathMLParser.get_doctype, "a", False
        )

    def test_mathmlparser_get_doctype_version_ok(self):
        self.assertEqual(
            "3",
            MathMLParser.get_doctype_version(
                '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" '
                '"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd">'
            ),
        )
        self.assertEqual(
            "1",
            MathMLParser.get_doctype_version(
                '<!DOCTYPE math SYSTEM "'
                '"http://www.w3.org/Math/DTD/mathml1/mathml.dtd">'
            ),
        )
        self.assertEqual(
            None, MathMLParser.get_doctype_version(""),
        )
        self.assertRaises(
            Exception,
            MathMLParser.get_doctype_version,
            '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" '
            '"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd">\n'
            '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" '
            '"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd">',
        )

    def test_mathmlparser_get_encoding(self):
        self.assertRaises(
            Exception,
            MathMLParser.get_encoding,
            "<?xml version='1.0' encoding='UTF-8'?>"
            "<mi>+</mi><?xml version='1.0' encoding='UTF-8'?>",
        )
        self.assertRaises(
            Exception,
            MathMLParser.get_encoding,
            "<mi>+</mi><?xml version='1.0' encoding='UTF-8'?>",
        )
        self.assertEqual(
            "UTF-8",
            MathMLParser.get_encoding(
                "<?xml version='1.0' encoding='UTF-8'?><mi>+</mi>"
            ),
        )
        self.assertEqual(
            None, MathMLParser.get_encoding(""),
        )

    def test_mathmlparser_set_doctype(self):
        self.assertRaises(
            Exception,
            MathMLParser.set_doctype,
            "<?xml version='1.0' encoding='UTF-8'?>"
            + '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" '
            + '"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd">'
            + '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" '
            + '"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd">',
            False
        )
        s = (
            "<?xml version='1.0' encoding='UTF-8'?>"
            + '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" '
            + '"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd">'
        )
        self.assertEqual(
            "<?xml version='1.0' encoding='UTF-8'?>"
            + MathMLParser.get_doctype("mathml3", False),
            MathMLParser.set_doctype(s, False),
        )
        s = "<?xml version='1.0' encoding='UTF-8'?>"
        self.assertEqual(
            "<?xml version='1.0' encoding='UTF-8'?>"
            + MathMLParser.get_doctype("mathml1", False),
            MathMLParser.set_doctype(s, False, dtd="mathml1"),
        )
        s = (
            '<!DOCTYPE math SYSTEM "'
            + PROJECT_ROOT
            + '/dtd/mathml2/mathml2.dtd">'
        )
        self.assertEqual(s, MathMLParser.set_doctype(s, True))
        self.assertRaises(
            Exception,
            MathMLParser.set_doctype,
            "<?xml version='1.0' encoding='UTF-8'?>"
            "<?xml version='1.0' encoding='UTF-8'?>",
            False
        )
        self.assertRaises(
            Exception,
            MathMLParser.set_doctype,
            "<mi>+</mi><?xml version='1.0' encoding='UTF-8'?>",
            False
        )


if __name__ == "__main__":
    unittest.main()
