from ..ast import *
from ..program import *

from .error import CompilerError
from .parser import Parser

class Compiler:
    def __init__(self):
        self._parser = Parser()

    def parser(self):
        return self._parser

    def compile(self, src):
        parsed = self._parser.parse(src)
        return self._finalize(parsed)
    
    def _finalize(self, parsed) -> Program:
        program = Program()
        for item in parsed:
            if isof(item, Declaration):
                if item.is_main():
                    if not program.entry_point() is None:
                        raise CompilerError('main entry point declared twice')
                    program.set_entry_point(item.name())
                program.ident(item.name(), Function(item.args(), item.block()))

            elif isof(item, Use):
                for arg in item.args():
                    program.use(arg)

            else:
                raise CompilerError('unexpected `{}`. only declarations and imports are allowed at top-level.'.format(item))

        return program
