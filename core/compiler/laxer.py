import logging
from dataclasses import dataclass
from enum import Enum, auto

from core.peekable import Peekable
from core.util import into_lookup_table, read_file_char


@dataclass(frozen=True)
class LaxerError:
    message: str
    file_path: str
    line_number: int
    pos: int
    

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
    def __init__(self, file_path: str):
        self.r = Peekable(read_file_char(file_path))
        self.file_path = file_path
        self.line_feed = 0

    def tokens(self):
        coll = []
        while True:
            token = self.token()
            if not token:
                break

            if isinstance(token, LaxerError):
                return [], token

            coll.append(token)
        return coll, None

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
            return self.err('single quotes are not supported')
        if b == ' ':
            self.r.get()
            return self.token()
        if b == '\n' :
            self.line_feed += 1
            self.r.get()
            return self.token()
        return self.err(f'unexpected value: {repr(b)}')

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
                return self.err('Unexpected EOF')
            if b == '"':
                break
            coll += b
        return Token(coll, TokenKind.STRING_LITERAL)

    def err(self, msg: str):
        return LaxerError(
            message=msg,
            line_number=self.line_feed + 1,
            file_path=self.file_path,
            pos=0
        )
