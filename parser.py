from ast_printer import (
    node,
    syntax_error,
    KiraSyntaxError,
    parse_expr,   # <expr>  -> (Node, pos)
    parse_cond,   # <cond>  -> (Node, pos)
)


# Helpers
def is_keyword(tok, word):
    return tok.type == "KEYWORD" and tok.lexeme == word


def expect(tokens, pos, tok_type, shown):

    # Check that tokens[pos] has type tok_type.Then return pos + 1. 'shown' is how the missing token appears in the error message
    if tokens[pos].type != tok_type:
        raise syntax_error(tokens[pos], shown)
    return pos + 1


def let_in_block_error(tok):
    return KiraSyntaxError(
        f"SyntaxError at line {tok.line}, col {tok.col}: "
        f"'let' is only allowed at the top level, not inside a block"
    )



# Simple statements
def parse_decl(tokens, pos):
    """'let' id '=' expr ';'   ->  Let <name> / <expr>"""
    after_let = pos + 1                                  
    name_tok = tokens[after_let]
    after_id = expect(tokens, after_let, "IDENTIFIER", "an identifier")
    after_eq = expect(tokens, after_id, "ASSIGN", "'='")
    # hook: the expression parser fills in the value here
    value, after_expr = parse_expr(tokens, after_eq)
    # ----------------------------------------------------------------
    after_semi = expect(tokens, after_expr, "SEMICOLON", "';'")
    return node("Let", name_tok.lexeme, (value,)), after_semi


def parse_assign(tokens, pos):
    """id '=' expr ';'   ->  Assign <name> / <expr>"""
    name_tok = tokens[pos]
    after_eq = expect(tokens, pos + 1, "ASSIGN", "'='")

    # hook: the expression parser fills in the right-hand side here
    value, after_expr = parse_expr(tokens, after_eq)

    after_semi = expect(tokens, after_expr, "SEMICOLON", "';'")
    return node("Assign", name_tok.lexeme, (value,)), after_semi


def parse_print(tokens, pos):
    """'print' '(' expr ')' ';'   ->  Print / <expr>"""
    after_lp = expect(tokens, pos + 1, "LPAREN", "'('")
    
    # hook: the expression parser handles what goes inside print( )
    value, after_expr = parse_expr(tokens, after_lp)

    after_rp = expect(tokens, after_expr, "RPAREN", "')'")
    after_semi = expect(tokens, after_rp, "SEMICOLON", "';'")
    return node("Print", "", (value,)), after_semi


# Blocks, if, while
def parse_stmts_until_rbrace(tokens, pos, acc):
    #Collects statements until the closing '}' (the '}' itself is not consumed)
    # Using recursion here instead of a loop. acc holds the statements seen so far
    tok = tokens[pos]
    if tok.type == "RBRACE":
        return acc, pos
    if tok.type == "EOF":
        raise syntax_error(tok, "'}'")                    # block never closed
    stmt, after = parse_stmt(tokens, pos)                 # inside a block, let is not allowed
    return parse_stmts_until_rbrace(tokens, after, acc + (stmt,))


def parse_block(tokens, pos, label):
   #'{' stmt { stmt } '}'  ->  node named `label` (Then / Else / Body)"""
    after_lb = expect(tokens, pos, "LBRACE", "'{'")
    stmts, close_pos = parse_stmts_until_rbrace(tokens, after_lb, ())
    if len(stmts) == 0:                                   # an empty block is an error
        raise syntax_error(tokens[close_pos], "a statement")
    return node(label, "", stmts), close_pos + 1          # skip the '}'


def parse_else_part(tokens, pos):
    # Optional 'else' block. Returns tuple of 0 or 1 Else nodes, pos
    if is_keyword(tokens[pos], "else"):
        else_node, after = parse_block(tokens, pos + 1, "Else")
        return (else_node,), after
    return (), pos


def parse_if(tokens, pos):
    """'if' '(' cond ')' block [ 'else' block ]"""
    after_lp = expect(tokens, pos + 1, "LPAREN", "'('")

    # hook: the condition parser handles the if condition
    cond, after_cond = parse_cond(tokens, after_lp)

    after_rp = expect(tokens, after_cond, "RPAREN", "')'")
    then_node, after_then = parse_block(tokens, after_rp, "Then")
    else_nodes, after_else = parse_else_part(tokens, after_then)
    return node("If", "", (cond, then_node) + else_nodes), after_else


def parse_while(tokens, pos):
    """'while' '(' cond ')' block"""
    after_lp = expect(tokens, pos + 1, "LPAREN", "'('")

    # hook: the condition parser handles the while condition
    cond, after_cond = parse_cond(tokens, after_lp)

    after_rp = expect(tokens, after_cond, "RPAREN", "')'")
    body, after_body = parse_block(tokens, after_rp, "Body")
    return node("While", "", (cond, body)), after_body



# Statement dispatch. Used both at top level and inside blocks
def parse_stmt(tokens, pos):
    
    # Parses one statement. A 'let' is rejected here and only parse_item which runs at the top level will accepts declarations
    tok = tokens[pos]
    if is_keyword(tok, "let"):
        raise let_in_block_error(tok)
    if is_keyword(tok, "if"):
        return parse_if(tokens, pos)
    if is_keyword(tok, "while"):
        return parse_while(tokens, pos)
    if is_keyword(tok, "print"):
        return parse_print(tokens, pos)
    if tok.type == "IDENTIFIER":
        return parse_assign(tokens, pos)
    raise syntax_error(tok, "a statement")


# Top level
def parse_item(tokens, pos):
    """<item> -> <decl> | <stmt>   (top level only, so 'let' is allowed)"""
    if is_keyword(tokens[pos], "let"):
        return parse_decl(tokens, pos)
    return parse_stmt(tokens, pos)


def parse_items(tokens, pos, acc):
    """item { item } until EOF."""
    if tokens[pos].type == "EOF":
        return acc
    item, after = parse_item(tokens, pos)
    return parse_items(tokens, after, acc + (item,))


def parse_program(tokens):
    # Entry point. Takes the token list from tokenize() which will ends with EOF
    # Returns the Program node, or raises KiraSyntaxError at the first syntax error
     
    # empty file: nothing to parse
    if tokens[0].type == "EOF":                           
        raise syntax_error(tokens[0], "a statement")
    return node("Program", "", parse_items(tokens, 0, ()))
