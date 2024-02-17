import logging
from pprint import pprint

from core.compiler.reader import Reader
from core.compiler.laxer import Laxer
from core.compiler.parser import Parser

logger = logging.basicConfig(level=logging.INFO)


def main():
    r = Reader("./resources/main.s")
    l = Laxer(r)
    ast = Parser(l).parse()
    pprint(ast)

if __name__ == "__main__":
    main()