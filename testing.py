"""
Tests the current subset of APL implemented.
"""

import unittest

from rgspl import Interpreter, Parser, Tokenizer, Token
from arraymodel import APLArray

run = lambda code: Interpreter(Parser(Tokenizer(code))).interpret()

def S(scalar):
    return APLArray([], scalar)

class TestTokenizer(unittest.TestCase):
    """Test the tokenizer."""

    tok = lambda _, s: Tokenizer(s).tokenize()
    eof = Token(Token.EOF, None)

    def test_integers(self):
        """Test integer tokenization."""

        for n in range(30):
            self.assertEqual(self.tok(str(n)), [self.eof, Token(Token.INTEGER, n)])
            self.assertEqual(self.tok(f"¯{n}"), [self.eof, Token(Token.INTEGER, -n)])

    def test_floats(self):
        """Test float tokenization."""

        self.assertEqual(self.tok("0.5"), [self.eof, Token(Token.FLOAT, 0.5)])
        self.assertEqual(self.tok("¯0.25"), [self.eof, Token(Token.FLOAT, -0.25)])
        self.assertEqual(self.tok(".125"), [self.eof, Token(Token.FLOAT, 0.125)])
        self.assertEqual(self.tok("¯.0625"), [self.eof, Token(Token.FLOAT, -0.0625)])

    def test_complex_nums(self):
        """Test complex number tokenization."""

        T = Token
        C = lambda c: [self.eof, T(T.COMPLEX, c)]
        realss = ["0", "2", "¯3", "0.5", "¯0.25", ".125", "¯.5"]
        realsv = [0, 2, -3, 0.5, -0.25, 0.125, -0.5]
        compss = ["1", "¯4", "0.1", "¯0.01", ".2", "¯.8"]
        compsv = [1, -4, 0.1, -0.01, 0.2, -0.8]
        for rs, rv in zip(realss, realsv):
            for cs, cv in zip(compss, compsv):
                c = complex(rv, cv)
                with self.subTest(c=c):
                    self.assertEqual(self.tok(f"{rs}J{cs}"), C(c))

    def test_numeric_upgrades(self):
        """Ensure empty imaginary parts and empty decimals get promoted."""

        f = lambda t: lambda v: [self.eof, Token(t, v)]
        I = f(Token.INTEGER)
        F = f(Token.FLOAT)

        self.assertEqual(self.tok("1."), I(1))
        self.assertEqual(self.tok("56.0"), I(56))
        self.assertEqual(self.tok("¯987."), I(-987))
        self.assertEqual(self.tok("¯23.0"), I(-23))

        self.assertEqual(self.tok("1J0"), I(1))
        self.assertEqual(self.tok("2J¯0"), I(2))
        self.assertEqual(self.tok("1.2J0"), F(1.2))
        self.assertEqual(self.tok("¯0.5J0"), F(-0.5))

        self.assertEqual(self.tok("1.0J0."), I(1))
        self.assertEqual(self.tok("¯8.J0.0"), I(-8))
        self.assertEqual(self.tok(".125J0.0"), F(0.125))
        self.assertEqual(self.tok("¯.25J0."), F(-0.25))

class TestScalarParsing(unittest.TestCase):
    """Test that scalars are parsed conveniently."""

    def test_nonneg_integers(self):
        self.assertEqual(run("0"), S(0))
        self.assertEqual(run("1"), S(1))
        self.assertEqual(run("2"), S(2))
        self.assertEqual(run("123456789987654321"), S(123456789987654321))

    def test_negative_integers(self):
        self.assertEqual(run("¯1"), S(-1))
        self.assertEqual(run("¯2"), S(-2))
        self.assertEqual(run("¯0"), S(0))
        self.assertEqual(run("¯973"), S(-973))

if __name__ == "__main__":
    unittest.main()

def raw_data_test(code, raw):
    """Test if the given code gives the expected raw result."""
    assert run(code) == raw

def test(code, expected):
    """Test if the given code is interpreted to the expected result."""
    assert run(code) == run(expected)

# Test simple scalars on their own.
raw_data_test("5", S(5))
raw_data_test("¯2", S(-2))
raw_data_test("123456", S(123456))
raw_data_test("5.6", S(5.6))
raw_data_test("1.0", S(1))
raw_data_test("¯05.06", S(-5.06))
raw_data_test("¯000.001", S(-0.001))
raw_data_test("0J1", S(complex(0, 1)))
raw_data_test("56J0.002", S(complex(56, 0.002)))
raw_data_test("102.5J1", S(complex(102.5, 1)))
raw_data_test("1J0", S(1))
raw_data_test("¯3.7J0.0", S(-3.7))

# Test simple vectors on their own.
raw_data_test("1 2 3 4", APLArray([4], [S(1), S(2), S(3), S(4)]))
raw_data_test("¯1 1 ¯1 1", APLArray([4], [S(-1), S(1), S(-1), S(1)]))
raw_data_test("(2.3 5.6 7.8 9)", APLArray([4], [S(2.3), S(5.6), S(7.8), S(9)]))

# Test redundant parenthesis
raw_data_test("(0.2)", S(0.2))
raw_data_test("((5))", S(5))
raw_data_test("(((¯3)))", S(-3))

# Test nested vectors
raw_data_test(
    "1 2 3 (4 5) (6 7)",
    APLArray([5], [S(1), S(2), S(3), APLArray([2], [S(4), S(5)]), APLArray([2], [S(6), S(7)])])
)
raw_data_test(
    "1 (2 (3 (4 5)))",
    APLArray([2], [S(1), APLArray([2], [S(2), APLArray([2], [S(3), APLArray([2], [S(4), S(5)])])])])
)
raw_data_test(
    "(((1 2) 3) 4) 5",
    APLArray([2], [APLArray([2], [APLArray([2], [APLArray([2], [S(1), S(2)]), S(3)]), S(4)]), S(5)])
)

# Test nesting of scalars
test("⊂1", "1")
test("⊂⊂1", "1")
test("⊂⊂⊂¯3.5", "¯3.5")
