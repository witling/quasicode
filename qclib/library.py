from .ast import *
from .ast.generic import *

import dill
import inspect
import re
import sys

def create_fn(fn):
    sig = inspect.signature(fn)
    param_protocols = []

    # create a list of (param_name, conv_fn)-pairs where 
    # conv_fn is called on values retrieved from the context
    for param_name, param in sig.parameters.items():
        conv_fn = None
        if param.annotation != inspect._empty:
            conv_fn = param.annotation
        param_protocols.append((param_name, conv_fn))

    return PyFunction(param_protocols, fn)

#def create_fn_with_context(name, fn):
#    return PyFunction(name, fn)

def create_const(name, value):
    return Value.create(value)

def get_vlib_modname_by_path(path):
    from os.path import abspath, basename, splitext
    fname = basename(abspath(path))
    fname, _ = splitext(fname)
    return get_vlib_modname(fname)

def get_vlib_modname(sub=None):
    if sub is None:
        return Library.VIRTUAL_MODULE
    return '{}.{}'.format(Library.VIRTUAL_MODULE, sub)

def _load_binary(fname):
    modname = get_vlib_modname_by_path(fname)
    init_vlib()
    init_vlib(modname)

    with open(fname, 'rb') as fp:
        sys.modules[modname] = dill.load(fp)

    return sys.modules.get(modname)

def _load_source(fname):
    from .generate import Compiler
    compiler = Compiler()
    with open(fname, 'r') as src:
        return compiler.compile(src.read())

def init_vlib(modname=None, mod=None):
    """
    this initializes a virtual module containing all loaded qc library files.
    """
    import types

    if modname is None:
        modname = get_vlib_modname()

    if modname in sys.modules and modname == Library.VIRTUAL_MODULE:
        # this makes 'vlib' a package
        sys.modules[modname].__path__ = iter([])
    
    else:
        if mod is None:
            mod = types.ModuleType(modname, 'virtual module for importing libraries')

        if modname == Library.VIRTUAL_MODULE:
            # this makes 'vlib' a package
            mod.__path__ = iter([])

        sys.modules[modname] = mod

class Library(object):
    FEXT = '.qc'
    FEXTC = '.qcc'
    VIRTUAL_MODULE = '__main__'

    def __init__(self):
        self._idents = {}
        self._uses = []
        self._file = None

    def __contains__(self, key):
        return key in self._idents

    def __getitem__(self, key):
        if key not in self._idents:
            return None
        return self._idents[key]

    def set_file_path(self, fname):
        from os.path import abspath
        self._file = fname

    # load a program from filepointer
    def load(fname):
        from os.path import splitext

        _, fext = splitext(fname)

        if fext == Library.FEXT:
            lib = _load_source(fname)

        elif fext == Library.FEXTC:
            lib = _load_binary(fname)

        else:
            raise Exception('unsupported file extension')

        lib.set_file_path(fname)

        return lib

    # write a program into filepointer
    def save(self, fname):
        with open(fname, 'wb') as fp:
            dill.dump(self, fp, recurse=True)
        return True

    def ident(self, ident: str, value):
        self._idents[ident] = value

    def idents(self) -> dict:
        return self._idents

    def use(self, name):
        self._uses.append(name)

    def uses(self) -> list:
        return self._uses

    def modname(self):
        if self._file is None:
            return None

        from os.path import basename, splitext
        fname, _ = splitext(basename(self._file))
        return fname

    def __str__(self) -> str:
        fixed = map(lambda x: '{}:\n{}'.format(x[0], x[1]), self._idents.items())
        return '\n'.join(fixed)

class PyLibrary(Library):
    def __init__(self):
        Library.__init__(self)

class PyFunction(Function):
    def __init__(self, args, fn):
        super().__init__(args, Block())
        self._fn = fn

    def args(self):
        return [name for name, _ in self._args]

    def block(self):
        return self

    def __str__(self):
        return '<python function>'

    def run(self, ctx):
        kwargs = {}

        # generate a **kwargs out of ctx when called; pass it to `fn`
        for param_name, conv_fn in self._args:
            kwargs[param_name] = ctx[param_name]
            if not conv_fn is None:
                kwargs[param_name] = conv_fn(kwargs[param_name])

        return self._fn(**kwargs)
