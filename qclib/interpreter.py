from .ast import *
from .ast.generic import isof
from .context import *
from .program import *

class Interpreter:
    LIB_PATH = '/usr/local/lib/quasicode'
    USERLIB_PATH = '~/.local/lib/quasicode'

    def __init__(self):
        import os

        self._ctx = Context()
        self._ctx.add_include_path(os.getcwd())
        self._ctx.add_include_path(os.path.expanduser(Interpreter.USERLIB_PATH))
        self._ctx.add_include_path(Interpreter.LIB_PATH)

    def disable_funny_mode(self):
        self._ctx.disable_funny_mode()

    def load(self, program: Program):
        self._ctx.load(program)

    def _run_func(self, func: Function, ctx: Context):
        last = None
        for step in func.block():
            last = step.run(ctx)
        return last

    def call(self, name: str, args: list=[]):
        args = [Value.create(arg) for arg in args]
        call = FunctionCall(Ident(name), args)
        return call.run(self._ctx)

    def run(self):
        try:
            for _, loaded in self._ctx.loaded().items():
                if not isof(loaded, Program):
                    continue
                ep = loaded.entry_point()
                if ep:
                    self._run_func(loaded[ep], self._ctx)
                    break
            else:
                raise Exception('no starting point')

        except Exception as e:
            import traceback
            self._ctx.set_exit_code(1)
            print(traceback.format_exc())
            print(e)
