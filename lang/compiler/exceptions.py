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


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def log_compiler_exception(e: CompilerException):
    ex_cls = e.__class__.__name__
    print(f"{RED}{ex_cls}: {e.error} at {e.filepath}:{e.line_number + 1}{RESET}")

