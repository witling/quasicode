from ..const import *
from ..interpreter import Interpreter
from ..program import *
from ..stdlib import *

from .error import CompilerError
from .parser import Parser

from pylovm2 import Expr
import pylovm2

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

class CompileContext:
    def __init__(self, module_name):
        self.main_function = None
        if module_name:
            self.module = pylovm2.ModuleBuilder.named(module_name)
        else:
            self.module = pylovm2.ModuleBuilder()

class Compiler:
    def __init__(self):
        self._parser = Parser()
        self._compctx = None

    def parser(self):
        return self._parser

    def compile_file(self, fpath) -> Program:
        from os.path import abspath, basename, splitext
        fpath = abspath(fpath)
        name, _ = splitext(basename(fpath))
        with open(fpath, 'r') as fin:
            src = fin.read()
            return self.compile(src, auto_main=True, module_name=name, module_location=fpath)

    def compile(self, src, auto_main=False, module_name=None, module_location=None) -> Program:
        self._compctx = CompileContext(module_name)
        ast = self._parser.parse(src)
        module = self._translate(ast, auto_main, module_location)
        self._compctx = None
        return module

    def _map_builtin_type(self, name):
        tymap = {
            'liste': list,
            'menge': dict,
        }
        if not name in tymap:
            return None
        return tymap[name]

    def _map_operator(self, name):
        # TODO: remove lower
        name = name.lower()
        tymap = {
            'add': Expr.add,
            'sub': Expr.sub,
            'mul': Expr.mul,
            'div': Expr.div,
            'mod': Expr.rem,
            'lt' : Expr.lt,
            'cmp': Expr.eq,
            'and': Expr.land,
            'or': Expr.lor,
            'not': Expr.lnot,
            'pow': Expr.pow,
            'square': lambda x: Expr.pow(x, 2),
        }
        if not name in tymap:
            return None
        return tymap[name]

    def _map_constant(self, name):
        tymap = {
            'uzbl': True,
        }
        if not name in tymap:
            return None
        return tymap[name]

    def _to_access(self, item):
        def to_key(item):
            if typeof(item) == 'IDENT':
                return item.value
            return self._to_value(item)

        assure_type(item, 'access')
        args = item.children
        first, rest = self._to_value(args[0]), map(to_key, args[1:])
        return Expr.access(first, *rest)

    def _to_construct(self, item):
        assure_type(item, 'construct')
        assert 1 <= len(item.children)

        objty = item.children[0]
        assure_type(objty, 'objty')

        objty = self._map_builtin_type(objty.children[0].value)
        init = []

        if 2 == len(item.children):
            init = self._translate_construct_args(item.children[1])

        return Expr.val(objty(init))

    def _to_index(self, item):
        assure_type(item, 'index')
        assert len(item.children) == 2
        ident = self._to_value(item.children[0])
        index = self._to_value(item.children[1])
        return Expr.access(ident, index)

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

        return Expr.slice(target, start, end)

    def _to_value(self, item):
        ty = typeof(item)

        if ty == 'IDENT':
            if item.value[0] == '@':
                return Expr.call(item.value[1:])
            return Expr.var(item.value)
        elif ty == 'NUMBER':
            try:
                return Expr.val(int(item.value))
            except ValueError:
                return Expr.val(float(item.value))
        elif ty == 'STRING':
            val = item.value[1:-1]
            return Expr.val(val)
        elif ty == 'CONSTANT':
            const = self._map_constant(item)
            return Expr.val(const)
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
        name, ls = item.data, item.children
        opfunc = self._map_operator(name)
        args = []

        if name == 'not' or name == 'square':
            assert len(ls) == 1
            args = [self._to_value(ls[0])]

        else:
            assert len(ls) == 2

            left, right = ls[0], ls[1]
            left, right = self._to_value(left), self._to_value(right)
            
            if name == 'div':
                left = Expr.to_float(left)

            if name in ['and', 'or']:
                left, right = Expr.to_bool(left), Expr.to_bool(right)

            args = [left, right]
        
        return opfunc(*args)

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
        else:
            # TODO: implement slice assign
            todo()

    def _translate_rexpression(self, item):
        assure_type(item, 'expression')
        first = item.children[0]
        ty = typeof(first)

        if ty == 'call':
            return self._translate_call(first)
        elif ty == 'expression':
            return self._translate_rexpression(first)

        return self._to_value(first)

    def _translate_block(self, item, block):
        assure_type(item, 'block')

        for statement in item.children:
            # drop indents
            if hasattr(statement, 'type'):
                if statement.type == 'INDENT':
                    continue
                unreachable()

            self._translate_statement(statement, block)

    def _translate_declare(self, item):
        # which function do we use as our starting point? we have 
        # two different conditions to check for:
        #   m = functions name is pylovm2.ENTRY_POINT (or 'main')
        #   e = function is declared as entry point (has 'main_marker')
        #
        # this gives us four different permutations:
        #   m e   => _mf = block
        #   m !e  => forbidden state. assert !m or e
        #   !m e  => _mf = name, add block to module
        #   !m !e => add block to module
        #
        # at the end of compilation, we have to merge the entry()-block
        # together with a jump into the main code. according to above layout,
        # we have two distinct cases:
        #   type(_mf) == 'block' => merge _mf at end of entry()
        #   type(_mf) == 'str' => add call(name) to end of entry()

        assure_type(item, 'declare')
        name = item.children[0]
        assure_ident(name)

        it = iter(item.children[1:])

        block = pylovm2.ModuleBuilderSlot()

        main_marker = list(item.find_data('marker_main'))
        declare_args = list(item.find_data('declare_args'))
        statements = next(filter(lambda node: typeof(node) == 'block', item.children))

        assert name != pylovm2.ENTRY_POINT or main_marker 

        if declare_args:
            # main function does not have arguments
            assert not main_marker
            args = []
            for arg in declare_args[0].children:
                args.append(str(arg.value))
            block.args(args)

        if main_marker:
            if not self._compctx.main_function is None:
                raise CompilerError('main entry point declared twice.')

            # m e   => _mf = block
            if name == pylovm2.ENTRY_POINT:
                self._compctx.main_function = statements 
                return

            # !m e  => _mf = name, add block to module
            else:
                self._compctx.main_function = str(name)

        # !m !e => add block to module
        self._translate_block(statements, block.code())
        self._compctx.module.add_slot(name, block)

    def _translate_import(self, item, block, toplevel=False):
        assure_type(item, 'import')
        modname = item.children[0]
        assure_ident(modname)

        if toplevel:
            self._compctx.module.add_dependency(str(modname))
        else:
            block.load(Expr.val(str(modname)))

    def _translate_branch_elif(self, item, branch):
        assure_type(item, 'elif_branch')
        assert len(item.children) == 2
        expr = self._translate_rexpression(item.children[0])
        block = branch.add_condition(expr)
        self._translate_block(item.children[1], block)

    def _translate_branch_else(self, item, branch):
        assure_type(item, 'else_branch')
        assert len(item.children) == 1
        block = branch.default_condition()
        self._translate_block(item.children[0], block)

    def _translate_branch(self, item, block):
        assure_type(item, 'if_branch')
        assert 2 <= len(item.children)
        branch = block.branch()
        it = iter(item.children)

        expr = self._translate_rexpression(next(it))
        block = branch.add_condition(expr) 
        self._translate_block(next(it), block)

        for item in it:
            ty = typeof(item)
            if ty == 'elif_branch':
                self._translate_branch_elif(item, branch)
            elif ty == 'else_branch':
                self._translate_branch_else(item, branch)
            else:
                unreachable()

        return branch

    def _translate_loop(self, item, block):
        assure_type(item, 'loop')

        if len(item.children) == 2:
            condition, stmts = item.children[0], item.children[1]
            ty = typeof(condition) 
            condition = self._to_value(condition.children[0])

            if ty == 'loop_until':
                block = block.repeat_until(Expr.to_bool(condition))
            elif ty == 'loop_while':
                block = block.repeat_until(Expr.lnot(Expr.to_bool(condition)))
            else:
                unreachable()

        elif len(item.children) == 1:
            stmts = item.children[0]
            block = block.repeat()

        else:
            unreachable()

        self._translate_block(stmts, block)

    def _translate_break(self, item, block):
        assure_type(item, 'break')
        block.repeat_break()

    def _translate_return(self, item, block):
        assure_type(item, 'return')
        assert len(item.children) == 1
        value = self._to_value(item.children[0])
        block.ret(value)

    def _translate_assign(self, item, block, gscope=False):
        # first is lhassign/rhassign, second is newline
        assure_type(item, 'assign')
        assert len(item.children) == 1
        item = item.children[0]

        # dereference to lhassign/rhassign
        assert len(item.children) == 2

        wexpr, rexpr = None, None
        left, right = item.children[0], item.children[1]

        if item.data == 'lhassign':
            wexpr, rexpr = self._translate_wexpression(left), self._translate_rexpression(right)
        elif item.data == 'rhassign':
            wexpr, rexpr = self._translate_wexpression(right), self._translate_rexpression(left)
        else:
            unreachable()

        if wexpr.ty() == 'access':
            block.set(wexpr, rexpr)
        elif gscope:
            block.assign_global(wexpr, rexpr)
        else:
            block.assign(wexpr, rexpr)

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
                call_args.append(self._to_value(arg))

            return Expr.call(name, *call_args)

        except StopIteration:
            pass

        return Expr.call(name, [])

    def _translate_nop(self, item, block):
        assure_type(item, 'nop')

    def _translate_debug(self, item, block):
        assure_type(item, 'debug')
        block.interrupt(10)

    def _translate_statement(self, statement, block, toplevel=False):
        if istype(statement, 'statement'):
            assert len(statement.children) == 1
            statement = statement.children[0]

        ty = typeof(statement)

        if ty == 'import':
            return self._translate_import(statement, block, toplevel=toplevel)
        elif ty == 'declare':
            self._translate_declare(statement)
        elif ty == 'if_branch':
            self._translate_branch(statement, block)
        elif ty == 'loop':
            self._translate_loop(statement, block)
        elif ty == 'break':
            self._translate_break(statement, block)
        elif ty == 'return':
            self._translate_return(statement, block)
        elif ty == 'assign':
            # if there is a module, we are at top-level -> global assign
            self._translate_assign(statement, block, gscope=toplevel)
        elif ty == 'expression':
            inner = statement.children[0]
            name, ls = inner.data, inner.children
            if name == 'and' and istype(ls[1].children[0], 'IDENT'):
                arg = self._to_value(ls[0])
                block.ret(arg)
            else:
                try:
                    block.expr(self._translate_rexpression(statement))
                except RuntimeError:
                    raise CompilerError('cannot put expression on block level. remember the difference between `fun` (variable) and `@fun` (function call)')

        elif ty == 'nop':
            self._translate_nop(statement, block)
        elif ty == 'debug':
            self._translate_debug(statement, block)
        else:
            unreachable()

    def _translate(self, ast, auto_main, module_location=None) -> Program:
        entry_hir = self._compctx.module.entry().code()
        
        toplevel = ast.children
        for statement in toplevel:
            if typeof(statement) in ['assign', 'declare', 'import']:
                pass
            elif not auto_main:
                raise CompilerError('statement `{}` not expected at toplevel'.format(statement))

            self._translate_statement(statement, entry_hir, toplevel=True)

        # call into main function
        if self._compctx.main_function is None:
            pass
        elif type(self._compctx.main_function).__name__ == 'str':
            self._compctx.module.entry().code().call(self._compctx.main_function)
        else:
            self._translate_block(self._compctx.main_function, self._compctx.module.entry().code())

        module = self._compctx.module.build(module_location)
        return Library(module) if self._compctx.main_function is None else Program(module)
