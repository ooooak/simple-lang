import logging
from dataclasses import dataclass
from typing import Union, List

from core.compiler.laxer import TokenKind, Laxer, Token

logger = logging.getLogger(__name__)

class SyntaxTree:
    pass

@dataclass
class Body(SyntaxTree):
    expressions: Union['FnCall', 'Cond']

@dataclass
class Cond(SyntaxTree):
    pass

@dataclass
class FnCall(SyntaxTree):
    name: Token
    args: List[Token]

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

        logger.debug("Token: %s", Token)
        if token.kind == TokenKind.KEYWORD:
            body.append(self.fn_call(token))
        else:
            logger.error('invalid token, %s', token)

        return Body(body)
