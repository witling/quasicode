import qclib
from qclib.library import *

class StdLibrary(Library):
    __module__ = '__main__'

    def __init__(self):
        Library.__init__(self)

        self.ident('random', create([], self._rnd))
        self.ident('sqrt', create([Ident('arg1')], self._sqrt))

    def _sqrt(self, ctx):
        #self.binder.wimport('math')
        return Number(math.sqrt(float(ctx['arg1'])))
    
    def _rnd(self, ctx):
        #self.library.wimport('random')
        return Number(random.random())
