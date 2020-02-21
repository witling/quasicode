class Keyword:
    def __init__(self, name: str):
        self._name = name

    def eq(self, other):
        if isinstance(other, str):
            return self._name == other
        if isinstance(other, Keyword):
            return self._name == other._name
        return False

# operations that return a value
class Operator(Keyword):
    pass

# operations that don't return a value
class Statement(Keyword):
    pass

# attributes to statements
class Marker(Keyword):
    pass

class Value:
    def is_assignable(self):
        return False
    
    def eq(self, other):
        return True

class Constant(Value):
    def __init__(self, val):
        self._val = val

class Number(Value):
    def __init__(self, val):
        self._val = val

class String(Value):
    def __init__(self, val: str):
        self._val = val

class Ident(Value):
    def __init__(self, name: str):
        self._name = name

    def is_assignable(self):
        return True
