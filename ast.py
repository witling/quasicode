AST = {
    'Keyword': {
        # operations that return a value
        'Operator': { },
        # operations that don't return a value
        'Statement': {
            'Break': None,
            'Declaration': None,
            'Exit': None,
            # attributes to statements
            'Marker': None,
            'Nop': None,
            'If': None,
            'Elif': None,
            'Raise': None,
            'Return': None,
            'Repeat': None
        }
    }
}

def create_classes(ast, parents=(object, )):
    if not ast or isinstance(ast, list):
        return

    def default_constructor(self, *args):
        print(args)

    for k, v in ast.items():
        if k not in globals():
            new_cls = type(k, parents, {})
            globals()[k] = new_cls

        create_classes(v, parents=(new_cls, ))

create_classes(AST)

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
