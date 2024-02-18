import logging
from pprint import pprint


from core.log import setup_config, LOGGING_CONFIG
from core.compiler.reader import Reader
from core.compiler.laxer import Laxer
from core.compiler.parser import Parser
from core.transpiler.transpiler import Transpiler
from core.util import spit


setup_config(LOGGING_CONFIG)



def main():
    ast = Parser(Laxer(Reader("./resources/main.s"))).parse()
    output = Transpiler(ast).compile()
    spit("./resources/main.go", output)
    
if __name__ == "__main__":
    main()
