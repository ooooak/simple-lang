class CompilerException(Exception):
    def __init__(self, error: str, filepath: str, line_number: int, pos: int):
        self.error = error
        self.filepath = filepath
        self.line_number = line_number
        self.pos = pos
        super().__init__(error)


class LexerException(CompilerException):
    pass

class ParserException(CompilerException):
    pass


def log_compiler_exception(e: CompilerException):
    ex_cls = e.__class__.__name__

    print(f"{ex_cls} {e.filepath}:{e.line_number}:{e.pos}")
    print(e.message)

