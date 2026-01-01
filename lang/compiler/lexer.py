from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum, auto

from lang.compiler.reader import Reader
from lang.utils import lookup_table, read_chars
from lang.compiler.exceptions import LexerException


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
    line_number: int
    start_pos: int
    end_pos: int


def is_latter(b):
    return 'A' <= b <= 'Z' or 'a' <= b <= 'z'

def lexer_exception(lex: 'Lexer', error: str):
    return LexerException(
        error=error,
        filepath=lex.file_path,
        line_number=lex.line_feed + 1,
        pos=lex.r.position
    )

class Lexer:
    """
    Converts source code into tokens
    """
    def __init__(self, file_path: Path):
        self.r = Reader(read_chars(file_path))
        self.file_path = file_path
        self.line_feed = 0

    def tokens(self):
        coll = []
        while True:
            token = self.token()
            if not token:
                break
            if isinstance(token, LexerException):
                return [], token

            coll.append(token)
        return coll

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

        raise lexer_exception(self, f'unexpected value: {repr(b)}')

    def keyword(self):
        coll = ""
        start_pos = self.r.position
        while True:
            b = self.r.get()
            if is_latter(b):
                coll += b
            else:
                self.r.undo_read()
                break
        return Token(coll, TokenKind.KEYWORD, self.line_feed, start_pos, self.r.position)

    def symbol(self):
        return Token(self.r.get(), TokenKind.SYMBOL, self.line_feed, self.r.position, self.r.position)

    def operator(self):
        return Token(self.r.get(), TokenKind.OPERATOR, self.line_feed, self.r.position, self.r.position)
    

    def string_literal(self, starting_quote: str):
        coll = ""
        start_pos = self.r.position
        self.r.get() # skip start
        while True:
            b = self.r.get()
            if not b:
                raise lexer_exception(self, 'Unexpected EOF')
            if b == starting_quote:
                break
            coll += b
        return Token(coll, TokenKind.STRING_LITERAL, self.line_feed, start_pos, self.r.position)

    def attr(self):
        start_pos = self.r.position
        coll = self.r.get()
        while True:
            b = self.r.get()
            if b in SPACE or b in LINE_FEED:
                self.r.undo_read()
                break
            coll += b
        return Token(coll, TokenKind.ATTR, self.line_feed, start_pos, self.r.position)

    def comment(self):
        pass
