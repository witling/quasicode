from .ast import *
from .ast.generic import *

#import dill
import inspect
import pylovm2
import re
import sys

def todo():
    print('todo')
    assert False

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

def create_const(name, value):
    return Value.create(value)

def get_vlib_modname_by_path(path):
    from os.path import abspath, basename, splitext
    fpath = basename(abspath(path))
    fpath, _ = splitext(fpath)
    return get_vlib_modname(fpath)

def get_vlib_modname(sub=None):
    if sub is None:
        return Library.VIRTUAL_MODULE
    return '{}.{}'.format(Library.VIRTUAL_MODULE, sub)

def _load_binary(fpath):
    from .program import Program
    module = pylovm2.Module.load(fpath)
    return Program(module) if pylovm2.ENTRY_POINT in module else Library(module)
    #modname = get_vlib_modname_by_path(fpath)
    #init_vlib()
    #init_vlib(modname)

    #with open(fpath, 'rb') as fp:
    #    sys.modules[modname] = dill.load(fp)

    #return sys.modules.get(modname)

def _load_source(fpath, auto_main=False):
    from .generate import Compiler
    import os.path
    name, _ = os.path.splitext(os.path.basename(fpath))
    compiler = Compiler()
    with open(fpath, 'r') as src:
        return compiler.compile(src.read(), auto_main, module_name=name, module_location=fpath)

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

    def __init__(self, module=None):
        self._module = module
        #self._idents = {}
        #self._uses = []
        self._file = None

    def __contains__(self, key):
        return key in self._module

    def __getitem__(self, key):
        todo()
        #if key not in self._idents:
        #    return None
        #return self._idents[key]

    def set_file_path(self, fpath):
        from os.path import abspath
        self._file = fpath

    # load a program from a filepath
    def load(fpath, auto_main=False):
        import os.path
        fpath = os.path.abspath(fpath)

        _, fext = os.path.splitext(fpath)

        if fext == Library.FEXT:
            lib = _load_source(fpath, auto_main)

        elif fext == Library.FEXTC:
            lib = _load_binary(fpath)

        else:
            raise Exception('unsupported file extension')

        lib.set_file_path(fpath)

        return lib

    # write a program to a filepath
    def save(self, fpath):
        self._module.save(fpath)
        #with open(fpath, 'wb') as fp:
        #    dill.dump(self, fp, recurse=True)
        return True

    def ident(self, ident: str, value):
        todo()
        #self._idents[ident] = value

    def idents(self) -> dict:
        todo()
        #return self._idents

    def use(self, name):
        todo()
        #self._uses.append(name)

    def uses(self) -> list:
        return self._module.uses()

    def modname(self):
        if self._file is None:
            return None

        from os.path import basename, splitext
        fpath, _ = splitext(basename(self._file))
        return fpath

    def __str__(self) -> str:
        return str(self._module)
        #fixed = map(lambda x: '{}:\n{}'.format(x[0], x[1]), self._idents.items())
        #return '\n'.join(fixed)

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
