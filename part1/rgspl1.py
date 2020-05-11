"""
Implement a subset of the APL programming language.

Supports the monadic/dyadic functions +-×÷ ;
Supports (negative) integers/floats and vectors of those ;
Supports the monadic operator ⍨ ;
Supports parenthesized expressions ;

Read from right to left, this is the grammar supported:
    PROGRAM := EOF STATEMENT
    STATEMENT := ( ARRAY FUNCTION | FUNCTION )* ARRAY
    ARRAY := ARRAY* ( "(" STATEMENT ")" | SCALAR )
    SCALAR := INTEGER | FLOAT
    FUNCTION := F | FUNCTION "⍨"
    F := "+" | "-" | "×" | "÷"
"""


class Token:
    """Represents a token parsed from the source code."""

    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    DIVIDE = "DIVIDE"
    NEGATE = "NEGATE"
    COMMUTE = "COMMUTE"
    LPARENS = "LPARENS"
    RPARENS = "RPARENS"
    EOF = "EOF"

    # Helpful lists of token types.
    FUNCTIONS = [PLUS, MINUS, TIMES, DIVIDE]
    MONADIC_OPS = [COMMUTE]

    # What You See Is What You Get characters that correspond to tokens.
    WYSIWYG = "+-×÷()⍨"
    # The mapping from characteres to token types.
    mapping = {
        "+": PLUS,
        "-": MINUS,
        "×": TIMES,
        "÷": DIVIDE,
        "(": LPARENS,
        ")": RPARENS,
        "⍨": COMMUTE,
    }

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
        self.pos = len(self.code) - 1
        self.current_char = self.code[self.pos]

    def error(self, message):
        """Raises a Tokenizer error."""
        raise Exception(f"TokenizerError: {message}")

    def advance(self):
        """Advances the cursor position and sets the current character."""

        self.pos -= 1
        self.current_char = None if self.pos < 0 else self.code[self.pos]

    def skip_whitespace(self):
        """Skips all the whitespace in the source code."""

        while self.current_char and self.current_char in " \t":
            self.advance()

    def get_integer(self):
        """Parses an integer from the source code."""

        end_idx = self.pos
        while self.current_char and self.current_char.isdigit():
            self.advance()
        return self.code[self.pos+1:end_idx+1]

    def get_number_token(self):
        """Parses a number token from the source code."""

        parts = [self.get_integer()]
        # Check if we have a decimal number here.
        if self.current_char == ".":
            self.advance()
            parts.append(".")
            parts.append(self.get_integer())
        # Check for a negation of the number.
        if self.current_char == "¯":
            self.advance()
            parts.append("-")

        num = "".join(parts[::-1])
        if "." in num:
            return Token(Token.FLOAT, float(num))
        else:
            return Token(Token.INTEGER, int(num))

    def get_wysiwyg_token(self):
        """Retrieves a WYSIWYG token."""

        char = self.current_char
        if char in Token.mapping:
            self.advance()
            return Token(Token.mapping[char], char)

        self.error("Could not parse WYSIWYG token.")

    def get_next_token(self):
        """Finds the next token in the source code."""

        self.skip_whitespace()
        if not self.current_char:
            return Token(Token.EOF, None)

        if self.current_char in "0123456789":
            return self.get_number_token()

        if self.current_char in Token.WYSIWYG:
            return self.get_wysiwyg_token()

        self.error("Could not parse the next token...")

    def tokenize(self):
        """Returns the whole token list."""

        tokens = [self.get_next_token()]
        while tokens[-1].type != Token.EOF:
            tokens.append(self.get_next_token())
        return tokens[::-1]


class ASTNode:
    """Stub class to be inherited by the different types of AST nodes.

    The AST Nodes are used by the Parser instances to build an
        Abstract Syntax Tree out of the APL programs.
    These ASTs can then be traversed to interpret an APL program.
    """


class Scalar(ASTNode):
    """Node for a simple scalar like 3 or ¯4.2"""
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return f"S({self.value})"

    def __repr__(self):
        return self.__str__()


class Array(ASTNode):
    """Node for an array of simple scalars, like 3 ¯4 5.6"""
    def __init__(self, children):
        self.children = children

    def __str__(self):
        return f"A({self.children})"

    def __repr__(self):
        return self.__str__()


class MOp(ASTNode):
    """Node for monadic operators like ⍨"""
    def __init__(self, token, child):
        self.token = token
        self.child = child

    def __str__(self):
        return f"MOp({self.token.value} {self.child})"

    def __repr__(self):
        return self.__str__()


class Monad(ASTNode):
    """Node for monadic functions."""
    def __init__(self, token, child):
        self.token = token
        self.child = child

    def __str__(self):
        return f"Monad({self.token.value} {self.child})"

    def __repr__(self):
        return self.__str__()


class Dyad(ASTNode):
    """Node for dyadic functions."""
    def __init__(self, token, left, right):
        self.token = token
        self.left = left
        self.right = right

    def __str__(self):
        return f"Dyad({self.token.value} {self.left} {self.right})"

    def __repr__(self):
        return self.__str__()


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
        node = self.parse_statement()
        self.eat(Token.EOF)
        return node

    def parse_statement(self):
        """Parses a statement."""

        self.debug(f"Parsing statement from {self.tokens[:self.pos+1]}")
        node = self.parse_array()
        while self.token_at.type in Token.FUNCTIONS + Token.MONADIC_OPS:
            # pylint: disable=attribute-defined-outside-init
            func, base = self.parse_function()
            if isinstance(base, Dyad):
                base.right = node
                base.left = self.parse_array()
            elif isinstance(base, Monad):
                base.child = node
            else:
                self.error(f"Got {type(base)} instead of a Monad/Dyad.")
            node = func
        return node

    def parse_array(self):
        """Parses an array composed of possibly several simple scalars."""

        self.debug(f"Parsing array from {self.tokens[:self.pos+1]}")
        nodes = []
        while self.token_at.type in [Token.RPARENS, Token.INTEGER, Token.FLOAT]:
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
            node = Array(nodes)
        return node

    def parse_scalar(self):
        """Parses a simple scalar."""

        self.debug(f"Parsing scalar from {self.tokens[:self.pos+1]}")
        if self.token_at.type == Token.INTEGER:
            node = Scalar(self.token_at)
            self.eat(Token.INTEGER)
        else:
            node = Scalar(self.token_at)
            self.eat(Token.FLOAT)
        return node

    def parse_function(self):
        """Parses a function possibly monadically operated upon."""

        self.debug(f"Parsing function from {self.tokens[:self.pos+1]}")
        if self.token_at.type in Token.MONADIC_OPS:
            node = MOp(self.token_at, None)
            self.eat(self.token_at.type)
            node.child, base = self.parse_function()
        else:
            base = node = self.parse_f()
        return node, base

    def parse_f(self):
        """Parses a simple one-character function.

        We have to peek forward to decide if the function is monadic or dyadic.
        """

        self.debug(f"Parsing f from {self.tokens[:self.pos+1]}")
        if self.peek() in [Token.RPARENS, Token.INTEGER, Token.FLOAT]:
            node = Dyad(self.token_at, None, None)
        else:
            node = Monad(self.token_at, None)
        self.eat(node.token.type)
        return node

    def parse(self):
        """Parses the whole AST."""
        return self.parse_program()

if __name__ == "__main__":

    print("Welcome!")
    print("Type in an APL expression with integers, floats (and vectors of those)")
    print("  and making use of ¯+-×÷⍨ and see it get tokenized and parsed into an AST.")
    while inp := input(" >> "):
        p = Parser(Tokenizer(inp))
        print(p.tokens)
        print(p.parse())
