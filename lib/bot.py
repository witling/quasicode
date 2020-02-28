from .deps import *

def create(name, fn):
    return PythonFunction(name, fn)

class BotLibrary(PythonLibrary):
    def __init__(self):
        super().__init__()
