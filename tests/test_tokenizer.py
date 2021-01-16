"""
Test the RGSPL Tokenizer.
"""

import unittest

from rgspl import Parser, Tokenizer, Token
from arraymodel import APLArray

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

    def test_numeric_promotion(self):
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

    def test_ids(self):
        """Test id tokenization."""

        ID = lambda v: [self.eof, Token(Token.ID, v)]
        self.assertEqual(self.tok("bananas"), ID("bananas"))
        self.assertEqual(self.tok("abcd"), ID("abcd"))
        self.assertEqual(self.tok("CamelCase"), ID("CamelCase"))
        self.assertEqual(self.tok("pascalCase"), ID("pascalCase"))
        self.assertEqual(self.tok("using_Some_Underscores"), ID("using_Some_Underscores"))
        self.assertEqual(self.tok("_"), ID("_"))
        self.assertEqual(self.tok("__"), ID("__"))
        self.assertEqual(self.tok("_varname"), ID("_varname"))
        self.assertEqual(self.tok("var123"), ID("var123"))
        self.assertEqual(self.tok("var123_2"), ID("var123_2"))
        self.assertEqual(self.tok("_J3"), ID("_J3"))
        self.assertEqual(self.tok("_1J2"), ID("_1J2"))
        self.assertEqual(self.tok("J2"), ID("J2"))

    def test_comment_skipping(self):
        """Test if comments are skipped."""

        self.assertEqual(self.tok("⍝ this is a comment"), [self.eof])
        self.assertEqual(self.tok("⍝3J5 ¯3"), [self.eof])
        self.assertEqual(self.tok("⍝⍝⍝ triple comment"), [self.eof])
        self.assertEqual(self.tok("¯2 ⍝ neg 2"), [self.eof, Token(Token.INTEGER, -2)])
        self.assertEqual(self.tok("var ⍝ some var"), [self.eof, Token(Token.ID, "var")])

    def test_wysiwyg_tokens(self):
        """Test if WYSIWYG tokens are tokenized correctly."""

        for s, type_ in Token.WYSIWYG_MAPPING.items():
            for s2, type_2 in Token.WYSIWYG_MAPPING.items():
                code = s+s2
                toks = [self.eof, Token(type_, s), Token(type_2, s2)]
                with self.subTest(code=code):
                    self.assertEqual(self.tok(code), toks)
                code = s+" "+s2
                with self.subTest(code=code):
                    self.assertEqual(self.tok(code), toks)
