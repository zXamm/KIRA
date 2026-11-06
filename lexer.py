from token_def import Token, KEYWORDS, EOF, TOKEN_TYPES

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

            elif ch.isascii() and ch.isalpha():
                word = ""
                while self.peek() != "" and (self.peek().isascii() and self.peek().isalnum() or self.peek() == "_"):
                    word += self.advance()
                if word in KEYWORDS:
                    self.add_token("KEYWORD", word, start_line, start_col)
                else:
                    self.add_token("IDENTIFIER", word, start_line, start_col)

            elif ch.isascii() and ch.isdigit():
                num = ""
                while self.peek() != "" and self.peek().isascii() and self.peek().isdigit():
                    num += self.advance()
                if self.peek() != "" and (self.peek().isascii() and self.peek().isalpha() or self.peek() == "_"):
                    while self.peek() != "" and (self.peek().isascii() and self.peek().isalnum() or self.peek() == "_"):
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

def print_token_stream(tokens, errors):
    print("TOKEN STREAM")
    print("+------+------+--------------+----------------+")
    print("| Line | Col  | Type         | Lexeme         |")
    print("+------+------+--------------+----------------+")
    for t in tokens:
        if t.type == EOF:
            continue
        print(f"| {t.line:<4} | {t.col:<4} | {t.type:<12} | {t.lexeme:<14} |")
    print("+------+------+--------------+----------------+")
    if errors:
        print(f"\n{len(errors)} lexical error(s) found:")
        for e in errors:
            print("  " + e)


def print_token_counts(tokens):
    counts = {}
    for t in tokens:
        if t.type != EOF:
            counts[t.type] = counts.get(t.type, 0) + 1

    total = sum(counts.values())
    print("\nTOKEN COUNTS")
    for ty in TOKEN_TYPES:
        if ty in counts:
            print(f"  {ty:<12} : {counts[ty]:>3}")
    print("  " + "-" * 18)
    print(f"  {'TOTAL':<12} : {total:>3}")

# Just for testing the lexer from the command line before kira.py is ready to use it. (Later, will be remove)
if __name__ == "__main__":
    import sys
    with open(sys.argv[1], encoding="utf-8") as f:
        toks, errs = tokenize(f.read())
    print_token_stream(toks, errs)
    print_token_counts(toks)