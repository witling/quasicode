class Program:
    def __init__(self):
        self._idents = {}
        self._flow = []

    def ident(self, ident: str, value):
        self._idents[ident] = value

    def idents(self) -> dict:
        return self._idents
