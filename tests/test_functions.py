"""
Basic tests for the APL primitive functions.

The tests presented here only use a single primitive per test.
"""

from arraymodel import APLArray
from utils import APLTestCase, run, S

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

    def test_multiplication(self):
        self.assertEqual("0 × 0", "0")
        self.assertEqual("1 × 0", "0")
        self.assertEqual("0 × 1", "0")
        self.assertEqual("1 × 0J¯3.3", "0J¯3.3")
        self.assertEqual("13 × 12", "156")
        # Complex numbers.
        self.assertEqual("0J1 × 0J1", "¯1")
        self.assertEqual("0J1 × 0J¯1", "1")
        self.assertEqual("3J4 × 3J4", "¯7J24")
        self.assertEqual("0J0 × 45.3J¯42", "0")
        # Vector arguments.
        self.assertEqual(
            "0 1 0 1 13 0J1 0J1 3J4 0J0 × 0 0 1 0J¯3.3 12 0J1 0J¯1 3J4 45.3J¯42",
            "0 0 0 0J¯3.3 156 ¯1 1 ¯7J24 0"
        )
        self.assertEqual(
            "1 × 0 0 1 0J¯3.3 12 0J1 0J¯1 3J4 45.3J¯42",
            "0 0 1 0J¯3.3 12 0J1 0J¯1 3J4 45.3J¯42"
        )
        self.assertEqual(
            "0 0 1 0J¯3.3 12 0J1 0J¯1 3J4 45.3J¯42 × 2",
            "0 0 2 0J¯6.6 24 0J2 0J¯2 6J8 90.6J¯84"
        )
        # Test nesting.
        self.assertEqual(
            "0 (1 0) (1 13 (0J1 0J1) 3J4) 0J0 × 0 (0 1) (0J¯3.3 12 (0J1 0J¯1) 3J4) 45.3J¯42",
            "0 (0 0) (0J¯3.3 156 (¯1 1) ¯7J24) 0"
        )

class TestDivide(APLTestCase):
    """Test the primitive function ÷."""

    def test_inverse(self):
        self.assertEqual("÷1", "1")
        self.assertEqual("÷2", "0.5")
        self.assertEqual("÷4", "0.25")
        self.assertEqual("÷¯8", "¯0.125")
        # Complex numbers.
        self.assertEqual("÷0J1", "0J¯1")
        self.assertEqual("÷1J1", "0.5J¯0.5")
        self.assertEqual("÷¯1J1", "¯0.5J¯0.5")
        self.assertEqual("÷¯1J¯1", "¯0.5J0.5")
        self.assertEqual("÷1J¯1", "0.5J0.5")
        # With a vector argument.
        self.assertEqual(
            "÷1 2 4 ¯8 0J1 1J1 ¯1J1 ¯1J¯1 1J¯1",
            "1 0.5 0.25 ¯0.125 0J¯1 0.5J¯0.5 ¯0.5J¯0.5 ¯0.5J0.5 0.5J0.5"
        )
        # With a nested argument.
        self.assertEqual(
            "÷(1 2 (4 ¯8 0J1) (1J1 ¯1J1 ¯1J¯1)) 1J¯1",
            "(1 0.5 (0.25 ¯0.125 0J¯1) (0.5J¯0.5 ¯0.5J¯0.5 ¯0.5J0.5)) 0.5J0.5"
        )

    def test_division(self):
        self.assertEqual("1 ÷ 1", "1")
        self.assertEqual("¯46.5 ÷ 1", "¯46.5")
        self.assertEqual("3J¯4 ÷ 0J2", "¯2J¯1.5")
        self.assertEqual("¯7J24 ÷ 3J4", "3J4")
        self.assertEqual("156 ÷ 13", "12")
        # With vector arguments.
        self.assertEqual(
            "1 ¯46.5 3J¯4 ¯7J24 156 ÷ 0J1",
            "0J¯1 0J46.5 ¯4J¯3 24J7 0J¯156"
        )
        self.assertEqual(
            "12 ÷ 1 2 3 4 6 8 12 24",
            "12 6 4 3 2 1.5 1 0.5"
        )
        self.assertEqual(
            "1 ¯46.5 3J¯4 ¯7J24 156 1 12 ÷ 1 1 0J2 3J4 13 0J1 24",
            "1 ¯46.5 ¯2J¯1.5 3J4 12 0J¯1 0.5"
        )
        # With a nested argument.
        self.assertEqual(
            "12 (1 3J¯4 ¯7J24) ÷ (1 2 3 4) 0J1",
            "(12 6 4 3) (0J¯1 ¯4J¯3 24J7)"
        )

class TestCeiling(APLTestCase):
    """Test the primitive function ⌈."""

    def test_ceiling(self):
        self.assertEqual("⌈0", "0")
        self.assertEqual("⌈1", "1")
        self.assertEqual("⌈¯1", "¯1")
        self.assertEqual("⌈0.1", "1")
        self.assertEqual("⌈0.999", "1")
        self.assertEqual("⌈¯1.5", "¯1")

    def test_max(self):
        self.assertEqual("0 ⌈ 1", "1")
        self.assertEqual("1.5 ⌈ 3.4", "3.4")
        self.assertEqual("¯1 ⌈ ¯1.1", "¯1")
        self.assertEqual("0 ⌈ 0", "0")
        self.assertEqual("0.333 ⌈ 0.334", "0.334")

class TestFloor(APLTestCase):
    """Test the primitive function ⌊."""

    def test_floor(self):
        self.assertEqual("⌊0", "0")
        self.assertEqual("⌊1", "1")
        self.assertEqual("⌊¯1", "¯1")
        self.assertEqual("⌊0.1", "0")
        self.assertEqual("⌊0.999", "0")
        self.assertEqual("⌊¯1.5", "¯2")

    def test_min(self):
        self.assertEqual("0 ⌊ 1", "0")
        self.assertEqual("1.5 ⌊ 3.4", "1.5")
        self.assertEqual("¯1 ⌊ ¯1.1", "¯1.1")
        self.assertEqual("0 ⌊ 0", "0")
        self.assertEqual("0.333 ⌊ 0.334", "0.333")

class TestTacks(APLTestCase):
    """Test the primitive functions ⊢ and ⊣."""

    def test(self):
        strings = [
            "1",
            "1 2 3",
            "1 (2 3) 4.5 0J3",
            "4.5",
            "¯1",
            "0J1",
        ]
        for right in strings:
            # Test monadic version.
            with self.subTest(right=right):
                self.assertEqual(f"⊢{right}", right)
                self.assertEqual(f"⊣{right}", right)

            # Test dyadic version.
            for left in strings:
                with self.subTest(left=left, right=right):
                    self.assertEqual(f"{left} ⊢ {right}", right)
                    self.assertEqual(f"{left} ⊣ {right}", left)

class TestLess(APLTestCase):
    """Test the primitive function <."""

    def test(self):
        self.assertEqual("5 < ¯3 0 1 5 10", "0 0 0 0 1")
        self.assertEqual("¯2.3 < ¯3 0 1 5 10", "0 1 1 1 1")

class TestLessEq(APLTestCase):
    """Test the primitive function ≤."""

    def test(self):
        self.assertEqual("5 ≤ ¯3 0 1 5 10", "0 0 0 1 1")
        self.assertEqual("¯2.3 ≤ ¯3 0 1 5 10", "0 1 1 1 1")

class TestEq(APLTestCase):
    """Test the primitive function =."""

    def test(self):
        self.assertEqual(
            "5 ¯2.3 3.5J¯2 = (5 ¯2.3 3.5J¯2) (5 ¯2.3 3.5J¯2) (5 ¯2.3 3.5J¯2)",
            "(1 0 0) (0 1 0) (0 0 1)"
        )

class TestGreaterEq(APLTestCase):
    """Test the primitive function ≥."""

    def test(self):
        self.assertEqual("5 ≥ ¯3 0 1 5 10", "1 1 1 1 0")
        self.assertEqual("¯2.3 ≥ ¯3 0 1 5 10", "1 0 0 0 0")

class TestGreater(APLTestCase):
    """Test the primitive function >."""

    def test(self):
        self.assertEqual("5 > ¯3 0 1 5 10", "1 1 1 0 0")
        self.assertEqual("¯2.3 > ¯3 0 1 5 10", "1 0 0 0 0")

class TestNeq(APLTestCase):
    """Test the primitive function ≠."""

    def test_unique_mask(self):
        self.assertEqual("≠1 2 3 4", "1 1 1 1")
        self.assertEqual("≠1 1 1 1", "1 0 0 0")
        self.assertEqual("≠1 2 3 1 2 4", "1 1 1 0 0 1")
        self.assertEqual("≠(0 0) (1 0) (0 1) 1 0", "1 1 1 1 1")
        self.assertEqual("≠1 (1 1) (1 1 1) (1 1 1 1) (1 1)", "1 1 1 1 0")
        self.assertEqual("≠0J1 0J¯1", "1 1")

    def test_neq(self):
        self.assertEqual(
            "5 ¯2.3 3.5J¯2 ≠ (5 ¯2.3 3.5J¯2) (5 ¯2.3 3.5J¯2) (5 ¯2.3 3.5J¯2)",
            "(0 1 1) (1 0 1) (1 1 0)"
        )

class TestLShoe(APLTestCase):
    """Test the primitive function ⊂."""

    def test_enclose(self):
        self.assertEqual("⊂1", "1")
        self.assertEqual("⊂⊂3J1", "3J1")
        self.assertEqual("⊂⊂⊂⊂⊂¯3.4", "¯3.4")
        # Now when enclosing actually matters.
        arr_str = "1 3J1 (5 8)"
        arr = run(arr_str)
        for _ in range(5):
            arr = S(arr)
            arr_str = "⊂" + arr_str
            self.assertEqual(arr_str, arr)

    def test_partitioned_enclose(self):
        pass

class TestWithout(APLTestCase):
    """Test the primitive function ~."""

    def test_not(self):
        self.assertEqual("~1 0 0 1", "0 1 1 0")
        self.assertEqual("~1.0 0.0 1J0 0.0J0", "0 1 0 1")

    def test_without(self):
        self.assertEqual("1 2 3 4.5 ~ 2 4.5", "1 3")
        self.assertEqual("1 2 3 1 2 3 0J1 0J1 1.0 4.5 ~ 1 2 3", "0J1 0J1 4.5")

class TestIota(APLTestCase):
    """Test the primitive function ⍳."""

    def test_index_generator(self):
        self.assertEqual("⍳2", "0 1")
        self.assertEqual("⍳6", "0 1 2 3 4 5")

    def test_index_of(self):
        pass

class Rho(APLTestCase):
    """Test the primitive function ⍴."""

    def test_shape(self):
        self.assertEqual("⍴1 2 3 4", APLArray([1], [S(4)]))
        self.assertEqual("⍴0J1", APLArray([0], []))
        self.assertEqual("⍴(0 1 3) (4 5 6) (1 (3 ¯3))", APLArray([1], [S(3)]))

    def test_reshape(self):
        self.assertEqual("0⍴1 2 3", APLArray([0], []))
        self.assertEqual("1⍴1", APLArray([1], [S(1)]))
        self.assertEqual(
            "1⍴(1 2 3)(4 5 6)",
            APLArray([1], [APLArray([3], [S(1), S(2), S(3)])])
        )
        self.assertEqual("5⍴1 2 3", "1 2 3 1 2")
        self.assertEqual("1 1⍴0J1", APLArray([1,1], [S(1j)]))

    def test_shape_of_reshape(self):
        datas = [
            "0",
            "0J¯1",
            "1 ¯2 3.5 0J4",
            "(1 2 3) 4 (5 (6 7 8))",
        ]
        shapes = [
            "3 4",
            "4 3",
            "1 1 1",
            "2 3 4",
            "0 0 0",
            "0 0 1",
            "0 1 0",
            "0 1 1",
            "1 0 0",
            "1 0 1",
            "1 1 1",
        ]
        for data in datas:
            for shape in shapes:
                with self.subTest(data=data, shape=shape):
                    self.assertEqual(f"⍴{shape}⍴{data}", shape)
