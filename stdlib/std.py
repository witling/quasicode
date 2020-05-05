from qclib.library import *
from qclib.ast import *

import math
import random

class StdLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('random', create_fn(self._rnd))
        self.ident('sqrt', create_fn(self._sqrt))

    def _sqrt(self, arg1: float):
        return Number(math.sqrt(arg1))
    
    def _rnd(self):
        return Number(random.random())
