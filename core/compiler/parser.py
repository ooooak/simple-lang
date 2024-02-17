from dataclasses import dataclass
from typing import Union

from .laxer import TokenKind, Laxer, Token

class SyntaxTree:
    pass

@dataclass
class Body(SyntaxTree):
    expression: Union['FnCall', 'Cond']

@dataclass
class Cond(SyntaxTree):
    pass

@dataclass
class FnCall(SyntaxTree):
    name: Token
    args: list[Token]

class Parser:
    def __init__(self, lexer: Laxer) -> None:
        self.lexer = lexer

    def get(self):
        return self.lexer.token()

    def coll_args(self):
        pass
    
    def fn_call(self, tk: Token) -> FnCall:
        name = tk
        assert self.get().kind == TokenKind.SYMBOL
        val = self.get()
        return FnCall(name, [val])
        
        
    def parse(self):
        body = []
        token = self.get()
        if token.kind == TokenKind.KEYWORD:
            body.append(self.fn_call(token))
        return Body(body)