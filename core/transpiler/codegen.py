from core.compiler.parser import FnCall



class CodeGen:
    def __init__(self):
        self.output = []


    def pkg(self, name='main'):
        self.output.append(f"package {name}")


    def gen(self):
        '\n'.join(self.output)
