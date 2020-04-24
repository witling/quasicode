from .ast import *
from .ast.generic import *
#from .lib import *
#from . import lib

import pickle
import re
import sys

def create(name, fn):
    return PythonFunction(name, fn)

def create_const(name, fn):
    return PythonFunction(name, fn)

def get_vlib_modname_by_path(path):
    from os.path import abspath, basename, splitext
    fname = basename(abspath(path))
    fname, _ = splitext(fname)
    return get_vlib_modname(fname)

def get_vlib_modname(sub=None):
    if sub is None:
        return Library.VIRTUAL_MODULE
    return '{}.{}'.format(Library.VIRTUAL_MODULE, sub)

def init_vlib(modname=None, mod=None):
    """
    this initializes a virtual module containing all loaded qc library files.
    """
    import types

    if modname is None:
        modname = get_vlib_modname()

    if mod is None:
        mod = types.ModuleType(modname, 'virtual module for importing libraries')

    sys.modules[modname] = mod

class Library(object):
    FEXT = '.qc'
    FEXTC = '.qcc'
    VIRTUAL_MODULE = 'vlib'

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
    def load(fname):
        modname = get_vlib_modname_by_path(fname)
        init_vlib()
        init_vlib(modname)

        with open(fname, 'rb') as fp:
            return pickle.load(fp)

    # write a program into filepointer
    def save(self, fname):
        with open(fname, 'wb') as fp:
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
