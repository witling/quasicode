from .ast import *
from .ast.generic import *
from .lib import *
from . import lib

import sys
import re

import pickle

class Library(object):
    FEXT = '.qc'
    FEXTC = '.qcc'

    def __init__(self):
        self._idents = {}
        self._uses = []

    def __contains__(self, key):
        return key in self._idents

    def __getitem__(self, key):
        if key not in self._idents:
            return None
        return self._idents[key]

    # load a program from filepointer
    def load(fp):
        sys.modules['lib'] = lib
        return pickle.load(fp)

    # write a program into filepointer
    def save(self, fp):
        pickle.dump(self, fp)
        return True

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

class PythonFunction(Function):
    def __init__(self, args, fn):
        super().__init__(args, Block())
        self._fn = fn

    def block(self):
        return self

    def __str__(self):
        return '<python function>'

    def run(self, ctx):
        return self._fn(ctx)
