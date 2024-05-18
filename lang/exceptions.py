from dataclasses import dataclass

@dataclass(frozen=True)
class LexerError(Exception):
    message: str
    file_path: str
    line_number: int
    pos: int

    def __str__(self):
        return f"LexerError: {self.message} in {self.file_path}, \
        line {self.line_number}, position {self.pos}"