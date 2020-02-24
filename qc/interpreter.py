from context import *
from program import *

class Interpreter:
    def __init__(self):
        self._loaded = []
        self._ctx = Context()

    def load(self, program: Program):
        self._loaded.append(program)

    def _run_func(self, func: Function, ctx: Context):
        for step in func.block():
            print(step)
            step.run(ctx)

    def run(self):
        try:
            for loaded in self._loaded:
                ep = loaded.entry_point()
                if ep:
                    self._run_func(loaded.idents()[ep], self._ctx)
                    break
            else:
                print('no starting point.')
                return
        except OutOfOettingerException:
            print('out of oettinger exception')
