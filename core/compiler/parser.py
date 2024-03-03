import logging

from typing import List
from dataclasses import dataclass

from core.compiler.laxer import TokenKind, Token
from core.peekable import Peekable


logger = logging.getLogger(__name__)

@dataclass
class ParserErr:
    message: str

class Parser:
    def __init__(self, lexer: List[Token]) -> None:
        self.lexer = Peekable(lexer)

    def parse(self):
        token = self.lexer.peek()
        if not token:
            return None, None

        next = self.lexer.peek_next()
        if token.kind == TokenKind.KEYWORD:
            if next.value == '=':
                return self.binding()
            if next.value == '(':
                return self.fn_call()

        if token.value == 'def':
            # parse function definition
            return self.parse_def()

        if token.value == ':':
            return self.parse_keyword()

        if token.value == "{":
            return self.parse_block()

        return None, self.err(f'unexpected token {token.value}')


    def parse_body(self):
        body = []
        while True:
            token, err = self.parse()
            if err:
                return None, err

            if not token:
                break

            body.append(token)

        return { "body": body }, None


    def fn_call(self):
        start = self.lexer.get_pos()
        name = self.lexer.get()

        # skip (
        self.lexer.get()

        allowed = [
            TokenKind.KEYWORD,
            TokenKind.STRING_LITERAL
        ]

        arg = self.lexer.get()
        if arg.kind not in allowed:
            return self.err(f"invalid token in fn call {arg}")

        # skip symbol
        self.lexer.get()
        return {
            "op": "fn_call",
            "name": name.value,
            "args": [{"value": arg.value, "kind": arg.kind}],
        }, None

    def coll_args(self):
        pass

    def binding(self):
        start = self.lexer.get_pos()
        name = self.lexer.get()

        # Skip binding op
        self.lexer.get()

        tk: Token = self.lexer.get()

        return {
            "op": "binding",
            "name": name.value,
            "value": tk.value,
            "value_type": ""
        }, None

    def parse_def(self):
        # skip def
        self.lexer.get()
        method_name = self.lexer.get()

        if method_name.kind != TokenKind.KEYWORD:
            return self.err("method name is not defined")

        # parse args
        p1 = self.lexer.get()
        p2 = self.lexer.get()

        if p1.value != '(':
            return self.err(f'invalid token {p1.value}')

        if p2.value != ')':
            return self.err(f'invalid token {p1.value}')

        return {
            "op": "def",
            "method_name": method_name,
            "args": [],
            "body": self.parse_block(),
        }, None

    def parse_block(self):
        block_start = self.lexer.get()

        if block_start.value != '{':
            self.err('unexpected start of block, expecting {')

        block_ast = []
        while True:
            c = self.lexer.peek()
            if c.value == '}':
                # block ends here
                self.lexer.get()
                break


            node, err = self.parse()
            # node, err = self.parse()
            if err:
                return None, err
            block_ast.append(node)

        return {
            "op": "block",
            "body": block_ast
        }, None
    

    def parse_keyword(self):
        pass

    def err(self, txt):
        return None, ParserErr(message=txt)
