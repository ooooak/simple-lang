import logging_setup

import sys
from pathlib import Path
from lang.compiler.compiler import run_compile

def cli_report_error(message: str):
    """
    Common method to display error message for cli
    
    :param message: Description
    :type message: str
    """
    print(f"Error: {message}")
    exit(1)

def main():
    args = sys.argv[1:]
    if len(args) <= 0:
        cli_report_error("source file is missing")

    run_compile(Path(args[0]))
    
if __name__ == "__main__":
    main()
