from .ast.generic import Block, isof

class Function(object):
    def __init__(self, args, block):
        assert isof(args, list)
        assert isof(block, Block)
        self._args = args
        self._block = block

    def args(self):
        return self._args

    def block(self):
        return self._block

    def __str__(self):
        return '\n'.join(map(str, self._block))
