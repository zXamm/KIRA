"""Shared Token definition for the KIRA front end.

Used by the lexer (creates tokens) and the parser (reads tokens).
Do not change without telling the group. See TOKENS.md.
"""

# Token types, in the order they are printed in TOKEN COUNTS
TOKEN_TYPES = [
    "KEYWORD",
    "IDENTIFIER",
    "INTEGER",
    "ARITH_OP",
    "REL_OP",
    "ASSIGN",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "SEMICOLON",
]

# Special token added at the end of the list (not printed, not counted)
EOF = "EOF"

KEYWORDS = {"let", "if", "else", "while", "print"}


class Token:
    def __init__(self, type, lexeme, line, col):
        self.type = type      # e.g. "KEYWORD"
        self.lexeme = lexeme  # always a string, e.g. "let", "42"
        self.line = line      # starts from 1
        self.col = col        # starts from 1

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme!r}, {self.line}, {self.col})"