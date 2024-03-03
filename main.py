import logging
from pprint import pprint
import sys
import json


from core.log import setup_config, LOGGING_CONFIG
from core.compiler.laxer import Laxer, LaxerError
from core.compiler.parser import Parser
from core.transpiler.transpiler import Transpiler
from core.peekable import Peekable
from core.util import spit, read_file_char


setup_config(LOGGING_CONFIG)


def handle_error(err: LaxerError):
    print(f"{err.file_path}:{err.line_number}: {err.message}")
    exit()


def main():
    tokens, err = Laxer('./resources/main.s').tokens()
    if err:
        handle_error(err)

    # pprint(tokens)
    # exit()
    ast, err = Parser(tokens).parse_body()
    if err:
        print(err)
        sys.exit()
    
    pprint(ast)
    # output = Transpiler(ast).compile()
    # spit("./resources/main.go", output)
    
if __name__ == "__main__":
    main()
