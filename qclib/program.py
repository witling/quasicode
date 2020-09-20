from .library import *

class Program(Library):
    def __init__(self, module=None):
        super().__init__(module)
        self._entry_point = None

    def entry_point(self):
        return self._entry_point

    def set_entry_point(self, ident: str):
        self._entry_point = ident
