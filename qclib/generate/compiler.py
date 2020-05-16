from ..ast import *
from ..program import *

from .error import CompilerError
from .parser import Parser

def unreachable():
    raise Exception('unexpected compiler state.')

def notimplemented():
    raise Exception('this feature is not yet implemented.')

def typeof(token):
    return token.data if hasattr(token, 'data') else token.type

def istype(token, name):
    return typeof(token) == name

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

    def _map_builtin_type(self, name):
        tymap = {
            'liste': Liste,
            'menge': Menge
        }
        if not name in tymap:
            return None
        return tymap[name]

    def _map_operator(self, name):
        # TODO: remove lower
        name = name.lower()
        tymap = {
            'add': Add,
            'sub': Sub,
            'mul': Mul,
            'div': Div,
            'mod': Mod,
            'lt' : Less,
            'cmp': Compare,
            'and': LogicalAnd,
            'or': LogicalOr,
            'not': LogicalNot,
        }
        if not name in tymap:
            return None
        return tymap[name]

    def _map_constant(self, name):
        tymap = {
            'uzbl': UzblConstant,
        }
        if not name in tymap:
            return None
        return tymap[name]

    def _to_access(self, item):
        assure_type(item, 'access')
        path = list(item.children)
        return Access(path)

    def _to_construct(self, item):
        assure_type(item, 'construct')
        assert 1 <= len(item.children)

        objty = item.children[0]
        assure_type(objty, 'objty')

        objty = self._map_builtin_type(objty.children[0].value)
        init = []

        if 2 == len(item.children):
            init = self._translate_construct_args(item.children[1])

        return Construct(objty, init)

    def _to_index(self, item):
        assure_type(item, 'index')
        assert len(item.children) == 2
        ident = self._to_value(item.children[0])
        index = self._to_value(item.children[1])
        return Index(ident, index)

    def _to_slice(self, item):
        assure_type(item, 'slice')
        assert len(item.children) == 1

        target, start, end = None, None, None 

        start_ast = list(item.find_data('slice_start'))
        end_ast = list(item.find_data('slice_end'))

        if start_ast:
            start_ast = start_ast[0]
            target = self._to_value(start_ast.children[0])
            start = self._to_value(start_ast.children[1])

        if end_ast:
            end_ast = end_ast[0]

            if target is None:
                target = self._to_value(end_ast.children[0])

            end = self._to_value(end_ast.children[1])

        return Slice(target, start=start, end=end)

    def _to_value(self, item):
        ty = typeof(item)
        if ty == 'IDENT':
            return Ident(item.value)
        elif ty == 'NUMBER':
            return Number(float(item.value))
        elif ty == 'STRING':
            val = item.value[1:-1]
            return String(val)
        elif ty == 'CONSTANT':
            const = self._map_constant(item)
            return const()
        elif ty == 'access':
            return self._to_access(item)
        elif ty == 'call':
            return self._translate_call(item)
        elif ty == 'construct':
            return self._to_construct(item)
        elif ty == 'expression':
            return self._translate_rexpression(item)
        elif ty == 'index':
            return self._to_index(item)
        elif ty == 'slice':
            return self._to_slice(item)
        elif ty == 'value':
            return self._to_value(item.children[0])
        elif not self._map_operator(ty) is None:
            return self._translate_operation(item)
        unreachable()

    def _translate_operation(self, item):
        ls = item.children
        opcls = self._map_operator(item.data)
        comp = opcls()
        
        if opcls is LogicalNot:
            assert len(ls) == 1
            arg = self._to_value(ls[0])
            comp.add_arg(arg)

        else:
            assert len(ls) == 2
            left, right = ls[0], ls[1]
            left, right = self._to_value(left), self._to_value(right)
            comp.add_arg(left)
            comp.add_arg(right)

        return comp

    def _translate_construct_args(self, item):
        assure_type(item, 'construct_args')
        return [self._to_value(arg) for arg in item.children]

    def _translate_wexpression(self, item):
        assure_type(item, 'wexpression')
        first = item.children[0]
        ty = typeof(first)

        if ty == 'IDENT' or ty == 'access':
            return self._to_value(first)
        elif ty == 'index':
            return self._to_index(first)
        elif ty == 'slice':
            return self._to_slice(first)
        #elif ty == 'slice_start':
        #    return self._to_slice_start(first)
        #elif ty == 'slice_end':
        #    return self._to_slice_end(first)

        unreachable()

    def _translate_rexpression(self, item):
        assure_type(item, 'expression')
        first = item.children[0]
        ty = typeof(first)

        if ty == 'call':
            return self._translate_call(first)
        elif ty == 'expression':
            return self._translate_rexpression(first)

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

    def _translate_declare(self, item):
        assure_type(item, 'declare')
        name = item.children[0]
        assure_ident(name)
        declaration = Declaration()
        declaration.set_name(Ident(name.value))

        it = iter(item.children[1:])
        # parse rest of declaration
        for item in it:
            ty = typeof(item)
            if ty == 'marker_main':
                declaration.add_marker(MainMarker())
            elif ty == 'declare_args':
                args = []
                for arg in item.children:
                    assure_ident(arg)
                    args.append(Ident(arg.value))
                declaration.set_args(args)
            elif ty == 'block':
                # parse block
                block = self._translate_block(item)
                declaration.set_block(block)
            else:
                unreachable()


        return declaration

    def _translate_import(self, item):
        assure_type(item, 'import')
        modname = item.children[0]
        assure_ident(modname)
        use = Use()
        use.add_arg(modname.value)
        return use

    def _translate_branch_elif(self, item):
        assure_type(item, 'elif_branch')
        assert len(item.children) == 2
        expr = self._translate_rexpression(item.children[0])
        block = self._translate_block(item.children[1])
        return expr, block

    def _translate_branch_else(self, item):
        assure_type(item, 'else_branch')
        assert len(item.children) == 1
        return self._translate_block(item.children[0])

    def _translate_branch(self, item):
        assure_type(item, 'if_branch')
        assert 2 <= len(item.children)
        branch = Branch()
        it = iter(item.children)

        expr = self._translate_rexpression(next(it))
        block = self._translate_block(next(it))
        branch.add_branch(expr, block)

        for item in it:
            ty = typeof(item)
            if ty == 'elif_branch':
                expr, block = self._translate_branch_elif(item)
                branch.add_branch(expr, block)
            elif ty == 'else_branch':
                block = self._translate_branch_else(item)
                branch.set_default_branch(block)
            else:
                unreachable()

        return branch

    def _translate_loop(self, item):
        assure_type(item, 'loop')
        assert len(item.children) == 1
        loop = Repeat()
        block = self._translate_block(item.children[0])
        loop.set_block(block)
        return loop

    def _translate_break(self, item):
        assure_type(item, 'break')
        return Break()

    def _translate_return(self, item):
        assure_type(item, 'return')
        assert len(item.children) == 1
        ret = Return()
        value = self._to_value(item.children[0])
        ret.add_arg(value)
        return ret

    def _translate_assign(self, item):
        # first is lhassign/rhassign, second is newline
        assure_type(item, 'assign')
        assert len(item.children) == 1
        item = item.children[0]

        # dereference to lhassign/rhassign
        assert len(item.children) == 2

        assign = Assign()
        wexpr, rexpr = None, None
        left, right = item.children[0], item.children[1]

        if item.data == 'lhassign':
            wexpr, rexpr = self._translate_wexpression(left), self._translate_rexpression(right)
        elif item.data == 'rhassign':
            wexpr, rexpr = self._translate_wexpression(right), self._translate_rexpression(left)
        else:
            unreachable()

        assign.set_ident(wexpr)
        assign.set_value(rexpr)

        return assign

    def _translate_call(self, item):
        assure_type(item, 'call')
        it = iter(item.children)

        name = next(it)
        assure_ident(name)

        try:
            args = next(it)
            assure_type(args, 'call_args')
            call_args = []
            for arg in args.children:
                if istype(arg, 'value'):
                    call_args.append(self._to_value(arg))
                elif istype(arg, 'access'):
                    call_args.append(self._to_access(arg))
                elif istype(arg, 'expression'):
                    call_args.append(self._translate_rexpression(arg))
                else:
                    unreachable()
            return FunctionCall(Ident(name.value), call_args)

        except StopIteration:
            pass

        return FunctionCall(Ident(name.value), [])

    def _translate_nop(self, item):
        assure_type(item, 'nop')
        return Nop()

    def _translate_debug(self, item):
        assure_type(item, 'debug')
        return Debug()

    def _translate_statement(self, statement):
        if istype(statement, 'statement'):
            assert len(statement.children) == 1
            statement = statement.children[0]

        ty = typeof(statement)

        if ty == 'import':
            return self._translate_import(statement)
        elif ty == 'declare':
            return self._translate_declare(statement)
        elif ty == 'if_branch':
            return self._translate_branch(statement)
        elif ty == 'loop':
            return self._translate_loop(statement)
        elif ty == 'break':
            return self._translate_break(statement)
        elif ty == 'return':
            return self._translate_return(statement)
        elif ty == 'assign':
            return self._translate_assign(statement)
        elif ty == 'expression':
            return self._translate_rexpression(statement)
        elif ty == 'nop':
            return self._translate_nop(statement)
        elif ty == 'debug':
            return self._translate_debug(statement)

        unreachable()

    def _translate(self, ast) -> Program:
        program = Program()

        toplevel = ast.children
        for statement in toplevel:
            item = self._translate_statement(statement)

            if isof(item, Declaration):
                if item.is_main():
                    if not program.entry_point() is None:
                        raise CompilerError('main entry point declared twice.')
                    program.set_entry_point(item.name())

                program.ident(item.name(), Function(item.args(), item.block()))

            elif isof(item, Use):
                assert len(item.args()) == 1
                program.use(item.args()[0])

            else:
                # TODO: allow other statements in certain modes
                raise CompilerError('statement `{}` is not allowed at top-level. only import and declare.'.format(item))

        return program
