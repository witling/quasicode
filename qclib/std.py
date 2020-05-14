from .ast import *
from .function import *
from .library import *

import math
import random

class StdLibrary(PyLibrary):
    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('quasi', WriteFn())
        self.ident('bitte?', ReadFn())

    def modname(self):
        return 'std'

class ReadFn(Function):
    RESPONSES = ['verstehe.', 'gut.', 'okay.', 'perfekt.']

    def __init__(self):
        super().__init__([], Block())

    def __str__(self):
        return 'bitte?'

    def is_builtin(self):
        return True

    def block(self):
        return self

    def run(self, ctx):
        it = (value for _, value in ctx.locals().items())
        question = ' '.join(map(str, it))

        ctx.stdout().write(question)
        ctx.stdout().flush()

        ret = ctx.stdin().readline()
        # drop newline char
        ret = ret[:-1]

        if ctx.is_funny_mode():
            from random import choice
            ctx.stdout().write('{}\n'.format(choice(ReadFn.RESPONSES)))
            ctx.stdout().flush()

        return ret

class WriteFn(Function):
    def __init__(self):
        super().__init__([], Block())

    def __str__(self):
        return 'quasi'

    def is_builtin(self):
        return True

    def block(self):
        return self

    def run(self, ctx):
        it = (value for _, value in ctx.locals().items())
        msg = ' '.join(map(lambda x: str(x), it)) + '\n'
        ctx.stdout().write(msg)
        ctx.stdout().flush()
