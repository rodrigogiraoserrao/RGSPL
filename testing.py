"""
Tests the current subset of APL implemented.
"""

from rgspl import Interpreter, Parser, Tokenizer

run = lambda code: Interpreter(Parser(Tokenizer(code))).interpret()

def raw_test(code, raw):
    """Test if the given code gives the expected raw result."""
    assert run(code) == raw

def test(code, expected):
    """Test if the given code is interpreted to the expected result."""
    assert run(code) == run(expected)

# Test simple scalars on their own.
raw_test("5", 5)
raw_test("¯2", -2)
raw_test("123456", 123456)
raw_test("5.6", 5.6)
raw_test("1.0", 1)
raw_test("¯05.06", -5.06)
raw_test("¯000.001", -0.001)
raw_test("0J1", complex(0, 1))
raw_test("56J0.002", complex(56, 0.002))
raw_test("102.5J1", complex(102.5, 1))
raw_test("1J0", 1)
raw_test("¯3.7J0.0", -3.7)

# Test redundant parenthesis
raw_test("(0.2)", 0.2)
raw_test("((5))", 5)
raw_test("(((¯3)))", -3)
