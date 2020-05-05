from qclib.library import *
from qclib.ast import *

class IOLibrary(PyLibrary):
    __module__ = '__main__'

    def __init__(self):
        PyLibrary.__init__(self)

        self.ident('schreibe', create_fn(self._write))
        self.ident('inhaliere', create_fn(self._read))

    def _read(self, path):
        with open(path, 'r') as fp:
            return fp.read()

    def _write(self, path, content):
        with open(path, 'w') as fp:
            fp.write(content)
