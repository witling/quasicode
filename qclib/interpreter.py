from .ast import *
from .context import *
from .program import *

class Interpreter:
    LIB_PATH = '/usr/local/lib/quasicode'

    def __init__(self):
        import os

        self._ctx = Context()
        self._ctx.add_include_path(Interpreter.LIB_PATH)
        self._ctx.add_include_path(os.getcwd())

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
            for loaded in self._ctx.loaded():
                ep = loaded.entry_point()
                if ep:
                    self._run_func(loaded[ep], self._ctx)
                    break
            else:
                print('no starting point.')
                return
        except OutOfOettingerException:
            print('out of oettinger exception')
