"""KIRA compiler front end: main program.

Usage:  python kira.py <file.kira>

Runs the lexer, prints the token stream and token counts, then runs the
parser and prints the AST. If the lexer finds any error, the parser is
skipped. Every error is printed as a message, never as a Python crash.
"""

import sys

from lexer import tokenize, print_token_stream, print_token_counts
from parser import parse_program
from ast_printer import KiraSyntaxError, print_ast, write_dot


def read_source(path):
    """Return the file's text, or None after printing why it could not be read."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file '{path}' not found")
    except IsADirectoryError:
        print(f"Error: '{path}' is a folder, not a file")
    except UnicodeDecodeError:
        print(f"Error: '{path}' is not a valid UTF-8 text file")
    except OSError as e:
        print(f"Error: cannot read '{path}': {e.strerror}")
    return None


def run(path):
    source = read_source(path)
    if source is None:
        return

    # 1 and 2: lexer output (print_token_stream also lists lexical errors)
    tokens, errors = tokenize(source)
    print_token_stream(tokens, errors)
    print_token_counts(tokens)

    if errors:
        print(f"\n{len(errors)} lexical error(s). Parsing skipped.")
        return

    # 3: parser and AST
    print("\nAST")
    try:
        tree = parse_program(tokens)
    except KiraSyntaxError as e:
        print(e)
        return

    print_ast(tree)

    # Graphviz version of the tree (render with: dot -Tpng ast.dot -o ast.png)
    try:
        write_dot(tree, "ast.dot")
        print("\nGraphviz tree written to ast.dot")
    except OSError:
        pass  # the text tree is already printed, so this is not fatal


def main():
    if len(sys.argv) != 2:
        print("Usage: python kira.py <file.kira>")
        return

    # The parser is recursive, so very long or deeply nested programs
    # need more than Python's default limit of 1000 calls.
    sys.setrecursionlimit(20000)
    try:
        run(sys.argv[1])
    except RecursionError:
        print("Error: program is too deeply nested to parse")
    except Exception as e:  # last safety net: never show a stack trace
        print(f"Error: unexpected problem ({type(e).__name__}: {e})")


if __name__ == "__main__":
    main()