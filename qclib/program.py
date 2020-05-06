from .library import *

class Program(Library):
    def __init__(self):
        super().__init__()
        # TODO: is flow needed?
        self._flow = []
        self._entry_point = None

    def __iter__(self):
        return iter(self._flow)

    def entry_point(self):
        return self._entry_point

    def set_entry_point(self, ident: str):
        self._entry_point = ident
