import logging
from pathlib import Path
from typing import List

from lang.compiler.exceptions import ParserException
from lang.compiler.lexer import TokenKind, Token
from lang.compiler.reader import Reader

from pprint import pprint

logger = logging.getLogger(__name__)

def parser_exception(p, err):
    return ParserException(err, "p._filepath", 0, 0)



def scan_fn(lex: Reader):
    lex.get() # skip def

    method_name = lex.get()
    assert method_name.kind == TokenKind.IDENTIFIER

    token = lex.peek()
    print(token)
    assert token.kind == TokenKind.LEFT_PAREN

    args = scan_fn_args(lex)

    return_type = None
    if lex.peek().kind == TokenKind.IDENTIFIER:
        lex.get() # skip
        return_type = lex.peek() 


    assert lex.peek().kind == TokenKind.LEFT_BRACE
 
    block = scan_block(lex)

    return {
        "op": "def",
        "method_name": method_name.value,
        "args": args,
        "type": return_type,
        "body": block, 
    }


def scan_fn_args(lex: Reader):
    lex.get() # skip (

    args = []
    while True:
        arg_name = lex.get()
        arg_type = lex.get()

        assert arg_name.kind == arg_type.kind == TokenKind.IDENTIFIER
        args.append({
            "name": arg_name.value,
            "type": arg_type.value,
        })

        next: Token = lex.peek()
        if next.kind == TokenKind.COMMA:
            lex.get() # skip comma
            continue
        if next.kind == TokenKind.RIGHT_PAREN:
            lex.get() # skip )
            break
    return args

def scan_block(lex):
    lex.get()
    block_ast = []
    while True:
        c = lex.peek()
        if c.value == '}':
            # block ends here
            lex.get()
            break

        node = scan(lex)
        if not node:
            break

        block_ast.append(node)

    return {
        "op": "block",
        "body": block_ast
    }


def scan(lex):
    token: Token = lex.peek()
    if not token:
        return None
    
    if token.kind == TokenKind.FN_DEF:
        return scan_fn(lex)

    n = lex.peek_next()
    if token.kind == TokenKind.IDENTIFIER:
        if n.value == '=':
            return scan_binding(lex)
        if n.value == '(':
            return scan_fn_call(lex)


    # if token.value == ':':
    #     return self.parse_keyword()

    if token.value == "{":
        return scan_block(lex)
    v = lex.get()
    return v


def scan_binding(lex):
    name = lex.get()
    lex.get()

    tk: Token = lex.get()
    assert tk.kind == TokenKind.SCALAR_STRING

    return {
        "op": "binding",
        "name": name.value,
        "value": tk.value,
        "value_type": ""
    }, None

def scan_fn_call(lex):
    name = lex.get()

    # skip (
    lex.get()

    allowed = [
        TokenKind.IDENTIFIER,
        TokenKind.SCALAR_STRING
    ]

    arg = lex.get()
    if arg.kind not in allowed:
        raise parser_exception(None, f"invalid token in fn call {arg}")

    # skip symbol
    lex.get()
    return {
        "op": "fn_call",
        "name": name.value,
        "args": [{"value": arg.value, "kind": arg.kind}],
    }



def create_ast(tokens: List[Token], filepath: Path):

    lex = Reader(tokens)
    return {
        "source": filepath, 
        "program": [tok for tok in iter(lambda: scan(lex), None)]
    }
