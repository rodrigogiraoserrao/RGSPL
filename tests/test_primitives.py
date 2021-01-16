"""
Test the APL primitive functions.
"""

import unittest

from utils import run

class TestPlus(unittest.TestCase):
    """Test the primitive function +"""

    def test_scalar_conjugate(self):
        self.assertEqual(run("+0"), run("0"))
        self.assertEqual(run("+¯4.4"), run("¯4.4"))
        self.assertEqual(run("+0J1"), run("0J¯1"))
        self.assertEqual(run("+2.3J¯3.5"), run("2.3J3.5"))

    def test_vector_conjugate(self):
        self.assertEqual(
            run("+ 0 ¯4.4 0J1 2.3J¯3.5"),
            run("0 ¯4.4 0J¯1 2.3J3.5")
        )

    def test_nested_conjugate(self):
        self.assertEqual(
            run("+ 0J1 3J¯1 (3 1J¯0.33) (1J1 0 (0J¯0 0.1J0.1))"),
            run("0J¯1 3J1 (3 1J0.33) (1J¯1 0 (0 0.1J¯0.1))")
        )

    def test_scalar_addition(self):
        self.assertEqual(run("0 + 0"), run("0"))
        self.assertEqual(run("3 + 5"), run("8"))
        self.assertEqual(run("¯0.3 + 0.3"), run("0"))
        self.assertEqual(run("0J1 + 1"), run("1J1"))
        self.assertEqual(run("¯3J0.5 + 3J12"), run("0J12.5"))

    def test_vector_addition(self):
        self.assertEqual(
            run("0 1 2 + 3 4 5"),
            run("3 5 7")
        )
        self.assertEqual(
            run("0 3 ¯0.3 0J1 ¯3J0.5 + 0 5 0.3 1 3J12"),
            run("0 8 0 1J1 0J12.5")
        )

    def test_addition_pervasion(self):
        self.assertEqual(
            run("10 + 0 1 2 3 4 5"),
            run("10 11 12 13 14 15")
        )
        self.assertEqual(
            run("¯1 2 ¯3 4 ¯5 + 3"),
            run("2 5 0 7 ¯2")
        )
        self.assertEqual(
            run("0 (1 2) 0.1 + (1 2 3 4) (0.7 (1J1 2J3)) (5 (7 (9 10J1)))"),
            run("(1 2 3 4) (1.7 (3J1 4J3)) (5.1 (7.1 (9.1 10.1J1)))")
        )
