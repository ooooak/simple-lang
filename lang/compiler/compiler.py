from pprint import pprint
from pathlib import Path
from lang.compiler.exceptions import (
    CompilerException, 
    log_compiler_exception
)
from lang.compiler.lexer import Lexer
from lang.compiler.parser import Parser
# from lang.transpiler.transpiler import Transpiler
# from lang.utils import spit, read_file_char


def run_compile(filepath: Path):
    try:
        tokens = Lexer(filepath).tokens()
        ast = Parser(tokens, filepath).create_ast()
        pprint(ast)
    except CompilerException as e:
        log_compiler_exception(e)

    # ast, err = Parser(tokens).parse_body()
    # if err:
    #     print(err)
    #     sys.exit()
    
    # pprint(ast)
    # output = Transpiler(ast).compile()
    # spit("./resources/main.go", output)
    
