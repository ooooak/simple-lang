import logging
from dataclasses import dataclass
from enum import Enum, auto

from lang.compiler.reader import Reader
from lang.utils import lookup_table, read_file_char
from lang.exceptions import LexerError


logger = logging.getLogger(__name__)

OPERATORS = ['=']
SYMBOLS=lookup_table('(',')', '{', '}', '[', ']')
RESERVED_KEYWORDS=['if', 'else']

LINE_FEED = ['\n', '\r']
SPACE = [' ', '\t', ',']

class TokenKind(Enum):
    ATTR=auto()
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

class Lexer:
    def __init__(self, file_path: str):
        self.r = Reader(read_file_char(file_path))
        self.file_path = file_path
        self.line_feed = 0

    def tokens(self):
        coll = []
        while True:
            token = self.token()
            if not token:
                break
            if isinstance(token, LexerError):
                return [], token

            coll.append(token)
        return coll, None

    def token(self):
        b = self.r.peek()
        if not b:
            return None
        if is_latter(b):
            return self.keyword()
        if b in SYMBOLS:
            return self.symbol()
        if b in OPERATORS:
            return self.operator()
        if b == ':':
            return self.attr()
        if b == '"' or b == "'":
            return self.string_literal(b)
            
        if b == '/' and self.r.peek_next() == '/':
            self.comment()
        if b in SPACE:
            self.r.get()
            return self.token()
        if b in LINE_FEED:
            self.line_feed += 1
            self.r.get()
            return self.token()

        return self.err(f'unexpected value: {repr(b)}')

    def keyword(self):
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

    def string_literal(self, starting_quote: str):
        coll = ""
        self.r.get() # skip start
        while True:
            b = self.r.get()
            if not b:
                return self.err('Unexpected EOF')
            if b == starting_quote:
                break
            coll += b
        return Token(coll, TokenKind.STRING_LITERAL)

    def attr(self):
        coll = self.r.get()
        while True:
            b = self.r.get()
            if b in SPACE or b in LINE_FEED:
                self.r.undo_read()
                break
            coll += b
        return Token(coll, TokenKind.ATTR)

    def comment(self):
        pass

    def err(self, msg: str):
        return LexerError(
            message=msg,
            line_number=self.line_feed + 1,
            file_path=self.file_path,
            pos=0
        )
