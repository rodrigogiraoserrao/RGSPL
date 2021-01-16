"""
Tests the evaluation of the basic data types and arrays of those.
"""

import unittest

from arraymodel import APLArray
from utils import APLTestCase, S

class TestScalarEvaluation(APLTestCase):
    """Test that scalars are evaluated conveniently."""

    def test_nonneg_integers(self):
        self.assertEqual("0", S(0))
        self.assertEqual("1", S(1))
        self.assertEqual("2", S(2))
        self.assertEqual("123456789987654321", S(123456789987654321))

    def test_negative_integers(self):
        self.assertEqual("¯1", S(-1))
        self.assertEqual("¯2", S(-2))
        self.assertEqual("¯0", S(0))
        self.assertEqual("¯973", S(-973))

    def test_floats(self):
        self.assertEqual("0.0", S(0))
        self.assertEqual("0.5", S(0.5))
        self.assertEqual("¯0.25", S(-0.25))
        self.assertEqual("¯0.125", S(-0.125))

    def test_complex_numbers(self):
        self.assertEqual("0J0", S(0))
        self.assertEqual("1J1", S(1 + 1j))
        self.assertEqual("3J¯0.5", S(3 - 0.5j))
        self.assertEqual("¯0.3J15", S(-0.3 + 15j))

    def test_redundant_parens(self):
        self.assertEqual("(0.2)", S(0.2))
        self.assertEqual("(((¯3)))", S(-3))
        self.assertEqual("((((((((3J4))))))))", S(3 + 4j))

class TestArrayEvaluation(APLTestCase):
    """Test that arrays (that are not scalars) are evaluated conveniently."""

    def test_simple_arrays(self):
        self.assertEqual("1 2 3 4", APLArray([4], [S(1), S(2), S(3), S(4)]))
        self.assertEqual("¯1 1 ¯1 1", APLArray([4], [S(-1), S(1), S(-1), S(1)]))
        self.assertEqual("(2.3 5.6 7.8 9)", APLArray([4], [S(2.3), S(5.6), S(7.8), S(9)]))
        self.assertEqual("0J1 ¯1J0 0J¯1 1", APLArray([4], [S(1j), S(-1), S(-1j), S(1)]))

    def test_nested_vectors(self):
        self.assertEqual(
            "(0 1) (2 3) (4 5)",
            APLArray([3], [APLArray([2], [S(0), S(1)]), APLArray([2], [S(2), S(3)]), APLArray([2], [S(4), S(5)])])
        )
        self.assertEqual(
            "1 2 3 (4 5) (6 7)",
            APLArray([5], [S(1), S(2), S(3), APLArray([2], [S(4), S(5)]), APLArray([2], [S(6), S(7)])])
        )
        self.assertEqual(
            "1 (2 (3 (4 5)))",
            APLArray([2], [S(1), APLArray([2], [S(2), APLArray([2], [S(3), APLArray([2], [S(4), S(5)])])])])
        )
        self.assertEqual(
            "(((1 2) 3) 4) 5",
            APLArray([2], [APLArray([2], [APLArray([2], [APLArray([2], [S(1), S(2)]), S(3)]), S(4)]), S(5)])
        )
