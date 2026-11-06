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

            elif ch.isalpha():
                word = ""
                while self.peek() != "" and (self.peek().isalnum() or self.peek() == "_"):
                    word += self.advance()
                if word in KEYWORDS:
                    self.add_token("KEYWORD", word, start_line, start_col)
                else:
                    self.add_token("IDENTIFIER", word, start_line, start_col)

            elif ch.isdigit():
                num = ""
                while self.peek() != "" and self.peek().isdigit():
                    num += self.advance()
                if self.peek() != "" and (self.peek().isalpha() or self.peek() == "_"):
                    while self.peek() != "" and (self.peek().isalnum() or self.peek() == "_"):
                        num += self.advance()
                    self.add_error(start_line, start_col, f"malformed token '{num}'")
                else:
                    self.add_token("INTEGER", num, start_line, start_col)

            elif ch in "=<>!":
                self.advance()
                if self.peek() == "=":
                    self.advance()
                    self.add_token("REL_OP", ch + "=", start_line, start_col)
                elif ch == "=":
                    self.add_token("ASSIGN", ch, start_line, start_col)
                elif ch == "!":
                    self.add_error(start_line, start_col, f"invalid character '{ch}'")
                else:
                    self.add_token("REL_OP", ch, start_line, start_col)

            elif ch == "#":
                # skip comment until end of line
                while self.peek() != "" and self.peek() != "\n":
                    self.advance()

            else:
                self.advance()
                self.add_error(start_line, start_col, f"invalid character '{ch}'")

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

    print("Total tokens:", len(toks) - 1)   # -1 because EOF is not counted