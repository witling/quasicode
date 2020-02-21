AST = {
    'Keyword': {
        # operations that return a value
        'Operator': { },
        # operations that don't return a value
        'Statement': {
            'Declaration': None,
            # attributes to statements
            'Marker': None
        }
    }
}

def create_classes():
    pass

class Keyword:
    def __init__(self, name: str):
        self._name = name

    def name(self):
        return self._name

    def eq(self, other):
        if isinstance(other, str):
            return self._name == other
        if isinstance(other, Keyword):
            return self._name == other._name
        return False

class Operator(Keyword):
    pass

class Statement(Keyword):
    pass

class Marker(Keyword):
    pass

class Declaration(Statement):
    pass

class Return(Statement):
    pass

class Repeat(Statement):
    pass

class If(Statement):
    pass

class Elif(Statement):
    pass

class Break(Statement):
    pass

class Raise(Statement):
    pass

class Nop(Statement):
    pass

class Exit(Statement):
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
