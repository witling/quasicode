#from more_itertools import peekable

from ..ast import *
from ..program import *

from .error import CompilerError
from .parser import Parser

def unreachable():
    raise Exception('unexpected compiler state.')

def notimplemented():
    raise Exception('this feature is not yet implemented.')

def istype(token, name):
    return token.data == name if hasattr(token, 'data') else token.type == name

def assure_type(token, name):
    assert istype(token, name)

assure_ident = lambda token: assure_type(token, 'IDENT')

class Compiler:
    def __init__(self):
        self._parser = Parser()

    def parser(self):
        return self._parser

    def compile(self, src):
        ast = self._parser.parse(src)
        return self._translate(ast)

    def _to_value(self, item):
        if istype(item, 'IDENT'):
            return Ident(item.value)
        elif istype(item, 'value'):
            return self._to_value(item.children[0])
        elif istype(item, 'expression'):
            return self._translate_rexpression(item)
        unreachable()

    def _translate_wexpression(self, item):
        assure_type(item, 'wexpression')
        first = item.children[0]

        if istype(first, 'IDENT'):
            return Ident(first.value)

        unreachable()

    def _translate_rexpression(self, item):
        assure_type(item, 'expression')
        first = item.children[0]
        return self._to_value(first)

    def _translate_block(self, item):
        assure_type(item, 'block')
        block = Block()
        for statement in item.children:
            # drop indents
            if hasattr(statement, 'type'):
                if statement.type == 'INDENT':
                    continue
                unreachable()

            result = self._translate_statement(statement)
            block.append(result)
        return block

    def _translate_declare(self, ls):
        name = ls[0]
        assure_ident(name)
        declaration = Declaration()
        declaration.set_name(Ident(name.value))

        it = iter(ls[1:])

        # parse rest of declaration
        for item in it:
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

        # parse block
        block = self._translate_block(next(it))

        return declaration

    def _translate_import(self, ls):
        modname = ls[0]
        assure_ident(modname)
        use = Use()
        use.add_arg(modname.value)
        return use

    def _translate_branch(self, ls):
        expr = self._translate_rexpression(ls[0])
        #block = self._translate_block()
        for item in ls[2:][0].children:
            print('>>>>', item)

    def _translate_loop(self, ls):
        notimplemented()

    def _translate_break(self, ls):
        notimplemented()

    def _translate_return(self, ls):
        notimplemented()

    def _translate_assign(self, item):
        # first is lhassign/rhassign, second is newline
        assure_type(item, 'assign')
        assert len(item.children) == 2
        item = item.children[0]

        # dereference to lhassign/rhassign
        assert len(item.children) == 2

        assign = Assign()
        wexpr, rexpr = None, None
        left, right = item.children[0], item.children[1]

        if item.data == 'lhassign':
            wexpr, rexpr = self._translate_wexpression(left), self._translate_rexpression(right)
        elif item.data == 'rhassign':
            rexpr, wexpr = self._translate_wexpression(left), self._translate_rexpression(right)
        else:
            unreachable()

        assign.set_ident(wexpr)
        assign.set_value(rexpr)

        return assign

    def _translate_call(self, ls):
        unreachable()

    def _translate_statement(self, statement):
        assure_type(statement, 'statement')
        ls = statement.children

        if not ls:
            return None

        first = ls[0]
        ty = first.data

        if ty == 'import':
            return self._translate_import(first.children)
        elif ty == 'declare':
            return self._translate_declare(first.children)
        elif ty == 'if_branch':
            return self._translate_branch(first.children)
        elif ty == 'loop':
            return self._translate_loop(first.children)
        elif ty == 'break':
            return self._translate_break(first.children)
        elif ty == 'return':
            return self._translate_return(first.children)
        elif ty == 'assign':
            return self._translate_assign(first)
        elif ty == 'call':
            return self._translate_call(first.children)

        unreachable()

    def _translate(self, ast) -> Program:
        program = Program()

        toplevel = ast.children
        for statement in toplevel:
            item = self._translate_statement(statement)

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
