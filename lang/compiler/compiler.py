from pprint import pprint
from pathlib import Path
from lang.compiler.exceptions import (
    CompilerException, 
    log_compiler_exception
)
from lang.compiler.lexer import Lexer
from lang.compiler.parser import create_ast

def log_tokens(tokens):
    for t in tokens:
        print(f"{t.kind} -> {repr(t.value)}")


def run_compile(filepath: Path):
    try:
        tokens = Lexer(filepath).tokens()
        ast = create_ast(tokens, filepath)
        pprint(ast)
        exit()
    except CompilerException as e:
        log_compiler_exception(e)

    # ast, err = Parser(tokens).parse_body()
    # if err:
    #     print(err)
    #     sys.exit()
    
    # pprint(ast)
    # output = Transpiler(ast).compile()
    # spit("./resources/main.go", output)
    
