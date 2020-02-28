from .deps import *

def create(name, fn):
    return PythonFunction(name, fn)

def random(ctx):
    import random
    return random.random()

class StdLibrary(PythonLibrary):
    def __init__(self):
        super().__init__()

        self.ident('random', create([], random))
