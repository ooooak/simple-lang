import logging
from dataclasses import dataclass
from enum import Enum, auto

from core.peekable import Peekable
from core.util import into_lookup_table

logger = logging.getLogger(__name__)

# dentifiers, keywords, literals, operators

OPERATORS = ['=']
SYMBOLS=into_lookup_table('(',')', '{', '}', '[', ']')
RESERVED_KEYWORDS=['if', 'else']

class TokenKind(Enum):
    KEYWORD=auto()
    SYMBOL=auto()
    STRING_LITERAL=auto()
    OPERATOR=auto()

@dataclass(frozen=True)
class Token:
    value: str
    kind: TokenKind

def is_latter(b):
    return 'A' <= b <= 'Z' or 'a' <= b <= 'z'

class Laxer:
    def __init__(self, r: Peekable):
        self.r = r
        self.line_feed = 0

    def tokens(self):
        coll = []
        while True:
            token = self.token()
            if not token:
                break
            coll.append(token)
        return coll

    def token(self):
        b = self.r.peek()
        if not b:
            return None
        if is_latter(b):
            return self.keyword_latter()
        if b in SYMBOLS:
            return self.symbol()
        if b in OPERATORS:
            return self.operator()
        if b == '"':
            return self.string_literal()
        if b == "'":
            raise ValueError("single quotes are not supported")
        if b == ' ':
            self.r.get()
            return self.token()
        if b == '\n' :
            self.line_feed += 1
            self.r.get()
            return self.token()

        raise ValueError(f'unexpected value: {repr(b)}')

    def keyword_latter(self):
        coll = ""
        while True:
            b = self.r.get()
            if is_latter(b):
                coll += b
            else:
                self.r.undo_read()
                break
        return Token(coll, TokenKind.KEYWORD)

    def symbol(self):
        return Token(self.r.get(), TokenKind.SYMBOL)

    def operator(self):
        return Token(self.r.get(), TokenKind.OPERATOR)

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
