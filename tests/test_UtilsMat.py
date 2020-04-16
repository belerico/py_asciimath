import unittest

from py_asciimath.utils.utils import UtilsMat


class TestUtilsMat(unittest.TestCase):
    def setUp(self):
        pass

    # Returns True if the string contains 4 a.
    def test_check_mat_ok_1(self):
        b, _ = UtilsMat.check_mat("[1,2], [1,2]")
        self.assertTrue(b)

    def test_check_mat_ok_2(self):
        b, _ = UtilsMat.check_mat("[], []")
        self.assertTrue(b)

    def test_check_mat_ok_3(self):
        b, _ = UtilsMat.check_mat("[[,[,]],[[,],]], [[[[,],],],[,[,[,]]]]")
        self.assertTrue(b)

    def test_check_mat_ok_4(self):
        b, _ = UtilsMat.check_mat("[,], [,]")
        self.assertTrue(b)

    def test_check_mat_fail_1(self):
        b, _ = UtilsMat.check_mat("[], [,]")
        self.assertFalse(b)

    def test_check_mat_fail_2(self):
        b, _ = UtilsMat.check_mat("[,], []")
        self.assertFalse(b)

    def test_check_mat_fail_3(self):
        b, _ = UtilsMat.check_mat("[,][,]")
        self.assertFalse(b)

    def test_check_mat_fail_4(self):
        b, _ = UtilsMat.check_mat("[,],[")
        self.assertFalse(b)

    def test_check_mat_fail_5(self):
        b, _ = UtilsMat.check_mat("[1,2],[1,2,[1,2],[3,4]")
        self.assertFalse(b)

    def test_check_mat_fail_6(self):
        b, _ = UtilsMat.check_mat("[,],")
        self.assertFalse(b)

    def test_check_mat_fail_7(self):
        b, _ = UtilsMat.check_mat("[,]],")
        self.assertFalse(b)

    def test_check_mat_fail_8(self):
        b, _ = UtilsMat.check_mat("[,],,")
        self.assertFalse(b)

    def test_check_mat_fail_9(self):
        b, _ = UtilsMat.check_mat("[][]")
        self.assertFalse(b)

    def test_check_mat_fail_10(self):
        b, _ = UtilsMat.check_mat("[]")
        self.assertFalse(b)

    def test_get_mat_ok_1(self):
        s = UtilsMat.get_latex_mat(
            "\\left[1 , 2\\right] , \\left[1 , 2\\right]"
        )
        self.assertEqual(s, "1  &  2  \\\\  1  &  2")

    def test_get_mat_ok_2(self):
        s = UtilsMat.get_latex_mat(
            "\\left[1 , 2\\right] , \\left[1 , \\right]"
        )
        self.assertEqual(s, "1  &  2  \\\\  1  &  \\null")

    def test_get_mat_ok_3(self):
        s = UtilsMat.get_latex_mat("\\left[\\right] , \\left[\\right]")
        self.assertEqual(s, "\\null  \\\\  \\null")

    def test_get_mat_ok_4(self):
        s = UtilsMat.get_latex_mat("\\left[,\\right] , \\left[,\\right]")
        self.assertEqual(s, "\\null & \\null  \\\\  \\null & \\null")

    def test_check_get_mat_ok_4(self):
        s = "\\left[2*[x+n], 3(int x dx)\\right], \\left[sqrt(x), a\\right]"
        b, row_par = UtilsMat.check_mat(s)
        self.assertTrue(b)
        self.assertEqual(row_par, ["[", "]"])
        m = UtilsMat.get_latex_mat(s, row_par)
        self.assertEqual(m, "2*[x+n] &  3(int x dx) \\\\  sqrt(x) &  a")

    def test_check_get_mat_fail_1(self):
        s = "\\left[2*[x+n], 3(int x dx)\\right, \\left[sqrt(x), a\\right]"
        b, row_par = UtilsMat.check_mat(s)
        self.assertFalse(b)
        self.assertEqual(row_par, [])
        m = UtilsMat.get_latex_mat(s, row_par)
        self.assertNotEqual(m, "2*[x+n] &  3(int x dx) \\\\ sqrt(x) &  a")

    def test_get_row_par_1(self):
        s = "{1+2]"
        i, row_par = UtilsMat.get_row_par(s)
        self.assertEqual(i, -1)
        self.assertEqual(row_par, [])

    def test_get_row_par_2(self):
        s = "{1+2]"
        ok, row_par = UtilsMat.check_mat(s)
        self.assertFalse(ok)
        self.assertEqual(row_par, [])

    def test_get_mathml_mat_1(self):
        s = "<mrow><mo>[</mo><mrow><mn>1</mn><mo>,</mo><mn>2</mn></mrow></mrow>"
        ok, row_par = UtilsMat.check_mat(s)
        self.assertFalse(ok)
        self.assertEqual(row_par, [])
        mat = UtilsMat.get_mathml_mat(s, row_par)
        self.assertEqual(s, mat)

    def test_get_mathml_mat_2(self):
        s = "<mrow><mo>[</mo><mrow><mn>1</mn><mo>,</mo><mo>[</mo><mrow><mn>2</mn></mrow><mo>]</mo></mrow><mo>]</mo></mrow>"
        ok, row_par = UtilsMat.check_mat(s)
        self.assertFalse(ok)
        self.assertEqual(row_par, [])


if __name__ == "__main__":
    unittest.main()
