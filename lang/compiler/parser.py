import logging
from pathlib import Path
from typing import List

from lang.compiler.exceptions import ParserException
from lang.compiler.lexer import TokenKind, Token
from lang.compiler.reader import Reader


logger = logging.getLogger(__name__)



def parser_exception(err):
    return ParserException(err, "unk", 0, 0)

class Parser:
    """
    Converts tokens into an Abstract Syntax Tree (AST)
    """
    def __init__(self, tokens: List[Token], filepath: Path) -> None:
        self._lexer = Reader(tokens)
        self._filepath = filepath

    def create_ast(self):
        body = []
        while True:
            token = self.parse()
            if not token:
                break
            body.append(token)
        return { "source": self._filepath, "body": body }

    def parse(self):
        token = self._lexer.peek()
        if not token:
            return None

        n = self._lexer.peek_next()
        if token.kind == TokenKind.KEYWORD:
            if n.value == '=':
                return self.binding()
            if n.value == '(':
                return self.fn_call()

        if token.value == 'def':
            # parse function definition
            return self.parse_def()

        # if token.value == ':':
        #     return self.parse_keyword()

        if token.value == "{":
            return self.parse_block()

        logger.error('invalid token, %s', token)



    def fn_call(self):
        start = self._lexer.position
        name = self._lexer.get()

        # skip (
        self._lexer.get()

        allowed = [
            TokenKind.KEYWORD,
            TokenKind.STRING_LITERAL
        ]

        arg = self._lexer.get()
        if arg.kind not in allowed:
            raise parser_exception(f"invalid token in fn call {arg}")

        # skip symbol
        self._lexer.get()
        return {
            "op": "fn_call",
            "name": name.value,
            "args": [{"value": arg.value, "kind": arg.kind}],
        }, None

    def coll_args(self):
        pass

    def binding(self):
        start = self._lexer.position
        name = self._lexer.get()

        # Skip binding op
        self._lexer.get()

        tk: Token = self._lexer.get()

        if tk.kind != TokenKind.STRING_LITERAL:
            return parser_exception("only strings are supported")

        return {
            "op": "binding",
            "name": name.value,
            "value": tk.value,
            "value_type": ""
        }, None

    def parse_def(self):
        # skip def
        self._lexer.get()
        method_name = self._lexer.get()

        if method_name.kind != TokenKind.KEYWORD:
            return parser_exception("method name is not defined")

        # parse args
        p1 = self._lexer.get()
        p2 = self._lexer.get()

        if p1.value != '(':
            return parser_exception(f'invalid token {p1.value}')

        if p2.value != ')':
            return parser_exception(f'invalid token {p1.value}')

        return {
            "op": "def",
            "method_name": method_name,
            "args": [],
            "body": self.parse_block(),
        }

    def parse_block(self):
        block_start = self._lexer.get()

        if block_start.value != '{':
            parser_exception('unexpected start of block, expecting {')

        block_ast = []
        while True:
            c = self._lexer.peek()
            if c.value == '}':
                # block ends here
                self._lexer.get()
                break


            node = self.parse()
            if not node:
                break

            block_ast.append(node)

        return {
            "op": "block",
            "body": block_ast
        }
