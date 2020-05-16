from qclib.library import *
from qclib.ast import *

class ListeLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('länge', create_fn(self._len))

    def _len(self, ls):
        return Number(len(ls._val))
