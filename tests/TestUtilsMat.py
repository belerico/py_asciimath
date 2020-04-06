import unittest
from utils.utils import UtilsMat


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

    def test_check_mat_ok_3(self):
        b, _ = UtilsMat.check_mat("[,], [,]")
        self.assertTrue(b)

    def test_check_mat_fail_1(self):
        b, _ = UtilsMat.check_mat("[], [,]")
        self.assertFalse(b)

    def test_check_mat_fail_2(self):
        b, _ = UtilsMat.check_mat("[,], []")
        self.assertFalse(b)

    def test_check_mat_fail_3(self):
        b, _ = UtilsMat.check_mat("[,],")
        self.assertFalse(b)

    def test_get_mat_ok_1(self):
        s = UtilsMat.get_mat("\\left[1 , 2\\right] , \\left[1 , 2\\right]")
        self.assertEqual(s, "1  &  2 \\\\ 1  &  2")

    def test_get_mat_ok_2(self):
        s = UtilsMat.get_mat("\\left[1 , 2\\right] , \\left[1 , \\right]")
        self.assertEqual(s, "1  &  2 \\\\ 1  &  \\null")

    def test_get_mat_ok_3(self):
        s = UtilsMat.get_mat("\\left[\\right] , \\left[\\right]")
        self.assertEqual(s, "\\null \\\\ \\null")

    def test_get_mat_ok_4(self):
        s = UtilsMat.get_mat("\\left[,\\right] , \\left[,\\right]")
        self.assertEqual(s, "\\null & \\null \\\\ \\null & \\null")

    def test_check_get_mat_ok_4(self):
        s = "\\left[2*[x+n], 3(int x dx)\\right], \\left[sqrt(x), a\\right]"
        b, row_par = UtilsMat.check_mat(s)
        self.assertTrue(b)
        self.assertEqual(row_par, ["[", "]"])
        m = UtilsMat.get_mat(s, row_par)
        self.assertEqual(m, "2*[x+n] &  3(int x dx) \\\\ sqrt(x) &  a")


if __name__ == "__main__":
    unittest.main()
