from .deps import *

import math
import random

def create(name, fn):
    return PythonFunction(name, fn)

def sqrt(ctx):
    return Number(math.sqrt(float(ctx['arg1'])))

def rnd(ctx):
    return Number(random.random())

class StdLibrary(PythonLibrary):
    def __init__(self):
        super().__init__()

        self.ident('random', create([], rnd))
        self.ident('sqrt', create([Ident('arg1')], sqrt))
