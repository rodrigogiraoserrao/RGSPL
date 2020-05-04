# Token types
#
# EOF (end-of-file) token is used to indicate that there is no more input left.
INTEGER, NEGATE, EOF = "INTEGER", "NEGATE", "EOF"
LPARENS, RPARENS = "LPARENS", "RPARENS"
PLUS, MINUS, TIMES, DIVISION = "PLUS", "MINUS", "TIMES", "DIVISION"
OPS = {
    PLUS: lambda l, r: l+r,
    MINUS: lambda l, r: l-r,
    TIMES: lambda l, r: l*r,
    DIVISION: lambda l, r: l/r,
}

# We accept the following grammar with the rules matching from right to left:
#
# STATEMENT := EOF (TERM OP)* TERM
# TERM := NUM | LPARENS STATEMENT RPARENS
# NUM := NEGATE? INTEGER
# OP := PLUS | MINUS | TIMES | DIVISION


class Token:
    def __init__(self, type_, value):
        # Token type, e.g. INTEGER or LPARENS
        self.type = type_
        # Token value, e.g. 45 or "("
        self.value = value

    def __str__(self):
        """String representation of a Token instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, "+")
        """
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()


class Lexer:
    """Takes a line of code and breaks it into tokens."""

    OP_CHARS = "+-÷×¯"

    def __init__(self, text):
        self.text = text
        # We traverse from right to left
        self.pos = len(self.text) - 1
        self.current_char = self.text[self.pos]
        self.current_token = None

    def error(self, msg="Error in lexer!"):
        """Raises an error."""
        raise Exception(msg)

    def advance(self):
        """Advance internal pointer and get the next character."""

        self.pos -= 1
        if self.pos < 0:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Ignores whitespace."""

        while self.current_char and self.current_char.isspace():
            self.advance()

    def get_integer_token(self):
        """Creates a multidigit integer token."""

        stop = self.pos + 1
        while self.current_char and self.current_char.isdigit():
            self.advance()
        num = self.text[self.pos + 1:stop]
        return Token(INTEGER, int(num))

    def get_op_token(self):
        """Returns an operator token."""

        tok = None
        if self.current_char == "+":
            tok = Token(PLUS, "+")
        elif self.current_char == "-":
            tok = Token(MINUS, "-")
        elif self.current_char == "×":
            tok = Token(TIMES, "×")
        elif self.current_char == "÷":
            tok = Token(DIVISION, "÷")
        elif self.current_char == "¯":
            tok = Token(NEGATE, "¯")

        if tok is not None:
            self.advance()
            return tok
        else:
            return self.error("Could not parse operator token.")

    def get_next_token(self):
        """Lexical analyzer (aka scanner or tokenizer)

        This method is responsible for breaking a sentence into tokens, one at a time.
        """

        self.skip_whitespace()
        # Check if we already parsed everything.
        if not self.current_char:
            return Token(EOF, None)

        # Check what type of token we have now.
        if self.current_char.isdigit():
            return self.get_integer_token()

        if self.current_char in self.OP_CHARS:
            return self.get_op_token()

        if self.current_char == ")":
            self.advance()
            return Token(RPARENS, ")")
        elif self.current_char == "(":
            self.advance()
            return Token(LPARENS, "(")

        self.error("Could not parse an appropriate token.")

class Interpreter:
    def __init__(self, lexer):
        # Client string input, e.g. "6×3+5"
        self.lexer = lexer
        # Current token instance
        self.current_token = self.lexer.get_next_token()

    def error(self, msg="Error parsing input."):
        """Raises an interpreter error with a custom message."""
        raise Exception(msg)

    def eat(self, token_type):
        """Compare the current token with th⌈e expected token type."""

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected type {token_type} and got {self.current_token}")

    def num(self):
        """Interprets a NUM."""

        result = self.current_token.value
        self.eat(INTEGER)

        if self.current_token.type == NEGATE:
            result *= -1
            self.eat(NEGATE)

        return result

    def term(self):
        """Interprets a TERM."""

        if self.current_token.type == RPARENS:
            self.eat(RPARENS)
            result = self.statement()
            self.eat(LPARENS)
        else:
            result = self.num()

        return result

    def statement(self):
        """Interprets a STATEMENT."""

        result = self.term()
        while self.current_token.type in [PLUS, MINUS, TIMES, DIVISION]:
            op = self.current_token.type
            self.eat(self.current_token.type)
            left_term = self.term()

            result = OPS[op](left_term, result)

        return result

    def interpret(self):
        """Interprets the client string."""

        result = self.statement()
        self.eat(EOF)
        return result


def main():
    while (inp := input(" >> ")):
        lexer = Lexer(inp)
        interpreter = Interpreter(lexer)
        result = interpreter.interpret()
        print(result)


if __name__ == "__main__":
    main()
