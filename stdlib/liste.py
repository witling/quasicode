from qclib.ast import *
from qclib.library import *

class ListeLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('länge', create_fn(self._len))
        self.ident('lösche', create_fn(self._delete))

        self.ident('push', create_fn(self._push))
        self.ident('pop', create_fn(self._pop))
        self.ident('pop_front', create_fn(self._pop_front))

    def _len(self, ls):
        return Number(len(ls._val))

    def _delete(self, ls, idx):
        del ls._val[idx]

    def _push(self, ls, item):
        ls._val.append(item)

    def _pop(self, ls):
        return ls._val.pop()

    def _pop_front(self, ls):
        if 0 < len(ls):
            first = ls._val[0]
            del ls._val[0]
            return first
        return None
