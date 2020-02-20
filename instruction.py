class Instruction:
    ASSIGN = 1
    PRINT = 2

    ADD = 3
    SUB = 4
    MUL = 5
    DIV = 6
    POW = 7
    MOD = 8

    def __init__(self):
        self._args = []

    def arguments(self, **kargs):
        self._args = kargs
