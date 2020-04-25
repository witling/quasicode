from qclib.library import *
from qclib.ast import *

class StringLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('concat', create(['first', 'second'], self._concat))
        self.ident('format', create(['template', 'arg'], self._format))

    def _concat(self, ctx):
        first, second = ctx['first'], ctx['second']
        return Value.create(first + second)

    def _format(self, ctx):
        template, arg = ctx['template'], ctx['arg']
        return Value.create(str(template).format(arg))
