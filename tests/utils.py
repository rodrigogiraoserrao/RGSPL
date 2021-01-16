"""
Utility functions used by the tests.
"""

import functools
import unittest

from rgspl import Interpreter, Parser, Tokenizer
from arraymodel import APLArray

def run(code):
    """Run a string containing APL code."""
    return Interpreter(Parser(Tokenizer(code))).interpret()

def S(scalar):
    """Create an APL scalar."""
    return APLArray([], scalar)

def run_apl_code_decorator(assert_method):
    """Create a new assert method interpreting positional strings as APL code."""

    @functools.wraps(assert_method)
    def new_assert_method(*args, **kwargs):
        i = 0
        args = list(args) # to allow in-place modification.
        # Run, as APL code, the first consecutive strings in the positional arguments.
        while i < len(args) and isinstance(args[i], str):
            args[i] = run(args[i])
            i += 1
        return assert_method(*args, **kwargs)
    return new_assert_method

class APLTestCase(unittest.TestCase):
    """The assert methods preprocess the arguments by running the APL code.
    
    A test case class that overrides some assert methods that start by running
    the APL code in the arguments and only then applying the assertions over them.
    """

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        # Traverse all the methods of the unittest.TestCase, looking for assertX
        # methods and decorating them accordingly.
        for method_name in dir(self):
            if method_name.startswith("assert") and not method_name.endswith("_"):
                decorated = run_apl_code_decorator(getattr(self, method_name))
                setattr(self, method_name, decorated)
