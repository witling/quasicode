from qclib.library import *
from qclib.ast import *

import math
import random

class MathLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('ceil', create_fn(self._ceil))
        self.ident('floor', create_fn(self._floor))
        self.ident('random', create_fn(self._rnd))
        self.ident('sqrt', create_fn(self._sqrt))

    def _ceil(self, arg1: float):
        return Number(math.ceil(arg1))

    def _floor(self, arg1: float):
        return Number(math.floor(arg1))

    def _sqrt(self, arg1: float):
        return Number(math.sqrt(arg1))
    
    def _rnd(self):
        return Number(random.random())
