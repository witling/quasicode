import os
import unittest

from deps import *

def patch_path(*args):
    return os.path.join(os.getcwd(), *args)

def load_source(fname):
    with open(fname, 'r') as src:
        return src.read()

class TestExamples(unittest.TestCase):
    def test_all(self):
        examples = os.listdir(patch_path('examples'))
        compiler = Compiler()

        for example in examples:
            src_path = patch_path('examples', example)
            src = load_source(src_path)
            program = compiler.compile(src)

            interpreter = Interpreter()
            interpreter.load(program)
            interpreter.run()
