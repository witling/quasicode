from qclib.library import *
from qclib.ast import *

from urllib import request

class NetLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('ziehe', create(['url'], self._download))

    def _download(self, ctx):
        url = ctx['url']
        req = request.urlopen(url)
        if req.msg == 'OK':
            return Value.create(req.read())
        return Value.create(False)
