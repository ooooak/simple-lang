import logging
from dataclasses import dataclass
from typing import Union, List

from core.compiler.laxer import TokenKind, Laxer, Token
from core.peekable import Peekable

logger = logging.getLogger(__name__)

class SyntaxTree:
    pass

@dataclass
class Body(SyntaxTree):
    expressions: Union['FnCall', 'Cond']


@dataclass
class Binding(SyntaxTree):
    name: Token
    exp: [Token]

@dataclass
class Cond(SyntaxTree):
    pass


@dataclass
class FnCall(SyntaxTree):
    name: Token
    args: List[Token]



class Parser:
    def __init__(self, lexer: Peekable) -> None:
        self.lexer = lexer

    def parse(self):
        body = []

        while True:
            token = self.lexer.peek()
            if not token:
                 break

            next: Token = self.lexer.peek_next()

            if token.kind == TokenKind.KEYWORD:
                if next.value == '=':
                    body.append(self.binding())
                    continue
                elif next.value == '(':
                    body.append(self.fn_call())
                    continue
            logger.error('invalid token, %s', token)
            break

        return Body(body)

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
