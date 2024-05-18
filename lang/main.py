from pprint import pprint
import sys

from lang.log import setup_config, LOGGING_CONFIG
from lang.compiler import Lexer, Parser, Reader
from lang.transpiler.transpiler import Transpiler

from lang.utils import spit, read_file_char


setup_config(LOGGING_CONFIG)


def handle_error(err):
    print(f"{err.file_path}:{err.line_number}: {err.message}")
    exit()


def main():
    tokens, err = Lexer('./resources/main.s').tokens()
    if err:
        handle_error(err)

    pprint(tokens)
    exit()
    ast, err = Parser(tokens).parse_body()
    if err:
        print(err)
        sys.exit()
    
    pprint(ast)
    # output = Transpiler(ast).compile()
    # spit("./resources/main.go", output)
    
if __name__ == "__main__":
    main()
