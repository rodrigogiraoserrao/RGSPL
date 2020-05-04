"""
Implement a basic calculator with APL-like syntax.

This simple calculator only implements the operators +-×÷ and ¯ on simple integer scalars.
This is the grammar accepted, where rules match from right to left.
STATEMENT := EOL (TERM OP)* TERM
TERM := NUM | "(" STATEMENT ")"
NUM := "¯"? INTEGER
OP := "+" | "-" | "×" | "÷"
"""

import abc

# Token types
# EOL (end-of-line) token is used to indicate that there is no more input left.
INTEGER, NEGATE, EOL = "INTEGER", "NEGATE", "EOL"
LPARENS, RPARENS = "LPARENS", "RPARENS"
PLUS, MINUS, TIMES, DIVISION = "PLUS", "MINUS", "TIMES", "DIVISION"
OPS = {
    PLUS: lambda l, r: l+r,
    MINUS: lambda l, r: l-r,
    TIMES: lambda l, r: l*r,
    DIVISION: lambda l, r: l/r,
}

def error(msg="Error with RGSPL."):
    """Raise an exception from the RGSPL inner workings."""
    raise Exception(msg)

class Token:
    """Token class for our interpreter."""

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
    """A lexer instance has the job of breaking down code into tokens."""

    OP_CHARS = "+-÷×¯"

    def __init__(self, text):
        self.text = text
        # We traverse from right to left
        self.pos = len(self.text) - 1
        self.current_char = self.text[self.pos]
        self.current_token = None

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
            return error("Could not parse operator token.")

    def get_next_token(self):
        """Lexical analyzer (aka scanner or tokenizer)

        This method is responsible for breaking a sentence into tokens, one at a time.
        """

        self.skip_whitespace()
        # Check if we already parsed everything.
        if not self.current_char:
            return Token(EOL, None)

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

        error("Could not parse an appropriate token.")

class ASTNode(abc.ABC):
    """Base class for all the ASTNode classes."""

class UnOp(ASTNode):
    """Node for unary operations."""
    def __init__(self, op, child):
        self.token = self.op = op
        self.child = child

    def __str__(self):
        return f"{self.token} [{self.child}]"

class BinOp(ASTNode):
    """Node for binary operations."""
    def __init__(self, op, left, right):
        self.token = self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.token} [{self.left}   {self.right}]"

class Num(ASTNode):
    """Node for numbers."""
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

    def __str__(self):
        return f"{self.token}"

class Parser:
    """Parses code into an Abstract Syntax Tree (AST)."""

    def __init__(self, lexer):
        # Client string input, e.g. "6×3+5"
        self.lexer = lexer
        # Current token instance
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        """Compare the current token with the expected token type."""

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            error(f"Expected type {token_type} and got {self.current_token}")

    def num(self):
        """Parses a NUM."""

        node = Num(self.current_token)
        self.eat(INTEGER)

        if self.current_token.type == NEGATE:
            node = UnOp(self.current_token, node)
            self.eat(NEGATE)

        return node

    def term(self):
        """Parses a TERM."""

        if self.current_token.type == RPARENS:
            self.eat(RPARENS)
            node = self.statement()
            self.eat(LPARENS)
        else:
            node = self.num()

        return node

    def statement(self):
        """Parses a STATEMENT."""

        node = self.term()
        while self.current_token.type in [PLUS, MINUS, TIMES, DIVISION]:
            op = self.current_token
            self.eat(self.current_token.type)
            left_node = self.term()

            node = BinOp(op, left_node, node)

        return node

    def parse(self):
        """Parses the client string."""

        node = self.statement()
        self.eat(EOL)
        return node

class NodeVisitor:
    """Any type of interpreter must inherit from this base class."""
    def visit(self, node):
        """Dispatch the correct visit method for a given node."""
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Triggers an error for visitors that haven't been implemented."""
        error(f"No visitor for {type(node).__name__}!")

class Interpreter(NodeVisitor):
    """Interprets the code with the NodeVisitor pattern."""

    def __init__(self, parser):
        self.parser = parser

    def visit_Num(self, node):
        """Visit a Num node and return its intrinsic value."""
        return node.value

    def visit_UnOp(self, node):
        """Visit a UnOp and apply its operation to its child."""

        value = self.visit(node.child)
        if node.token.type == NEGATE:
            return -value
        error(f"Could not visit UnOp {node}")

    def visit_BinOp(self, node):
        """Visit a BinOp and apply its operation to its children."""

        right = self.visit(node.right)
        left = self.visit(node.left)
        func = OPS.get(node.token.type, None)
        if func:
            return func(left, right)
        error(f"Could not visit BinOp {node}")

    def interpret(self):
        """Interprets a given piece of code and returns its result."""
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    """Run a REPL to test the code."""

    while inp := input(" >> "):
        lexer = Lexer(inp)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == "__main__":
    main()
