from ast import *
from .parser import Parser
from program import *

class Compiler:
    def __init__(self):
        self._parser = Parser()

    def compile(self, src):
        parsed = self._parser.parse(src)
        return self._finalize(parsed)
    
    def _finalize(self, parsed) -> Program:
        program = Program()
        for item in parsed:
            if isof(item, Declaration):
                if item.is_main():
                    program.set_entry_point(item.name())
                program.ident(item.name(), Function(item.args(), item.block()))

            elif isof(item, Use):
                for arg in item.args():
                    program.use(arg)

        return program
