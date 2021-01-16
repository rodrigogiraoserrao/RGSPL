"""
Implement a subset of the APL programming language.

Supports the monadic/dyadic functions +-×÷⌈⌊⊢⊣⍳<≤=≥>≠~⊂ ;
Supports (negative) integers/floats/complex numbers and vectors of those ;
Supports the monadic operators ⍨ and ¨ ;
Supports the dyadic operators ∘ (only functions as operands) and ⍥ ;
Supports parenthesized expressions ;
Supports multiple expressions separated by ⋄ ;
Supports comments with ⍝ ;

This is the grammar supported:

    program        ::= EOF statement_list
    statement_list ::= (statement "⋄")* statement
    statement      ::= ( ID "←" | vector function | function )* vector
    function       ::= function mop | function dop f | f
    dop            ::= "∘" | "⍥"
    mop            ::= "⍨" | "¨"
    f              ::= "+" | "-" | "×" | "÷" | "⌈" | "⌊" |
                     | "⊢" | "⊣" | "⍳" | "<" | "≤" | "=" |
                     | "≥" | ">" | "≠" | "~" | "⊂" | "⍴" | LPARENS function RPARENS
    vector         ::= vector* ( scalar | ( LPARENS statement RPARENS ) )
    scalar         ::= INTEGER | FLOAT | COMPLEX | ID
"""
# pylint: disable=invalid-name

import argparse
from typing import List

import doperators
import functions
import moperators
from arraymodel import APLArray

class Token:
    """Represents a token parsed from the source code."""

    # "Data types"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    COMPLEX = "COMPLEX"
    ID = "ID"
    # Functions
    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    DIVIDE = "DIVIDE"
    CEILING = "CEILING"
    FLOOR = "FLOOR"
    RIGHT_TACK = "RIGHT_TACK"
    LEFT_TACK = "LEFT_TACK"
    IOTA = "IOTA"
    LESS = "LESS"
    LESSEQ = "LESSEQ"
    EQ = "EQ"
    GREATEREQ = "GREATEREQ"
    GREATER = "GREATER"
    NEQ = "NEQ"
    WITHOUT = "WITHOUT"
    LSHOE = "LSHOE"
    RHO = "RHO"
    # Operators
    COMMUTE = "COMMUTE"
    DIAERESIS = "DIAERESIS"
    JOT = "JOT"
    OVER = "OVER"
    # Misc
    DIAMOND = "DIAMOND"
    NEGATE = "NEGATE"
    ASSIGNMENT = "ASSIGNMENT"
    LPARENS = "LPARENS"
    RPARENS = "RPARENS"
    EOF = "EOF"

    # Helpful lists of token types.
    FUNCTIONS = [
        PLUS, MINUS, TIMES, DIVIDE, FLOOR, CEILING, RIGHT_TACK, LEFT_TACK, IOTA,
        LESS, LESSEQ, EQ, GREATEREQ, GREATER, NEQ, WITHOUT, LSHOE, RHO,
    ]
    MONADIC_OPS = [COMMUTE, DIAERESIS]
    DYADIC_OPS = [JOT, OVER]

    # What You See Is What You Get characters that correspond to tokens.
    # The mapping from characteres to token types.
    WYSIWYG_MAPPING = {
        "+": PLUS,
        "-": MINUS,
        "×": TIMES,
        "÷": DIVIDE,
        "⌈": CEILING,
        "⌊": FLOOR,
        "⊢": RIGHT_TACK,
        "⊣": LEFT_TACK,
        "⍳": IOTA,
        "<": LESS,
        "≤": LESSEQ,
        "=": EQ,
        "≥": GREATEREQ,
        ">": GREATER,
        "≠": NEQ,
        "~": WITHOUT,
        "⊂": LSHOE,
        "⍴": RHO,
        "⍨": COMMUTE,
        "¨": DIAERESIS,
        "∘": JOT,
        "⍥": OVER,
        "←": ASSIGNMENT,
        "(": LPARENS,
        ")": RPARENS,
        "⋄": DIAMOND,
        "\n": DIAMOND,
    }

    ID_CHARS = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            isinstance(other, Token)
            and (self.type, self.value) == (other.type, other.value)
        )


class Tokenizer:
    """Class that tokenizes source code into tokens."""

    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.current_char = self.code[self.pos]

    def error(self, message):
        """Raises a Tokenizer error."""
        raise Exception(f"TokenizerError: {message}")

    def advance(self):
        """Advances the cursor position and sets the current character."""

        self.pos += 1
        self.current_char = None if self.pos >= len(self.code) else self.code[self.pos]

    def skip_whitespace(self):
        """Skips all the whitespace in the source code."""

        while self.current_char and self.current_char in " \t":
            self.advance()

    def skip_comment(self):
        """Skips commented code."""

        if not self.current_char == "⍝":
            return
        while self.current_char and self.current_char != "\n":
            self.advance()

    def get_integer(self):
        """Parses an integer from the source code."""

        start_idx = self.pos
        while self.current_char and self.current_char.isdigit():
            self.advance()
        return self.code[start_idx:self.pos] or "0"

    def get_real_number(self):
        """Parses a real number from the source code."""

        # Check for a negation of the number.
        if self.current_char == "¯":
            self.advance()
            int_ = "-" + self.get_integer()
        else:
            int_ = self.get_integer()
        # Check if we have a decimal number here.
        if self.current_char == ".":
            self.advance()
            dec_ = self.get_integer()
        else:
            dec_ = "0"

        if int(dec_):
            return float(f"{int_}.{dec_}")
        else:
            return int(int_)

    def get_number_token(self):
        """Parses a number token from the source code."""

        real = self.get_real_number()
        if self.current_char == "J":
            self.advance()
            im = self.get_real_number()
        else:
            im = 0

        if im:
            tok = Token(Token.COMPLEX, complex(real, im))
        elif isinstance(real, int):
            tok = Token(Token.INTEGER, real)
        elif isinstance(real, float):
            tok = Token(Token.FLOAT, real)
        else:
            self.error("Cannot recognize type of number.")
        return tok

    def get_id_token(self):
        """Retrieves an identifier token."""

        start = self.pos
        while self.current_char and self.current_char in Token.ID_CHARS:
            self.advance()
        return Token(Token.ID, self.code[start:self.pos])

    def get_wysiwyg_token(self):
        """Retrieves a WYSIWYG token."""

        char = self.current_char
        self.advance()
        try:
            return Token(Token.WYSIWYG_MAPPING[char], char)
        except KeyError:
            self.error("Could not parse WYSIWYG token.")

    def get_next_token(self):
        """Finds the next token in the source code."""

        self.skip_whitespace()
        self.skip_comment()
        if not self.current_char:
            return Token(Token.EOF, None)

        if self.current_char in "¯.0123456789":
            return self.get_number_token()

        if self.current_char in Token.ID_CHARS:
            return self.get_id_token()

        if self.current_char in Token.WYSIWYG_MAPPING:
            return self.get_wysiwyg_token()

        self.error("Could not parse the next token...")

    def tokenize(self):
        """Returns the whole token list."""

        tokens = [self.get_next_token()]
        while tokens[-1].type != Token.EOF:
            tokens.append(self.get_next_token())
        # Move the EOF token to the beginning of the list.
        return [tokens[-1]] + tokens[:-1]


class ASTNode:
    """Stub class to be inherited by the different types of AST nodes.

    The AST Nodes are used by the Parser instances to build an
        Abstract Syntax Tree out of the APL programs.
    These ASTs can then be traversed to interpret an APL program.
    """

    def __repr__(self):
        return self.__str__()


class S(ASTNode):
    """Node for a simple scalar like 3 or ¯4.2"""
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return f"S({self.value})"


class V(ASTNode):
    """Node for a stranded vector of simple scalars, like 3 ¯4 5.6"""
    def __init__(self, children: List[ASTNode]):
        self.children = children

    def __str__(self):
        return f"V({self.children})"


class MOp(ASTNode):
    """Node for monadic operators like ⍨"""
    def __init__(self, token: Token, child: ASTNode):
        self.token = token
        self.operator = self.token.value
        self.child = child

    def __str__(self):
        return f"MOp({self.operator} {self.child})"


class DOp(ASTNode):
    """Node for dyadic operators like ∘"""
    def __init__(self, token: Token, left: ASTNode, right: ASTNode):
        self.token = token
        self.operator = self.token.value
        self.left = left
        self.right = right

    def __str__(self):
        return f"DOP({self.left} {self.operator} {self.right})"


class F(ASTNode):
    """Node for built-in functions like + or ⌈"""
    def __init__(self, token: Token):
        self.token = token
        self.function = self.token.value

    def __str__(self):
        return f"F({self.function})"


class Monad(ASTNode):
    """Node for monadic function calls."""
    def __init__(self, function: ASTNode, omega: ASTNode):
        self.function = function
        self.omega = omega

    def __str__(self):
        return f"Monad({self.function} {self.omega})"


class Dyad(ASTNode):
    """Node for dyadic functions."""
    def __init__(self, function: ASTNode, alpha: ASTNode, omega: ASTNode):
        self.function = function
        self.alpha = alpha
        self.omega = omega

    def __str__(self):
        return f"Dyad({self.function} {self.alpha} {self.omega})"


class Assignment(ASTNode):
    """Node for assignment expressions."""
    def __init__(self, varname: ASTNode, value: ASTNode):
        self.varname = varname
        self.value = value

    def __str__(self):
        return f"Assignment({self.varname.token.value} ← {self.value})"


class Var(ASTNode):
    """Node for variable references."""
    def __init__(self, token: Token):
        self.token = token
        self.name = self.token.value

    def __str__(self):
        return f"Var({self.token.value})"


class Statements(ASTNode):
    """Node to represent a series of consecutive statements."""
    def __init__(self):
        self.children = []

    def __str__(self):
        return str(self.children)


class Parser:
    """Implements a parser for a subset of the APL language.

    The grammar parsed is available at the module-level docstring.
    """

    def __init__(self, tokenizer, debug=False):
        self.tokens = tokenizer.tokenize()
        self.pos = len(self.tokens) - 1
        self.token_at = self.tokens[self.pos]
        self.debug_on = debug

    def debug(self, message):
        """If the debugging option is on, print a message."""
        if self.debug_on:
            print(f"PD @ {message}")

    def error(self, message):
        """Throws a Parser-specific error message."""
        raise Exception(f"Parser: {message}")

    def eat(self, token_type):
        """Checks if the current token matches the expected token type."""

        if self.token_at.type != token_type:
            self.error(f"Expected {token_type} and got {self.token_at.type}.")
        else:
            self.pos -= 1
            self.token_at = None if self.pos < 0 else self.tokens[self.pos]

    def peek(self):
        """Returns the next token type without consuming it."""
        peek_at = self.pos - 1
        return None if peek_at < 0 else self.tokens[peek_at].type

    def peek_beyond_parens(self):
        """Returns the next token type that is not a right parenthesis."""
        peek_at = self.pos - 1
        while peek_at >= 0 and self.tokens[peek_at].type == Token.RPARENS:
            peek_at -= 1
        return None if peek_at < 0 else self.tokens[peek_at].type

    def parse_program(self):
        """Parses a full program."""

        self.debug(f"Parsing program from {self.tokens}")
        statement_list = self.parse_statement_list()
        self.eat(Token.EOF)
        return statement_list

    def parse_statement_list(self):
        """Parses a list of statements."""

        self.debug(f"Parsing a statement list from {self.tokens}")
        root = Statements()
        statements = [self.parse_statement()]
        while self.token_at.type == Token.DIAMOND:
            self.eat(Token.DIAMOND)
            statements.append(self.parse_statement())

        root.children = statements
        return root

    def parse_statement(self):
        """Parses a statement."""

        self.debug(f"Parsing statement from {self.tokens[:self.pos+1]}")

        relevant_types = [Token.ASSIGNMENT, Token.RPARENS] + Token.FUNCTIONS + Token.MONADIC_OPS
        statement = self.parse_vector()
        while self.token_at.type in relevant_types:
            if self.token_at.type == Token.ASSIGNMENT:
                self.eat(Token.ASSIGNMENT)
                statement = Assignment(Var(self.token_at), statement)
                self.eat(Token.ID)
            else:
                function = self.parse_function()
                if self.token_at.type in [Token.RPARENS, Token.INTEGER, Token.FLOAT, Token.COMPLEX, Token.ID]:
                    array = self.parse_vector()
                    statement = Dyad(function, array, statement)
                else:
                    statement = Monad(function, statement)

        return statement

    def parse_vector(self):
        """Parses a vector composed of possibly several simple scalars."""

        self.debug(f"Parsing vector from {self.tokens[:self.pos+1]}")

        nodes = []
        array_tokens = [Token.INTEGER, Token.FLOAT, Token.COMPLEX, Token.ID]
        while self.token_at.type in array_tokens + [Token.RPARENS]:
            if self.token_at.type == Token.RPARENS:
                if self.peek_beyond_parens() in array_tokens:
                    self.eat(Token.RPARENS)
                    nodes.append(self.parse_statement())
                    self.eat(Token.LPARENS)
                else:
                    break
            else:
                nodes.append(self.parse_scalar())
        nodes = nodes[::-1]
        if not nodes:
            self.error("Failed to parse scalars inside a vector.")
        elif len(nodes) == 1:
            node = nodes[0]
        else:
            node = V(nodes)
        return node

    def parse_scalar(self):
        """Parses a simple scalar."""

        self.debug(f"Parsing scalar from {self.tokens[:self.pos+1]}")

        if self.token_at.type == Token.ID:
            scalar = Var(self.token_at)
            self.eat(Token.ID)
        elif self.token_at.type == Token.INTEGER:
            scalar = S(self.token_at)
            self.eat(Token.INTEGER)
        elif self.token_at.type == Token.FLOAT:
            scalar = S(self.token_at)
            self.eat(Token.FLOAT)
        else:
            scalar = S(self.token_at)
            self.eat(Token.COMPLEX)

        return scalar

    def parse_function(self):
        """Parses a (derived) function."""

        self.debug(f"Parsing function from {self.tokens[:self.pos+1]}")

        if self.token_at.type in Token.MONADIC_OPS:
            function = self.parse_mop()
            function.child = self.parse_function()
        else:
            function = self.parse_f()
            if self.token_at.type in Token.DYADIC_OPS:
                dop = DOp(self.token_at, None, function)
                self.eat(dop.token.type)
                dop.left = self.parse_function()
                function = dop
        return function

    def parse_mop(self):
        """Parses a monadic operator."""

        self.debug(f"Parsing a mop from {self.tokens[:self.pos+1]}")

        mop = MOp(self.token_at, None)
        if (t := self.token_at.type) not in Token.MONADIC_OPS:
            self.error(f"{t} is not a valid monadic operator.")
        self.eat(t)

        return mop

    def parse_f(self):
        """Parses a simple one-character function."""

        self.debug(f"Parsing f from {self.tokens[:self.pos+1]}")

        if (t := self.token_at.type) in Token.FUNCTIONS:
            f = F(self.token_at)
            self.eat(t)
        else:
            self.eat(Token.RPARENS)
            f = self.parse_function()
            self.eat(Token.LPARENS)

        return f

    def parse(self):
        """Parses the whole AST."""
        return self.parse_program()


class NodeVisitor:
    """Base class for the node visitor pattern."""
    def visit(self, node):
        """Dispatches the visit call to the appropriate function."""
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Default method for unknown nodes."""
        raise Exception(f"No visit method for {type(node).__name__}")

class Interpreter(NodeVisitor):
    """APL interpreter using the visitor pattern."""

    def __init__(self, parser):
        self.parser = parser
        self.var_lookup = {}

    def visit_S(self, scalar):
        """Returns the value of a scalar."""
        return APLArray([], scalar.value)

    def visit_V(self, array):
        """Returns the value of an array."""
        scalars = [self.visit(child) for child in array.children]
        return APLArray([len(scalars)], scalars)

    def visit_Var(self, var):
        """Tries to fetch the value of a variable."""
        return self.var_lookup[var.name]

    def visit_Statements(self, statements):
        """Visits each statement in order."""
        return [self.visit(child) for child in statements.children[::-1]][-1]

    def visit_Assignment(self, assignment):
        """Assigns a value to a variable."""

        value = self.visit(assignment.value)
        varname = assignment.varname.name
        self.var_lookup[varname] = value
        return value

    def visit_Monad(self, monad):
        """Evaluate the function on its only argument."""

        function = self.visit(monad.function)
        omega = self.visit(monad.omega)
        return function(omega=omega)

    def visit_Dyad(self, dyad):
        """Evaluate a dyad on both its arguments."""

        function = self.visit(dyad.function)
        omega = self.visit(dyad.omega)
        alpha = self.visit(dyad.alpha)
        return function(alpha=alpha, omega=omega)

    def visit_F(self, func):
        """Fetch the callable function."""

        name = func.token.type.lower()
        function = getattr(functions, name, None)
        if function is None:
            raise Exception(f"Could not find function {name}.")
        return function

    def visit_MOp(self, mop):
        """Fetch the operand and alter it."""

        aalpha = self.visit(mop.child)
        name = mop.token.type.lower()
        operator = getattr(moperators, name, None)
        if operator is None:
            raise Exception(f"Could not find monadic operator {name}.")
        return operator(aalpha=aalpha)

    def visit_DOp(self, dop):
        """Fetch the operands and alter them as needed."""

        oomega = self.visit(dop.right)
        aalpha = self.visit(dop.left)
        name = dop.token.type.lower()
        operator = getattr(doperators, name, None)
        if operator is None:
            raise Exception(f"Could not find dyadic operator {name}.")
        return operator(aalpha=aalpha, oomega=oomega)

    def interpret(self):
        """Interpret the APL code the parser was given."""
        tree = self.parser.parse()
        return self.visit(tree)

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Parse and interpret an APL program.")
    main_group = arg_parser.add_mutually_exclusive_group()
    main_group.add_argument(
        "--repl",
        action="store_true",
        help="starts a REPL session",
    )
    main_group.add_argument(
        "-f",
        "--file",
        nargs=1,
        metavar="filename",
        help="filename with code to parse and interpret",
        type=str,
    )
    main_group.add_argument(
        "-c",
        "--code",
        nargs="+",
        metavar="expression",
        help="expression(s) to be interpreted",
        type=str,
    )

    args = arg_parser.parse_args()

    if args.repl:
        print("Please notice that, from one input line to the next, variables aren't stored (yet).")
        while inp := input(" >> "):
            try:
                print(Interpreter(Parser(Tokenizer(inp), debug=True)).interpret())
            except Exception as error:
                print(error)

    elif args.code:
        for expr in args.code:
            print(f"{expr} :")
            print(Interpreter(Parser(Tokenizer(expr), debug=True)).interpret())

    elif args.file:
        print("Not implemented yet...")

    else:
        arg_parser.print_usage()
