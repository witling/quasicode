from qclib.library import *
from qclib.ast import *

import math
import random

class StdLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('random', create_fn([], self._rnd))
        self.ident('sqrt', create_fn([Ident('arg1')], self._sqrt))

    def _sqrt(self, ctx):
        return Number(math.sqrt(float(ctx['arg1'])))
    
    def _rnd(self, ctx):
        return Number(random.random())
