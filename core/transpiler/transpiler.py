from typing import List
from string import Template

from core.compiler.laxer import Token, TokenKind
from core.transpiler.templates import (
    FN_CALL_TPL,
    WRAPPER_TPL
)
from core.compiler.parser import (
    SyntaxTree, 
    Cond,
    FnCall
)


class Transpiler:
    def __init__(self, ast: SyntaxTree) -> None:
        self.ast = ast


    def fn_call(self, fn: FnCall):
        name = fn.name.value
        ret = FN_CALL_TPL.substitute(name=name, args=self.args(fn.args))
        return ret


    def args(self, args: List[Token]):
        ret = []
        for item in args:
            if item.kind == TokenKind.STRING_LITERAL:
                ret.append(f'"{item.value}"')
            else:
                raise ValueError(f'unexpected value kind {item}')
        return ','.join(ret)

    def compile(self):
        return WRAPPER_TPL.substitute(body=self._compile())

    def _compile(self):
        instructions = []
        for item in self.ast.expressions:
            if isinstance(item, FnCall):
                instructions.append(self.fn_call(item))
            else:
                raise ValueError("Expression is not supported")
        return '\n'.join(instructions)
