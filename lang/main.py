from lang.utils.common import cli_report_error
from lang.error.messages import CLI_MISSING_FILE_ARGUMENT

import sys
from pprint import pprint
from lang.compiler.lexer import Lexer
from lang.compiler.parser import Parser
from lang.transpiler.transpiler import Transpiler
from lang.utils import spit, read_file_char


def handle_error(err):
    print(f"{err.file_path}:{err.line_number}: {err.message}")
    exit()




def main():
    args = sys.argv[1:]
    if len(args) <= 0:
        cli_report_error(CLI_MISSING_FILE_ARGUMENT)

    exit()
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
