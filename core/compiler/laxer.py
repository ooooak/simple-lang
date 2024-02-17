from dataclasses import dataclass
from enum import Enum, auto

from core.compiler.reader import Reader
from core.util import (
    into_lookup_tbl,
    map_has
)

# dentifiers, keywords, literals, operators

SYMBOLS=into_lookup_tbl('(',')', '{', '}', '[', ']')

class TokenKind(Enum):
    KEYWORD=auto()
    SYMBOL=auto()
    STRING_LITERAL=auto()

@dataclass(frozen=True)
class Token:
    value: str
    kind: TokenKind

def is_latter(b):
    return 'A' <= b <= 'Z' or 'a' <= b <= 'z'

class Laxer:
    def __init__(self, r: Reader):
        self.r = r
        
    def token(self):
        b = self.r.peek()
        if not b:
            return None
        if is_latter(b):
            return self.keyword_latter()
        if map_has(SYMBOLS, b):
            return self.symbol()
        if b == '"':
            return self.string_literal()
            

    def keyword_latter(self):
        coll = ""
        while True:
            b = self.r.get()
            if is_latter(b):
                coll += b
            else:
                self.r.undo()
                break
        return Token(coll, TokenKind.KEYWORD)

    def symbol(self):
        return Token(self.r.get(), TokenKind.SYMBOL)

    def string_literal(self):
        coll = ""
        self.r.get() # skip "
        
        while True:
            b = self.r.get()
            if not b:
                raise Exception("Unexpected EOF")
            if b == '"':
                break
            coll += b
        return Token(coll, TokenKind.STRING_LITERAL)

    def tokens(self):
        ret = []
        for t in self.token():
            ret.append(t)
        return ret