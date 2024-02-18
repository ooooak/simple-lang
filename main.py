import logging
from pprint import pprint


from core.log import setup_config, LOGGING_CONFIG
from core.compiler.reader import Reader
from core.compiler.laxer import Laxer
from core.compiler.parser import Parser
from core.transpiler.transpiler import Transpiler
from core.util import spit


setup_config(LOGGING_CONFIG)

def dump_lexer(l: Laxer):
    while True:
        token = l.token()
        if not token:
            break
        print(token)



def main():
    reader = Reader("./resources/main.s")
    lexer = Laxer(reader)
    dump_lexer(lexer)
    exit()
    ast = Parser(lexer).parse()
    return ast
    output = Transpiler(ast).compile()
    spit("./resources/main.go", output)
    
if __name__ == "__main__":
    main()
