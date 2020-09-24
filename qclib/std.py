from .ast import *
from .error import AssertException
from .function import *
from .library import *

import math
import random

class StdLibrary(Library):
    RESPONSES = ['verstehe.', 'gut.', 'okay.', 'perfekt.']

    def __init__(self, ctx):
        self._ctx = ctx

        module = pylovm2.ModuleBuilder()
        module.add('assert').pyfn(self._assert)
        module.add('bitte?').pyfn(self._bitte)
        module.add('quasi').pyfn(self._quasi)

        super().__init__(module.build())

    def _assert(self, *args):
        assert args[0]

    def _bitte(self, *args):
        question = ' '.join(map(str, args))

        self._ctx.stdout().write(question)
        self._ctx.stdout().flush()

        ret = self._ctx.stdin().readline()
        # drop newline char
        ret = ret[:-1]

        if self._ctx.is_funny_mode():
            from random import choice
            self._ctx.stdout().write('{}\n'.format(choice(Library.RESPONSES)))
            self._ctx.stdout().flush()

        return ret

    def _quasi(self, *args):
        msg = ' '.join(map(str, args)) + '\n'
        self._ctx.stdout().write(msg)
        self._ctx.stdout().flush()
