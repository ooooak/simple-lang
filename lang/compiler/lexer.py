from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum, auto

from lang.compiler.reader import Reader
from lang.utils import read_chars
from lang.compiler.exceptions import LexerException

logger = logging.getLogger(__name__)

LINE_FEED = ['\n', '\r']
SPACE = [' ', '\t']
RESERVED_KEYWORDS=['if', 'else', 'var', 'const']
SYMBOLS = {
    '(': True,
    ')': True,
    '+': True,
    '-': True,
    '*': True,
    '/': True,
    '//': True,
    '%': True,
    '{': True,
    '}': True,
    '[': True,
    ']': True,
    ',': True,
    ':': True,
    '=': True,
}


class TokenKind(Enum):
    RESERVED_KEYWORD=auto()
    IDENTIFIER=auto()
    SYMBOL=auto()
    STRING_LITERAL=auto()
    COMMENT=auto()
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

def is_number(b):
    return '0' <= b <= '9'

def is_identifier_start(b):
    return is_latter(b) or b == "_"

def valid_identifier_continuation(b):
    # check if followup char is valid identifier continuation
    if b in LINE_FEED or b in SPACE:
        return False

    return is_latter(b) or b == "_" or is_number(b) 

def valid_string_continuation(b):
    # check if followup char is valid string continuation
    return b not in LINE_FEED




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
        return list(iter(self.token, None))

    def token(self):
        b = self.r.peek()
        if b is None:
            return None

        if b in SYMBOLS:
            return self.consume(TokenKind.RESERVED_KEYWORD, self.r.get())
        
        if is_identifier_start(b):
            keyword = self.keyword()
            if keyword in RESERVED_KEYWORDS:
                return self.consume(TokenKind.RESERVED_KEYWORD, keyword)
            return self.consume(TokenKind.IDENTIFIER, keyword)
        
        if b == "#":
            return self.comment()

        if b == '"':
            return self.string()
 
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
        while True:
            b = self.r.get()
            if valid_identifier_continuation(b):
                coll += b
            else:
                self.r.undo_read()
                break
        return coll
    
    def string(self):
        self.r.get() # skip start
        coll = ""
        while True:
            b = self.r.get()
            if not b:
                raise lexer_exception(self, 'unexpected eof while parsing string literal')

            if b == '"':
                break
        
            if valid_string_continuation(b):
                coll += b
        return self.consume(TokenKind.STRING_LITERAL, coll)

    def comment(self):
        coll = ""
        while b := self.r.get():
            coll += b
            if b in LINE_FEED:
                break
        return self.consume(TokenKind.COMMENT, coll)

    def consume(self, kind: TokenKind, value: str):
        """
        Consume single value quickly, to avoid code repetition
        """
        return Token(
            value,
            kind,
            self.line_feed, 
            self.r.position, 
            self.r.position
        )