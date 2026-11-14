# KIRA Compiler Front End

CPT316 Assignment 1: lexer and parser for the KIRA language.

## Group Assignment

| Member | Matric No. | Role |
|---|---|---|
| Muhammad Irham bin Zainal | 23303996 | Lexer |
| Muhammad Hafizuddin bin Muhamad Husni | 23303563 | Parser for statements and blocks |
| Muhammad Aiman Hakim bin Kasman | 23304245 | Parser for expressions and AST display |
| Muhammad Naqqib bin Radzuan | 23302408 | Error handling and testing |

## Requirements

- Language: Python 3.12
- No external libraries needed

## How to run

```
python kira.py <file.kira>
```

To run the six public tests:

```
python kira.py tests/public1_arithmetic_if.kira
python kira.py tests/public2_while.kira
python kira.py tests/public3_nested_blocks.kira
python kira.py tests/public4_lexical_errors.kira
python kira.py tests/public5_syntax_error.kira
python kira.py tests/public6_syntax_end_of_input.kira
```

## Output

1. Token stream
2. Token counts
3. AST

If the lexer finds an error, the parser does not run.