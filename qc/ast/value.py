from context import *

class Value:
    def __init__(self, val):
        self._val = val

    def create(val):
        raise Exception()

    def __str__(self):
        return self._val

    def is_assignable(self):
        return False
    
    def eq(self, other):
        return True

    def run(self, ctx: Context):
        return self._val

class Constant(Value):
    def __init__(self, val):
        super().__init__(val)

class Number(Value):
    def __init__(self, val):
        super().__init__(val)

    def __str__(self):
        return str(self._val)

class String(Value):
    def __init__(self, val: str):
        super().__init__(val)

class Ident(Value):
    def __init__(self, name: str):
        super().__init__(name)

    def name(self):
        return self._val

    def run(self, ctx: Context):
        return ctx[self._val]
    
    def is_assignable(self):
        return True
