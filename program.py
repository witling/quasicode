class Block:
    pass

class Branch:
    pass

class Loop:
    pass

class Function:
    def __init__(self, block):
        self._block = block

class Program:
    def __init__(self):
        self._idents = {}
        self._flow = []
        self._entry_point = None

    def entry_point(self):
        return self._entry_point

    def set_entry_point(self, ident: str):
        assert not self._entry_point
        self._entry_point = ident

    def ident(self, ident: str, value):
        self._idents[ident] = value

    def idents(self) -> dict:
        return self._idents

    def __str__(self) -> str:
        fixed = map(lambda x: '{}: {}'.format(x[0], x[1]), self._idents.items())
        return '\n'.join(fixed)
