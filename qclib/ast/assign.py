from .generic import *
from .value import Access

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
        if isof(self._ident, Access):
            menge = ctx[self._ident]
            last = self._ident.subparts()[-1]

            for subpart in self._ident.subparts()[:-1]:
                menge = menge[subpart]

            menge[last] = self._value.run(ctx)
        else:
            ctx[self._ident] = self._value.run(ctx)

    def __str__(self):
        return '{} = {}'.format(self._ident, self._value)

class LHAssign(Assign):
    def __init__(self):
        super().__init__()

class RHAssign(Assign):
    def __init__(self):
        super().__init__()
