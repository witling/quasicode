from .generic import *

class Assign(Statement, Runnable):
    def __init__(self):
        self._ident = None
        self._value = None

    def ident(self):
        return self._ident

    def set_ident(self, ident):
        self._ident = ident

    def value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def run(self, ctx):
        ctx[self._ident] = self._value.run(ctx)

    def __str__(self):
        return '{} = {}'.format(self._ident, self._value)

class LHAssign(Assign):
    def __init__(self):
        super().__init__()

class RHAssign(Assign):
    def __init__(self):
        super().__init__()
