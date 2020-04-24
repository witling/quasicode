from .library import *

class Program(Library):
    def __init__(self):
        super().__init__()
        self._flow = []
        self._entry_point = None

    def __iter__(self):
        return iter(self._flow)

    def entry_point(self):
        return self._entry_point

    def set_entry_point(self, ident: str):
        assert not self._entry_point
        self._entry_point = ident
