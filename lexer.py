from token_def import Token, KEYWORDS, EOF

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        self.errors = []

    def peek(self):
        # return current char, or "" if at the end
        if self.pos < len(self.source):
            return self.source[self.pos]
        return ""
        

    def advance(self):
        # move forward 1 char
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch
        
    def add_token(self, type, lexeme, line, col):
        # append a Token
        self.tokens.append(Token(type, lexeme, line, col))
        

    def add_error(self, line, col, message):
        # append "LexicalError at line L, col C: message"
        self.errors.append(f"LexicalError at line {line}, col {col}: {message}")
        

    SINGLE_CHARS = {
        "+": "ARITH_OP", "-": "ARITH_OP", "*": "ARITH_OP", "/": "ARITH_OP",
        "%": "ARITH_OP", "(": "LPAREN", ")": "RPAREN",
        "{": "LBRACE", "}": "RBRACE", ";": "SEMICOLON",
    }

    def tokenize(self):
        while self.peek() != "":
            ch = self.peek()
            start_line, start_col = self.line, self.col

            if ch in " \t\r\n":
                self.advance()  # skip whitespace

            elif ch in self.SINGLE_CHARS:
                self.advance()
                self.add_token(self.SINGLE_CHARS[ch], ch, start_line, start_col)

            else:
                self.advance()
                self.add_error(self.line, self.col, f"Unexpected character: {ch}")

        self.add_token(EOF, "", self.line, self.col)
        return self.tokens, self.errors

def tokenize(source):
    return Lexer(source).tokenize()

# Just for testing the lexer from the command line before kira.py is ready to use it.
if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        toks, errs = tokenize(f.read())
    for t in toks:
        print(t)    
    for e in errs:
        print(e)