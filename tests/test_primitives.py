"""
Test the APL primitive functions.
"""

from utils import APLTestCase

class TestPlus(APLTestCase):
    """Test the primitive function +."""

    def test_conjugate(self):
        # With scalars.
        self.assertEqual("+0", "0")
        self.assertEqual("+¯4.4", "¯4.4")
        self.assertEqual("+0J1", "0J¯1")
        self.assertEqual("+2.3J¯3.5", "2.3J3.5")
        # With a vector argument.
        self.assertEqual(
            "+ 0 ¯4.4 0J1 2.3J¯3.5",
            "0 ¯4.4 0J¯1 2.3J3.5"
        )
        # With a nested argument.
        self.assertEqual(
            "+ 0J1 3J¯1 (3 1J¯0.33) (1J1 0 (0J¯0 0.1J0.1))",
            "0J¯1 3J1 (3 1J0.33) (1J¯1 0 (0 0.1J¯0.1))"
        )

    def test_addition(self):
        # With scalar arguments.
        self.assertEqual("0 + 0", "0")
        self.assertEqual("3 + 5", "8")
        self.assertEqual("¯0.3 + 0.3", "0")
        self.assertEqual("0J1 + 1", "1J1")
        self.assertEqual("¯3J0.5 + 3J12", "0J12.5")
        # With vector arguments.
        self.assertEqual(
            "0 1 2 + 3 4 5",
            "3 5 7"
        )
        self.assertEqual(
            "0 3 ¯0.3 0J1 ¯3J0.5 + 0 5 0.3 1 3J12",
            "0 8 0 1J1 0J12.5"
        )
        # Testing uneven pervasion.
        self.assertEqual(
            "10 + 0 1 2 3 4 5",
            "10 11 12 13 14 15"
        )
        self.assertEqual(
            "¯1 2 ¯3 4 ¯5 + 3",
            "2 5 0 7 ¯2"
        )
        self.assertEqual(
            "0 (1 2) 0.1 + (1 2 3 4) (0.7 (1J1 2J3)) (5 (7 (9 10J1)))",
            "(1 2 3 4) (1.7 (3J1 4J3)) (5.1 (7.1 (9.1 10.1J1)))"
        )

class TestMinus(APLTestCase):
    """Test the primitive function -."""

    def test_symmetric(self):
        # With scalars.
        self.assertEqual("-0", "0")
        self.assertEqual("-¯4.4", "4.4")
        self.assertEqual("-0J1", "0J¯1")
        self.assertEqual("-2.3J¯3.5", "¯2.3J3.5")
        # With a vector argument.
        self.assertEqual(
            "- 0 ¯4.4 0J1 2.3J¯3.5",
            "0 4.4 0J¯1 ¯2.3J3.5"
        )
        # With a nested argument.
        self.assertEqual(
            "- 0J1 3J¯1 (3 1J¯0.33) (1J1 0 (0J¯0 0.1J0.1))",
            "0J¯1 ¯3J1 (¯3 ¯1J0.33) (¯1J¯1 0 (0 ¯0.1J¯0.1))"
        )

    def test_subtraction(self):
        # With scalar arguments.
        self.assertEqual("0 - 0", "0")
        self.assertEqual("3 - 5", "¯2")
        self.assertEqual("¯0.3 - 0.3", "¯0.6")
        self.assertEqual("0J1 - 1", "¯1J1")
        self.assertEqual("¯3J0.5 - 3J12", "¯6J¯11.5")
        # With vector arguments.
        self.assertEqual(
            "0 1 2 - 3 4 5",
            "¯3 ¯3 ¯3"
        )
        self.assertEqual(
            "0 3 ¯0.3 0J1 ¯3J0.5 - 0 5 0.3 1 3J12",
            "0 ¯2 ¯0.6 ¯1J1 ¯6J¯11.5"
        )
        # Testing uneven pervasion.
        self.assertEqual(
            "10 - 0 1 2 3 4 5",
            "10 9 8 7 6 5"
        )
        self.assertEqual(
            "¯1 2 ¯3 4 ¯5 - 3",
            "¯4 ¯1 ¯6 1 ¯8"
        )
        self.assertEqual(
            "0 (1 2) 0.1 - (1 2 3 4) (0.5 (1J1 2J3)) (5 (7 (9 10J1)))",
            "(¯1 ¯2 ¯3 ¯4) (0.5 (1J¯1 0J¯3)) (¯4.9 (¯6.9 (¯8.9 ¯9.9J¯1)))"
        )

class TestTimes(APLTestCase):
    """Test the primitive function ×."""

    def test_sign(self):
        self.assertEqual("×0", "0")
        self.assertEqual("×¯1", "¯1")
        self.assertEqual("×¯3", "¯1")
        self.assertEqual("×1", "1")
        self.assertEqual("×51.6", "1")
        # Complex numbers.
        self.assertEqual("×0J1", "0J1")
        self.assertEqual("×0J¯1", "0J¯1")
        self.assertEqual("×3J¯4", "0.6J¯0.8")
        self.assertEqual("×¯7J24", "¯0.28J0.96")
        # With a vector argument.
        self.assertEqual(
            "×0 ¯1 ¯3 1 51.6 0J1 0J¯1 3J¯4 ¯7J24",
            "0 ¯1 ¯1 1 1 0J1 0J¯1 0.6J¯0.8 ¯0.28J0.96"
        )
        # With a nested argument.
        self.assertEqual(
            "×0 (¯1 ¯3 1) (51.6 0J1 (0J¯1 3J¯4 ¯7J24))",
            "0 (¯1 ¯1 1) (1 0J1 (0J¯1 0.6J¯0.8 ¯0.28J0.96))"
        )
