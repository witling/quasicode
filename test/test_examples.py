import os
import pytest

from .deps import *

def patch_path(*args):
    return os.path.join(os.getcwd(), *args)

def load_source(fname):
    with open(fname, 'r') as src:
        return src.read()

class TestExamples(Test):
    def test_all(self):
        examples = os.listdir(patch_path('examples'))
        compiler = Compiler()
        ignore = ['bot.qc']

        for example in examples:
            if example in ignore:
                continue

            src_path = patch_path('examples', example)
            print('$', example)

            src = load_source(src_path)
            program = compiler.compile(src)

            interpreter = Interpreter()
            interpreter.disable_funny_mode()

            interpreter.load(program)
            interpreter.run()

            self.assertEqual(0, interpreter._ctx.exit_code())
