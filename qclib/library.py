import inspect
import pylovm2
import re
import sys

def _load_binary(fpath):
    from .program import Program
    module = pylovm2.Module.load(fpath)
    return Program(module) if pylovm2.ENTRY_POINT in module else Library(module)

def _load_source(fpath, auto_main=False):
    from .generate import Compiler
    import os.path
    name, _ = os.path.splitext(os.path.basename(fpath))
    compiler = Compiler()
    with open(fpath, 'r') as src:
        return compiler.compile(src.read(), auto_main, module_name=name, module_location=fpath)

class Library(object):
    FEXT = '.qc'
    FEXTC = '.qcc'
    VIRTUAL_MODULE = '__main__'

    def __init__(self, module=None):
        self._module = module

    def __contains__(self, key):
        return key in self._module

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

        return lib

    # write a program to a filepath
    def save(self, fpath):
        self._module.save(fpath)
        return True

    def location(self):
        return self._module.location()

    def uses(self) -> list:
        return self._module.uses()

    def modname(self):
        return self._module.name()

    def __str__(self) -> str:
        return str(self._module)
