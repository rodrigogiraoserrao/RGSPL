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

class TestRho(APLTestCase):
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

class TestAnd(APLTestCase):
    """Test the primitive function ∧."""

    def test_and(self):
        self.assertEqual("0 ∧ 0", "0")
        self.assertEqual("0 ∧ 1", "0")
        self.assertEqual("1 ∧ 0", "0")
        self.assertEqual("1 ∧ 1", "1")
        self.assertEqual("0 ∧ 0 1", "0 0")
        self.assertEqual("1 ∧ 0 1", "0 1")
        self.assertEqual("0 1 ∧ 0", "0 0")
        self.assertEqual("0 1 ∧ 1", "0 1")
        self.assertEqual("0 0 1 1 ∧ 0 1 0 1", "0 0 0 1")

    def test_lcm(self):
        pass

class TestOr(APLTestCase):
    """Test the primitive function ∨."""

    def test_or(self):
        self.assertEqual("0 ∨ 0", "0")
        self.assertEqual("0 ∨ 1", "1")
        self.assertEqual("1 ∨ 0", "1")
        self.assertEqual("1 ∨ 1", "1")
        self.assertEqual("0 ∨ 0 1", "0 1")
        self.assertEqual("1 ∨ 0 1", "1 1")
        self.assertEqual("0 1 ∨ 0", "0 1")
        self.assertEqual("0 1 ∨ 1", "1 1")
        self.assertEqual("0 0 1 1 ∨ 0 1 0 1", "0 1 1 1")

    def test_gcd(self):
        pass

class TestNotAnd(APLTestCase):
    """Test the primitive function ⍲."""

    def test_not_and(self):
        self.assertEqual("0 ⍲ 0", "1")
        self.assertEqual("0 ⍲ 1", "1")
        self.assertEqual("1 ⍲ 0", "1")
        self.assertEqual("1 ⍲ 1", "0")
        self.assertEqual("0 ⍲ 0 1", "1 1")
        self.assertEqual("1 ⍲ 0 1", "1 0")
        self.assertEqual("0 1 ⍲ 0", "1 1")
        self.assertEqual("0 1 ⍲ 1", "1 0")
        self.assertEqual("0 0 1 1 ⍲ 0 1 0 1", "1 1 1 0")

class TestNotOr(APLTestCase):
    """Test the primitive function ⍱."""

    def test_not_or(self):
        self.assertEqual("0 ⍱ 0", "1")
        self.assertEqual("0 ⍱ 1", "0")
        self.assertEqual("1 ⍱ 0", "0")
        self.assertEqual("1 ⍱ 1", "0")
        self.assertEqual("0 ⍱ 0 1", "1 0")
        self.assertEqual("1 ⍱ 0 1", "0 0")
        self.assertEqual("0 1 ⍱ 0", "1 0")
        self.assertEqual("0 1 ⍱ 1", "0 0")
        self.assertEqual("0 0 1 1 ⍱ 0 1 0 1", "1 0 0 0")

class TestDecode(APLTestCase):
    """Test the primitive function ⊥."""

    def test_decode(self):
        self.assertEqual("0 ⊥ 3", "3")
        self.assertEqual("10000 ⊥ 4", "4")
        self.assertEqual("42 ⊥ 5", "5")
        self.assertEqual("5 ⊥ 6", "6")
        self.assertEqual("¯10 ⊥ 7", "7")
        self.assertEqual("2 ⊥ 1 0 1", "5")
        self.assertEqual("2 2 2 ⊥ 1 0 1", "5")
        self.assertEqual("2 3 2 ⊥ 1 0 1", "7")
        self.assertEqual("5 3 2 ⊥ 1 0 1", "7")
        self.assertEqual("1 0 1 ⊥ 2", "4")

    def test_high_rank(self):
        self.assertEqual(
            "(3 2⍴8 8 0 8 6 3) ⊥ 2 4⍴2 9 3 1 0 3 8 0",
            "3 4⍴16 75 32 8 16 75 32 8 6 30 17 3"
        )
        self.assertEqual(
            "(3 4 2⍴3 5 6 9 9 1 4 7 7 4 10 8 1 4 9 9 1 6 5 8 6 7 8 6) ⊥ 2 5 4⍴9 7 1 3 10 6 2 3 4 10 8 4 1 9 3 1 3 3 10 8 3 1 9 5 10 3 3 9 9 1 2 10 10 8 6 8 7 6 9 8",
            "3 4 5 4⍴48 36 14 20 60 33 13 24 29 51 42 30 15 53 21 13 22 21 59 48 84 64 18 32 100 57 21 36 45 91 74 46 19 89 33 17 34 33 99 80 12 8 10 8 20 9 5 12 13 11 10 14 11 17 9 9 10 9 19 16 66 50 16 26 80 45 17 30 37 71 58 38 17 71 27 15 28 27 79 64 39 29 13 17 50 27 11 21 25 41 34 26 14 44 18 12 19 18 49 40 75 57 17 29 90 51 19 33 41 81 66 42 18 80 30 16 31 30 89 72 39 29 13 17 50 27 11 21 25 41 34 26 14 44 18 12 19 18 49 40 84 64 18 32 100 57 21 36 45 91 74 46 19 89 33 17 34 33 99 80 57 43 15 23 70 39 15 27 33 61 50 34 16 62 24 14 25 24 69 56 75 57 17 29 90 51 19 33 41 81 66 42 18 80 30 16 31 30 89 72 66 50 16 26 80 45 17 30 37 71 58 38 17 71 27 15 28 27 79 64 57 43 15 23 70 39 15 27 33 61 50 34 16 62 24 14 25 24 69 56"
        )
        self.assertEqual(
            "(3 4 2⍴7 8 9 3 1 9 0 0 2 3 4 9 1 8 9 0 4 7 4 8 8 5 4 1) ⊥ 2 5 4⍴2 9 4 0 2 5 5 7 2 5 0 9 5 2 9 4 1 0 4 3 1 8 0 7 2 6 8 4 4 6 6 7 0 2 2 2 1 4 7 0",
            "3 4 5 4⍴17 80 32 7 18 46 48 60 20 46 6 79 40 18 74 34 9 4 39 24 7 35 12 7 8 21 23 25 10 21 6 34 15 8 29 14 4 4 19 9 19 89 36 7 20 51 53 67 22 51 6 88 45 20 83 38 10 4 43 27 1 8 0 7 2 6 8 4 4 6 6 7 0 2 2 2 1 4 7 0 7 35 12 7 8 21 23 25 10 21 6 34 15 8 29 14 4 4 19 9 19 89 36 7 20 51 53 67 22 51 6 88 45 20 83 38 10 4 43 27 17 80 32 7 18 46 48 60 20 46 6 79 40 18 74 34 9 4 39 24 1 8 0 7 2 6 8 4 4 6 6 7 0 2 2 2 1 4 7 0 15 71 28 7 16 41 43 53 18 41 6 70 35 16 65 30 8 4 35 21 17 80 32 7 18 46 48 60 20 46 6 79 40 18 74 34 9 4 39 24 11 53 20 7 12 31 33 39 14 31 6 52 25 12 47 22 6 4 27 15 3 17 4 7 4 11 13 11 6 11 6 16 5 4 11 6 2 4 11 3"
        )

class TestEncode(APLTestCase):
    """Test the primitive function ⊤."""

    def test_encode(self):
        self.assertEqual("4 ⊤ 2", "2")
        self.assertEqual("4 ⊤ 4", "0")
        self.assertEqual("4 ⊤ 6", "2")
        self.assertEqual("2 2 2 2 ⊤ 5", "0 1 0 1")
        self.assertEqual("2 2 2 2 ⊤ 5 7 12", "4 3⍴0 0 1 1 1 1 0 1 0 1 1 0")

    def test_high_rank(self):
        self.assertEqual(
            "(2 2⍴1 2 3 4) ⊤ 3 3⍴1 2 3 4 5 6 7 8 9",
            "2 2 3 3⍴0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 1 2 0 1 2 0 1 2 0 1 2 3 0 1 2 3 0 1"
        )
        self.assertEqual(
            "(2 3⍴3 0 0 6 8 2) ⊤ 4 2⍴6 5 3 5 0 6 3 5",
            "2 3 4 2⍴1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 3 2 1 2 0 3 1 2 0 5 3 5 0 0 3 5 6 5 3 5 0 6 3 5 0 1 1 1 0 0 1 1"
        )
