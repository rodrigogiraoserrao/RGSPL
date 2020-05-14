"""
Implement a subset of the APL programming language.

Supports the monadic/dyadic functions +-×÷ ;
Supports (negative) integers/floats and vectors of those ;
Supports the monadic operator ⍨ ;
Supports parenthesized expressions ;

Read from right to left, this is the grammar supported:

    program := EOF statemnt
    statement := ( ID "←" | array function | function )* array
    function := f | function mop
    mop := "⍨"
    f := "+" | "-" | "×" | "÷" | "⌈" | "⌊"
    array := scalar | ( "(" statement ")" | scalar )+
    scalar := INTEGER | FLOAT | ID
"""
# pylint: disable=invalid-name

from typing import List


class Token:
    """Represents a token parsed from the source code."""

    # "Data types"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    ID = "ID"
    # Functions
    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    DIVIDE = "DIVIDE"
    CEILING = "CEILING"
    FLOOR = "FLOOR"
    # Operators
    COMMUTE = "COMMUTE"
    # Misc
    NEGATE = "NEGATE"
    ASSIGNMENT = "ASSIGNMENT"
    LPARENS = "LPARENS"
    RPARENS = "RPARENS"
    EOF = "EOF"

    # Helpful lists of token types.
    FUNCTIONS = [PLUS, MINUS, TIMES, DIVIDE, FLOOR, CEILING]
    MONADIC_OPS = [COMMUTE]

    # What You See Is What You Get characters that correspond to tokens.
    # The mapping from characteres to token types.
    WYSIWYG_MAPPING = {
        "+": PLUS,
        "-": MINUS,
        "×": TIMES,
        "÷": DIVIDE,
        "⌈": CEILING,
        "⌊": FLOOR,
        "⍨": COMMUTE,
        "←": ASSIGNMENT,
        "(": LPARENS,
        ")": RPARENS,
    }

    ID_CHARS = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()


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

    def get_integer(self):
        """Parses an integer from the source code."""

        start_idx = self.pos
        while self.current_char and self.current_char.isdigit():
            self.advance()
        return self.code[start_idx:self.pos]

    def get_number_token(self):
        """Parses a number token from the source code."""

        parts = []
        # Check for a negation of the number.
        if self.current_char == "¯":
            self.advance()
            parts.append("-")
        parts.append(self.get_integer())
        # Check if we have a decimal number here.
        if self.current_char == ".":
            self.advance()
            parts.append(".")
            parts.append(self.get_integer())

        num = "".join(parts)
        if "." in num:
            return Token(Token.FLOAT, float(num))
        else:
            return Token(Token.INTEGER, int(num))

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
        if not self.current_char:
            return Token(Token.EOF, None)

        if self.current_char in "¯0123456789":
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


class A(ASTNode):
    """Node for an array of simple scalars, like 3 ¯4 5.6"""
    def __init__(self, children: List[ASTNode]):
        self.children = children

    def __str__(self):
        return f"A({self.children})"


class MOp(ASTNode):
    """Node for monadic operators like ⍨"""
    def __init__(self, token: Token, child: ASTNode):
        self.token = token
        self.child = child

    def __str__(self):
        return f"MOp({self.token.value} {self.child})"


class F(ASTNode):
    """Node for built-in functions like + or ⌈"""
    def __init__(self, function: Token):
        self.function = function

    def __str__(self):
        return f"F({self.function.value})"


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

    def __str__(self):
        return f"Var({self.token.value})"


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

    def parse_program(self):
        """Parses a full program."""

        self.debug(f"Parsing program from {self.tokens}")
        statement = self.parse_statement()
        self.eat(Token.EOF)
        return statement

    def parse_statement(self):
        """Parses a statement."""

        self.debug(f"Parsing statement from {self.tokens[:self.pos+1]}")

        relevant_types = [Token.ASSIGNMENT] + Token.FUNCTIONS + Token.MONADIC_OPS
        statement = self.parse_array()
        while self.token_at.type in relevant_types:
            if self.token_at.type == Token.ASSIGNMENT:
                self.eat(Token.ASSIGNMENT)
                statement = Assignment(Var(self.token_at), statement)
                self.eat(Token.ID)
            else:
                function = self.parse_function()
                if self.token_at.type in [Token.RPARENS, Token.INTEGER, Token.FLOAT, Token.ID]:
                    array = self.parse_array()
                    statement = Dyad(function, array, statement)
                else:
                    statement = Monad(function, statement)

        return statement

    def parse_array(self):
        """Parses an array composed of possibly several simple scalars."""

        self.debug(f"Parsing array from {self.tokens[:self.pos+1]}")

        nodes = []
        while self.token_at.type in [
            Token.RPARENS, Token.INTEGER, Token.FLOAT, Token.ID
        ]:
            if self.token_at.type == Token.RPARENS:
                self.eat(Token.RPARENS)
                nodes.append(self.parse_statement())
                self.eat(Token.LPARENS)
            else:
                nodes.append(self.parse_scalar())
        nodes = nodes[::-1]
        if not nodes:
            self.error("Failed to parse scalars inside an array.")
        elif len(nodes) == 1:
            node = nodes[0]
        else:
            node = A(nodes)
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
        else:
            scalar = S(self.token_at)
            self.eat(Token.FLOAT)

        return scalar

    def parse_function(self):
        """Parses a function possibly monadically operated upon."""

        self.debug(f"Parsing function from {self.tokens[:self.pos+1]}")

        if self.token_at.type in Token.MONADIC_OPS:
            function = self.parse_mop()
            function.child = self.parse_function()
        else:
            function = self.parse_f()
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

        f = F(self.token_at)
        if (t := self.token_at.type) not in Token.FUNCTIONS:
            self.error(f"{t} is not a valid function.")
        self.eat(t)

        return f

    def parse(self):
        """Parses the whole AST."""
        return self.parse_program()

if __name__ == "__main__":
    while inp := input(" >> "):
        print(Parser(Tokenizer(inp), debug=True).parse())
