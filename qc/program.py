import ast

class Function:
    def __init__(self, args, block):
        assert ast.isof(args, list)
        assert ast.isof(block, ast.Block)
        self._args = args
        self._block = block

    def args(self):
        return self._args

    def block(self):
        return self._block

    def __str__(self):
        return '\n'.join(map(str, self._block))

class Program:
    def __init__(self):
        self._idents = {}
        self._flow = []
        self._entry_point = None

    def __iter__(self):
        return iter(self._flow)

    def __contains__(self, key):
        return key in self._idents

    def __getitem__(self, key):
        if key not in self._idents:
            return None
        return self._idents[key]

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
        fixed = map(lambda x: '{}:\n{}'.format(x[0], x[1]), self._idents.items())
        return '\n'.join(fixed)
