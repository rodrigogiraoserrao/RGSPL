"""
Implement a subset of the APL programming language.

Supports the monadic/dyadic functions +-×÷ ;
Supports (negative) integers/floats and vectors of those ;
Supports the monadic operator ⍨ ;
Supports parenthesized expressions ;

Parses the following grammar, read from right to left:

STATEMENT := STATEMENT* FUNCTION ARRAY
ARRAY := ARRAY* ( "(" STATEMENT ")" | NUMBER )
NUMBER := "¯"? ( INTEGER | FLOAT )
FUNCTION := F "⍨"?
F := "+" | "-" | "×" | "÷"
"""


class Token:
    """Represents a token parsed from the source code."""

    FUNCTIONS = "+-×÷"

    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    DIVIDE = "DIVIDE"
    NEGATE = "NEGATE"
    COMMUTE = "COMMUTE"
    EOF = "EOF"

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

    def get_function_token(self):
        """Retrieves a function token."""

        mapping = {
            "+": Token.PLUS,
            "-": Token.MINUS,
            "×": Token.TIMES,
            "÷": Token.DIVIDE,
        }
        char = self.current_char
        if char in mapping:
            self.advance()
            return Token(mapping[char], char)

        self.error("Could not parse function token.")

    def get_next_token(self):
        """Finds the next token in the source code."""

        self.skip_whitespace()
        if not self.current_char:
            return Token(Token.EOF, None)

        if self.current_char in "0123456789":
            return self.get_number_token()

        if self.current_char in "+-×÷":
            return self.get_function_token()

        if self.current_char == "⍨":
            self.advance()
            return Token(Token.COMMUTE, "⍨")

        self.error("Could not parse the next token...")

    def tokenize(self):
        """Returns the whole token list."""

        tokens = [self.get_next_token()]
        while tokens[-1].type != Token.EOF:
            tokens.append(self.get_next_token())
        return tokens[::-1]


if __name__ == "__main__":
    while inp := input(" >> "):
        print(Tokenizer(inp).tokenize())
