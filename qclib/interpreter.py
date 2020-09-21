from .ast import *
from .ast.generic import isof
from .context import *
from .program import *
from .std import StdLibrary

import pylovm2

class Interpreter:
    LIB_PATH = '/usr/local/lib/quasicode'
    USERLIB_PATH = '~/.local/lib/quasicode'

    def __init__(self, restricted=False):
        import os

        self._ctx = Context() if not restricted else RestrictedContext()
        self._ctx.add_include_path(os.getcwd())
        self._ctx.add_include_path(os.path.expanduser(Interpreter.USERLIB_PATH))
        self._ctx.add_include_path(Interpreter.LIB_PATH)

        self._vm = pylovm2.Vm()

        #self._ctx.load(StdLibrary())

    def _run_func(self, func: Function, ctx: Context):
        last = None
        for step in func.block():
            last = step.run(ctx)
        return last

    def disable_funny_mode(self):
        self._ctx.disable_funny_mode()

    def load(self, program: Program):
        self._vm.load(program._module)
        #self._ctx.load(program)

    def call(self, name: str, *args):
        return self._vm.call(name, *args)
        #def to_quasi_value(val):
        #    if val.__class__ is Ident:
        #        return val
        #    return Value.create(val)
        #args = [to_quasi_value(arg) for arg in args]
        #call = FunctionCall(Ident(name), args)
        #return call.run(self._ctx)

    def run(self):
        self._vm.run()
        #try:
        #    for _, loaded in self._ctx.loaded().items():
        #        if not isof(loaded, Program):
        #            continue
        #        ep = loaded.entry_point()
        #        if ep:
        #            self._run_func(loaded[ep], self._ctx)
        #            break
        #    else:
        #        raise Exception('no starting point')

        #except Exception as e:
        #    import traceback
        #    self._ctx.set_exit_code(1)
        #    print(traceback.format_exc())
        #    print(e)

        #    self._ctx.last_error = e

        #return self._ctx.exit_code()
