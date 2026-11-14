"""AST node, expression parser and AST display for KIRA (Aiman's part).

Everything here is written in functional style: pure functions, immutable
data, recursion / reduce instead of loops, and no global variables.
Only print_ast and write_dot do I/O.
"""
from collections import namedtuple
from functools import reduce

# ======================================================================
# 1. AST node and syntax-error helper
# ======================================================================

Node = namedtuple("Node", ["kind", "value", "children"])


def node(kind, value="", children=()):
    """Build an immutable Node (children is always stored as a tuple)."""
    return Node(kind, value, tuple(children))


class KiraSyntaxError(Exception):
    """Carries a fully formatted message:
    'SyntaxError at line L, col C: ...' or 'SyntaxError at end of input: ...'
    """


def syntax_error(tok, expected):
    """Return a KiraSyntaxError for the token where parsing stopped."""
    if tok.type == "EOF":
        return KiraSyntaxError(f"SyntaxError at end of input: expected {expected}")
    return KiraSyntaxError(
        f"SyntaxError at line {tok.line}, col {tok.col}: "
        f"expected {expected} before '{tok.lexeme}'"
    )


# ======================================================================
# 2. Expression parser
# ======================================================================

ADD_OPS = ("+", "-")
MUL_OPS = ("*", "/", "%")


def parse_factor(tokens, pos):
    tok = tokens[pos]
    if tok.type == "IDENTIFIER":
        return node("Id", tok.lexeme), pos + 1
    if tok.type == "INTEGER":
        return node("Int", tok.lexeme), pos + 1
    if tok.type == "LPAREN":
        inner, after = parse_expr(tokens, pos + 1)
        if tokens[after].type != "RPAREN":
            raise syntax_error(tokens[after], "')'")
        return inner, after + 1
    raise syntax_error(tok, "an expression")


def _fold_tail(tokens, left, pos, ops, parse_operand):
    """{ op operand } : keep wrapping 'left' while the next token is in ops."""
    tok = tokens[pos]
    if tok.type == "ARITH_OP" and tok.lexeme in ops:
        right, after = parse_operand(tokens, pos + 1)
        return _fold_tail(tokens, node("BinOp", tok.lexeme, (left, right)),
                          after, ops, parse_operand)
    return left, pos


def parse_term(tokens, pos):
    first, after = parse_factor(tokens, pos)
    return _fold_tail(tokens, first, after, MUL_OPS, parse_factor)


def parse_expr(tokens, pos):
    first, after = parse_term(tokens, pos)
    return _fold_tail(tokens, first, after, ADD_OPS, parse_term)


def parse_cond(tokens, pos):
    left, after = parse_expr(tokens, pos)
    op = tokens[after]
    if op.type != "REL_OP":
        raise syntax_error(op, "a relational operator")
    right, end = parse_expr(tokens, after + 1)
    return node("RelOp", op.lexeme, (left, right)), end


# ======================================================================
# 3. AST display
# ======================================================================

def label(n):
    """Text of one node: 'Let x', 'BinOp +', 'Program'."""
    return n.kind if n.value == "" else f"{n.kind} {n.value}"


def tree_lines(n, depth=0):
    """Tuple of output lines for node n and all its descendants."""
    own = ("  " * depth + label(n),)
    below = tuple(line for c in n.children for line in tree_lines(c, depth + 1))
    return own + below


def format_ast(root):
    """The whole tree as one string (two spaces of indent per level)."""
    return "\n".join(tree_lines(root))


def print_ast(root):
    print(format_ast(root))


# ---------- Graphviz (optional, counts toward top band) ----------

def dot_nodes(n, nid):
    """Return (dot lines, next free id)."""
    own = (f'  n{nid} [label="{label(n)}"];',)

    def add_child(acc, child):
        lines, next_id = acc
        child_lines, after = dot_nodes(child, next_id)
        return (lines + (f"  n{nid} -> n{next_id};",) + child_lines, after)

    return reduce(add_child, n.children, (own, nid + 1))


def format_dot(root):
    lines, _ = dot_nodes(root, 0)
    return "digraph AST {\n  node [shape=box];\n" + "\n".join(lines) + "\n}\n"


def write_dot(root, path):
    """Write a .dot file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_dot(root))