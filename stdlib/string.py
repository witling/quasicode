from qclib.library import *
from qclib.ast import Value

class StringLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('concat', create_fn(self._concat))
        self.ident('format', create_fn(self._format))

    def _concat(self, first, second):
        return Value.create(first + second)

    def _format(self, template, arg):
        return Value.create(str(template).format(arg))
