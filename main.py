import logging

from core.compiler.reader import Reader
from core.compiler.laxer import Laxer

logger = logging.basicConfig(level=logging.INFO)


def main():
    r = Reader("./resources/main.s")
    l = Laxer(r)
    
    while True:
        token = l.token()
        if not token:
            break
        
        print(token)

if __name__ == "__main__":
    main()