AST = {
    'Block': { },
    'Keyword': {
        # operations that return a value
        'Operator': { 
            'Compare': None,
            'LogicalAnd': None,
            'LogicalNot': None,
            'LogicalOr': None
        },
        # operations that don't return a value
        'Statement': {
            'Break': None,
            'Declaration': None,
            'Exit': None,
            'LHAssign': None,
            'RHAssign': None,
            # attributes to statements
            'Marker': {
                'ConstantMarker': None,
                'MainMarker': None,
                'SoMarker': None
            },
            'Nop': None,
            'If': None,
            'Elif': None,
            'Raise': None,
            'Return': None,
            'Repeat': None
        }
    },
    'Value': {
        'Constant': None,
        'Number': None,
        'String': None,
        'Ident': None,
    }
}

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
    
    def __str__(self):
        return 'Ident({})'.format(self._name)

    def is_assignable(self):
        return True

def create_classes(ast, parents=(object, )):
    if not ast or isinstance(ast, list):
        return

    def construct(self, *args):
        super().__init__(args)
        print(args)

    for k, v in ast.items():
        if k not in globals():
            cls = type(k, parents, {'__init__': construct})
            globals()[k] = cls
        else:
            cls = globals()[k]

        create_classes(v, parents=(cls, ))

create_classes(AST)
