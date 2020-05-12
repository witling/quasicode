#from more_itertools import peekable

from ..ast import *
from ..program import *

from .error import CompilerError
from .parser import Parser

def unreachable():
    raise Exception('unexpected compiler state.')

def assure_type(token, name):
    assert token.type == name

assure_ident = lambda token: assure_type(token, 'IDENT')

class Compiler:
    def __init__(self):
        self._parser = Parser()

    def parser(self):
        return self._parser

    def compile(self, src):
        ast = self._parser.parse(src)
        return self._translate(ast)

    def _translate_declare(self, ls):
        name = ls[0]
        assure_ident(name)
        declaration = Declaration()
        declaration.set_name(Ident(name.value))

        for item in iter(ls[1:]):
            ty = item.data if hasattr(item, 'data') else item.type
            if ty == 'NEWLINE':
                break
            elif ty == 'marker_main':
                declaration.add_marker(MainMarker)
            elif ty == 'declare_args':
                args = []
                for arg in item.children:
                    assure_ident(arg)
                    args.append(Ident(arg.value))
            else:
                unreachable()

        return declaration

    def _translate_import(self, ls):
        modname = ls[0]
        assure_ident(modname)
        use = Use()
        use.add_arg(modname.value)
        return use

    def _translate_statement(self, ls):
        if not ls:
            return None

        first = ls[0]
        ty = first.data

        if ty == 'import':
            return self._translate_import(first.children)
        elif ty == 'declare':
            return self._translate_declare(first.children)
        
        unreachable()

    def _translate(self, ast) -> Program:
        program = Program()

        toplevel = ast.children
        for statement in toplevel:
            assert statement.data == 'statement'
            item = self._translate_statement(statement.children)

            if isof(item, Declaration):
                if item.is_main():
                    if not program.entry_point() is None:
                        raise CompilerError('main entry point declared twice')

                program.ident(item.name(), Function(item.args(), item.block()))
            elif isof(item, Use):
                assert len(item.args()) == 1
                program.use(item.args()[0])
            else:
                unreachable()

        return program
    
    #def _finalize(self, parsed) -> Program:
    #    program = Program()
    #    for item in parsed:
    #        if isof(item, Declaration):
    #            if item.is_main():
    #                if not program.entry_point() is None:
    #                    raise CompilerError('main entry point declared twice')
    #                program.set_entry_point(item.name())
    #            program.ident(item.name(), Function(item.args(), item.block()))

    #        elif isof(item, Use):
    #            for arg in item.args():
    #                program.use(arg)

    #        else:
    #            raise CompilerError('unexpected `{}`. only declarations and imports are allowed at top-level.'.format(item))

    #    return program
