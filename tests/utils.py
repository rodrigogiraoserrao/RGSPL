"""
Utility functions used by the tests.
"""

from rgspl import Interpreter, Parser, Tokenizer
from arraymodel import APLArray

def run(code):
    """Run a string containing APL code."""
    return Interpreter(Parser(Tokenizer(code))).interpret()

def S(scalar):
    """Create an APL scalar."""
    return APLArray([], scalar)
