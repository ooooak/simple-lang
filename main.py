import logging
from pprint import pprint


from core.log import setup_config, LOGGING_CONFIG
from core.compiler.laxer import Laxer
from core.compiler.parser import Parser
from core.transpiler.transpiler import Transpiler
from core.peekable import Peekable
from core.util import spit, read_file_char


setup_config(LOGGING_CONFIG)

def main():
    reader = Peekable(read_file_char("./resources/main.s"))
    lexer = Laxer(reader)
    
    ast = Parser(Peekable(lexer.tokens())).parse()
    pprint(ast)
    # output = Transpiler(ast).compile()
    # spit("./resources/main.go", output)
    
if __name__ == "__main__":
    main()
