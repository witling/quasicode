import io
import os
import pytest

from .deps import *

def patch_path(*args):
    return os.path.join(os.getcwd(), *args)

def load_source(fname):
    with open(fname, 'r') as src:
        return src.read()

class TestExamples(Test):
    def test_all(self, internals):
        internals.interpreter._ctx.set_stdin(io.StringIO())

        examples = os.listdir(patch_path('examples'))
        ignore = ['bot.qc']

        for example in examples:
            src_path = patch_path('examples', example)

            if example in ignore or os.path.isdir(src_path):
                continue

            print('$', example)

            src = load_source(src_path)
            program = internals.compiler.compile(src)

            internals.interpreter.disable_funny_mode()

            internals.interpreter.load(program)
            internals.interpreter.run()

            self.assertEqual(0, internals.interpreter._ctx.exit_code())
