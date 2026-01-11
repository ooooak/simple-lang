from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum, auto

from lang.compiler.reader import Reader
from lang.utils import read_chars
from lang.compiler.exceptions import LexerException
from lang.config import DEBUG_LEXER

logger = logging.getLogger(__name__)


class TokenKind(Enum):
    """
    Base Token Kinds
    """

    # Identifiers & Scalar
    IDENTIFIER = auto() # x, totalSum, myVar
    SCALAR_NUMBER = auto() # 10, 3.14, 42
    SCALAR_FLOAT = auto()
    SCALAR_STRING = auto() # "hello"
    SCALAR_CHAR = auto() # 'hello'


    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    VAR = auto()
    CONST = auto()
    FN_DEF = auto()

    # Operators
    OP_PLUS = auto() # +
    OP_MINUS = auto() # -
    OP_STAR = auto() # *
    OP_SLASH = auto() # /
    OP_EQUAL = auto() # =
    OP_EQUAL_EQUAL = auto() # ==
    OP_BANG_EQUAL = auto() # !=
    OP_PERCENT = auto() # %

    # Comparison
    # OP_EQUAL_EQUAL = auto()     # ==
    # OP_BANG_EQUAL = auto()      # !=
    # OP_LESS = auto()            # <
    # OP_LESS_EQUAL = auto()      # <=
    # OP_GREATER = auto()         # >
    # OP_GREATER_EQUAL = auto()   # >=

    # Logical
    # OP_AND = auto()             # and / &&
    # OP_OR = auto()              # or  / ||
    # OP_NOT = auto()             # not / !

    # # Unary / Increment (if supported)
    # OP_PLUS_PLUS = auto()       # ++
    # OP_MINUS_MINUS = auto()     # --

    # # Bitwise (optional but common)
    # OP_BIT_AND = auto()         # &
    # OP_BIT_OR = auto()          # |
    # OP_BIT_XOR = auto()         # ^
    # OP_BIT_NOT = auto()         # ~
    # OP_SHIFT_LEFT = auto()      # <<
    # OP_SHIFT_RIGHT = auto()     # >>


    # Delimiters
    LEFT_PAREN = auto() # (
    RIGHT_PAREN = auto() # )
    LEFT_BRACE = auto() # {
    RIGHT_BRACE = auto() # }
    LEFT_BRACKET = auto() # [
    RIGHT_BRACKET = auto() # ]
    COMMA = auto() # ,
    DOT = auto() # .
    SEMICOLON = auto()

    COMMENT = auto() # # comment
    EOF = auto()

LINE_FEED = ['\n', '\r']
SPACE = [' ', '\t']

RESERVED_KEYWORDS={
    'if': TokenKind.IF,
    'else': TokenKind.ELSE,
    'var': TokenKind.VAR,
    'const': TokenKind.CONST,
    'def': TokenKind.FN_DEF,
}

SINGULAR_TOKEN_MAPPINGS = {
    '(': TokenKind.LEFT_PAREN,
    ')': TokenKind.RIGHT_PAREN,
    '+': TokenKind.OP_PLUS,
    '-': TokenKind.OP_MINUS,
    '*': TokenKind.OP_STAR,
    '/': TokenKind.OP_SLASH,
    '%': TokenKind.OP_PERCENT,
    '{': TokenKind.LEFT_BRACE,
    '}': TokenKind.RIGHT_BRACE,
    '[': TokenKind.LEFT_BRACKET,
    ']': TokenKind.RIGHT_BRACKET,
    ',': TokenKind.COMMA,
    '.': TokenKind.DOT,
    '=': TokenKind.OP_EQUAL,
    ';': TokenKind.SEMICOLON,
}

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
        """
        create list of tokens
        """
        return list(iter(self.start_scanner, None))

    def start_scanner(self):
        """
        Start Scanning for tokens
        """""
        b = self.r.peek()
        if DEBUG_LEXER:
            logger.info(
                "b (%s) in SINGULAR_TOKEN_MAPPINGS: %s",
                repr(b),
                b in SINGULAR_TOKEN_MAPPINGS
            )

        match b:
            case None:
                return None

            case _ if b in SINGULAR_TOKEN_MAPPINGS:
                kind = SINGULAR_TOKEN_MAPPINGS[b]
                return self.consume(kind, self.r.get())

            case _ if is_identifier_start(b):
                val = self._scan_identifier_value()
                if val in RESERVED_KEYWORDS:
                    kind = RESERVED_KEYWORDS[val]
                    return self.consume(kind, val)
                return self.consume(TokenKind.IDENTIFIER, val)

            case "#":
                return self._scan_comment()

            case _ if is_number(b):
                return self._scan_number()

            case '"':
                return self._scan_string()

            case _ if b in SPACE:
                self.r.get()
                return self.start_scanner()

            case _ if b in LINE_FEED:
                self.line_feed += 1
                self.r.get()
                return self.start_scanner()

        raise lexer_exception(self, f'unexpected value: {repr(b)}')

    def _scan_identifier_value(self):
        coll = ""
        while True:
            b = self.r.get()
            if valid_identifier_continuation(b):
                coll += b
            else:
                self.r.undo_read()
                break
        return coll
    
    def _scan_string(self):
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
        return self.consume(TokenKind.SCALAR_STRING, coll)

    def _scan_comment(self):
        coll = ""
        while b := self.r.get():
            coll += b
            if b in LINE_FEED:
                break
        return self.consume(TokenKind.COMMENT, coll)


    def _scan_number(self):
        coll = ""
        while True:
            b = self.r.get()
            if not b:
                raise lexer_exception(self, 'unexpected eof while parsing string literal')

            if is_number(b):
                coll += b
                continue
            self.r.undo_read()
            break

        return self.consume(TokenKind.SCALAR_NUMBER, coll)

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