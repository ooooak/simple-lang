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
        body = []
        while True:
            token = self.lexer.peek()
            if not token:
                break

            next = self.lexer.peek_next()
            if token.kind == TokenKind.KEYWORD:
                if next.value == '=':
                    body.append(self.binding())
                    continue
                elif next.value == '(':
                    body.append(self.fn_call())
                    continue

            if token.value == 'def':
                ex, err = self.parse_def()
                body.append(ex)
                
            logger.error('invalid token, %s', token)
            break

        return {
            "body": body
        }

    def fn_def(self):
        pass


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
            raise ValueError(f"invalid token in fn call {arg}")

        # skip symbol
        self.lexer.get()
        return {
            "op": "fn_call",
            "name": name.value,
            "args": [{"value": arg.value, "kind": arg.kind}],

            # "tokens": self.lexer.take(start, self.lexer.get_pos())
        }

    def coll_args(self):
        pass

    def binding(self):
        start = self.lexer.get_pos()
        name = self.lexer.get()

        # Skip binding op
        self.lexer.get()

        tk: Token = self.lexer.get()

        if tk.kind != TokenKind.STRING_LITERAL:
            raise ValueError("only strings are supported")

        return {
            "op": "binding",
            "name": name.value,
            "value": tk.value,
            "value_type": ""
            # "tokens": self.lexer.take(start, self.lexer.get_pos())
        }

    def parse_def(self):
        # skip def
        self.lexer.get()
        method_name = self.lexer.get()

        if method_name.kind is not TokenKind.KEYWORD:
            return 

        while True:
            method_name

        
    def err(self):
        pass