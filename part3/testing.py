"""
Tests the current subset of APL implemented.
"""

from rgspl import Interpreter, Parser, Tokenizer
from arraymodel import APLArray

run = lambda code: Interpreter(Parser(Tokenizer(code))).interpret()

def S(scalar):
    return APLArray([], scalar)

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
