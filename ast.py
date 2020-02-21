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
            'NestedStatement': {
                'Declaration': None,
                'If': None,
                'Elif': None,
                'Repeat': None
            },
            'Print': None,
            'Raise': None,
            'Return': None,
        }
    },
    'Value': {
        'Constant': None,
        'Number': None,
        'String': None,
        'Ident': None,
    }
}

def create_classes(ast, parents=(object, )):
    if not ast or isinstance(ast, list):
        return

    def construct(self, **kargs):
        super(self.__class__, self).__init__(**kargs)

    for k, v in ast.items():
        if k not in globals():
            attrs = {}
            #attrs = {'__init__': construct}
            cls = type(k, parents, attrs)
            globals()[k] = cls
        else:
            cls = globals()[k]

        create_classes(v, parents=(cls, ))

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

class Declaration(NestedStatement):
    def __init__(self):
        self._is_main = False
        self._block = None

    def name(self):
        return self._name

    def set_name(self, name: Ident):
        self._name = name

    def block(self):
        return self._block

    def set_block(self, block):
        self._block = block

    def is_main(self):
        return self._is_main

    def add_marker(self, marker: Marker):
        if isinstance(marker, MainMarker):
            self._is_main = True

class Block(list):
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
    
    def __str__(self):
        return self._name

    def is_assignable(self):
        return True
