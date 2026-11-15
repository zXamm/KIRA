"""Shared Token definition for the KIRA front end.

Used by the lexer (creates tokens) and the parser (reads tokens).
Do not change without telling the group. See TOKENS.md.
"""

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
        self.type = type     
        self.lexeme = lexeme  
        self.line = line      
        self.col = col       

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme!r}, {self.line}, {self.col})"
