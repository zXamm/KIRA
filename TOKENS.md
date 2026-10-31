# KIRA Token Contract

> Agreed by all 4 members – 31 Oct 2026
> Language: Python 3.15

## 1. Token object

Defined in `token_def.py`:

```
Token(type, lexeme, line, col)
```

| Field    | Meaning                                                        |
|----------|----------------------------------------------------------------|
| `type`   | One of the token type strings below, spelled exactly the same  |
| `lexeme` | The original text from the file, **always a string** (`"42"`)  |
| `line`   | Line number, starting from 1                                   |
| `col`    | Column of the token's first character, starting from 1 (tab = 1 column) |

## 2. Token types

Printed and counted in this order:

```
KEYWORD     let if else while print   (lowercase only; "Let" is an IDENTIFIER)
IDENTIFIER  letter (letter | digit | _)*   case-sensitive
INTEGER     digit+
ARITH_OP    + - * / %
REL_OP      == != < > <= >=
ASSIGN      =
LPAREN      (
RPAREN      )
LBRACE      {
RBRACE      }
SEMICOLON   ;
EOF         (empty lexeme, added at the end, NOT printed and NOT counted)
```

## 3. Lexer rules

- Skip spaces, tabs and newlines.
- `#` starts a comment until the end of the line. Comments are not tokens.
- Longest match: `<=` before `<`, `>=` before `>`, `==` before `=`, `!=` before `!`.
- Read the whole word first, then check whether it is a keyword.

## 4. Lexical errors

Report **every** error, keep scanning, and produce **no token** for the bad part.

| Case                              | Example | Message                                   |
|-----------------------------------|---------|-------------------------------------------|
| Character not in the language     | `$` `@` | `invalid character '$'`                   |
| `!` not followed by `=`           | `!`     | `invalid character '!'`                   |
| Identifier starting with `_`      | `_x`    | `invalid character '_'`, then `x` is an IDENTIFIER |
| Digits followed by letters        | `2nd`   | `malformed token '2nd'` (whole word, one error) |

Format:
```
LexicalError at line L, col C: <message>
```

## 5. Lexer interface

```python
tokens, errors = tokenize(source)
```

- `source` – the whole text of the `.kira` file
- `tokens` – list of `Token`, always ends with one `EOF` token
- `errors` – list of error message strings (empty if no errors)

If `errors` is not empty, the parser does **not** run.

## 6. Output format

```
== TOKEN STREAM ==
LINE  COL  TYPE        LEXEME
   2    1  KEYWORD     let
...
(lexical errors printed here, if any)

== TOKEN COUNTS ==
Total tokens: N
  KEYWORD     5
  ...                  (types with count 0 are left out)

== AST ==
(tree, or the SyntaxError)
```

If there are lexical errors, the last line is:
```
N lexical error(s). Parsing skipped.
```

## 7. Who owns which file

| File                |                     Owner                    |
|---------------------|----------------------------------------------|
| `token_def.py`      | Shared (change only after telling the group) |
| `lexer.py`          | Irham                                        |
| `parser.py`         | Din (statements), Aiman (expressions)        |
| `ast_printer.py`    | Aiman                                        |
| `kira.py`, `tests/` | Naqqib                                       |