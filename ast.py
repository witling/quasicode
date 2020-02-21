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
            'Assign': {
                'LHAssign': None,
                'RHAssign': None
            },
            # attributes to statements
            'Marker': {
                'ConstantMarker': None,
                'MainMarker': None,
                'SoMarker': None
            },
            'Nop': None,
            'NestedStatement': {
                'Declaration': None,
                'Branch': {
                    'If': None,
                    'Elif': None
                },
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

def isof(var, cls) -> bool:
    return isinstance(var, cls) or any(isof(cls, b) for b in var.__class__.__bases__ if b.__name__ != 'object')

def create_classes(ast, parents=(object, )):
    if not ast or isinstance(ast, list):
        return

    def construct(self, **kargs):
        super(self.__class__, self).__init__(**kargs)

    # get around sharing `k`
    def to_string(k):
        def inner(_):
            return str(k)
        return inner

    for k, v in ast.items():
        if k not in globals():
            attrs = {'__str__': to_string(k)}
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
        if isof(other, Keyword):
            return self._name == other._name
        return False

    def __str__(self):
        return self.name()

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
        if isof(marker, MainMarker):
            self._is_main = True

    def __str__(self):
        return 'Declaration'

class Block(list):
    def __str__(self):
        return ' '.join(map(str, self))

class Value:
    def is_assignable(self):
        return False
    
    def eq(self, other):
        return True

class Constant(Value):
    def __init__(self, val):
        self._val = val

    def __str__(self):
        return self._val

class Number(Value):
    def __init__(self, val):
        self._val = val

    def __str__(self):
        return self._val

class String(Value):
    def __init__(self, val: str):
        self._val = val

    def __str__(self):
        return self._val

class Ident(Value):
    def __init__(self, name: str):
        self._name = name

    def name(self):
        return self._name
    
    def __str__(self):
        return self._name

    def is_assignable(self):
        return True

class Print(Statement):
    def __init__(self):
        self._args = []

    def add_arg(self, arg):
        self._args.append(arg)

    def __str__(self):
        return 'print {}'.format(' '.join(map(str, self._args)))

class Assign(Statement):
    def __init__(self):
        self._ident = None
        self._value = None

    def ident(self):
        return self._ident

    def set_ident(self, ident):
        self._ident = ident

    def value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def __str__(self):
        return '{} = {}'.format(self._ident, self._value)

class Branch(NestedStatement):
    def __init__(self):
        self._branches = []
        self._default_branch = None

    def add_branch(self, condition, block):
        self._branches.append((condition, block))

    def set_default_branch(self, block):
        self._default_branch = block

    def __str__(self):
        fixed = map(lambda x: '{} -> {}', self._branches)
        if self._default_branch:
            fixed.append('-> {}'.format(self._default_branch))
        return '\n'.join(fixed)

class Repeat(NestedStatement):
    def __init__(self):
        self._block = []

    def block(self):
        return self._block

    def set_block(self, block):
        self._block = block

    def __str__(self):
        return 'Repeat'

class Operator(Keyword):
    def __init__(self):
        self._args = []

    def add_arg(self, arg):
        self._args.append(arg)
