from .ast import *
from .ast.generic import *
import pickle

class Function(object):
    def __init__(self, args, block):
        assert isof(args, list)
        assert isof(block, Block)
        self._args = args
        self._block = block

    def args(self):
        return self._args

    def block(self):
        return self._block

    def __str__(self):
        return '\n'.join(map(str, self._block))

class Program(object):
    FEXT = '.qc'
    FEXTC = '.qcc'

    def __init__(self):
        self._idents = {}
        self._flow = []
        self._uses = []
        self._entry_point = None

    # load a program from filepointer
    def load(fp):
        import lib
        return pickle.load(fp)

    # write a program into filepointer
    def save(self, fp):
        pickle.dump(self, fp)
        return True

    def __iter__(self):
        return iter(self._flow)

    def __contains__(self, key):
        return key in self._idents

    def __getitem__(self, key):
        if key not in self._idents:
            return None
        return self._idents[key]

    def entry_point(self):
        return self._entry_point

    def set_entry_point(self, ident: str):
        assert not self._entry_point
        self._entry_point = ident

    def ident(self, ident: str, value):
        self._idents[ident] = value

    def idents(self) -> dict:
        return self._idents

    def use(self, name):
        self._uses.append(name)

    def uses(self) -> list:
        return self._uses

    def __str__(self) -> str:
        fixed = map(lambda x: '{}:\n{}'.format(x[0], x[1]), self._idents.items())
        return '\n'.join(fixed)

class PythonLibrary(Program):
    def __init__(self):
        super().__init__()

class PythonFunction(Function):
    def __init__(self, args, fn):
        super().__init__(args, Block())
        self._fn = fn

    def block(self):
        return None

    def __str__(self):
        return '<python function>'

    def run(self, ctx):
        return fn(ctx)
