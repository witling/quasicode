from ..ast import *

SYN_PHRASES = [
    ('action please', MainMarker),  # main method
    ('passt so', Operator),         # rounding nums: <value> passt so 
    ('das ist', Compare),           # comparison
    ('im quadrat', Operator),       # square something
    ('und zwar', Declaration),      # function declaration: und zwar <ident> mit <ident1>
    ('und fertig', Return),         # return from a function: <value> und fertig
    ('das holen wir nach', Repeat), # repeat last statement
    ('ach kris.', Else),            # add an else branch to an if
]

SYN_OPERATORS = [
    ('+', Add),
    ('-', Sub),
    ('*', Mul),
    ('/', Div),
    ('modulo', Mod),
    ('<', Less),
]

SYN_KEYWORDS = [
    ('use', Use),               # import functions from a file
    ('uzbl', UzblConstant),     # True
    ('menge', Menge),           # object-like thing
    ('liste', Liste),           # list-like thing
    ('quasi', Print),           # output value
    ('bitte?', Readin),         # input value
    ('und', LogicalAnd),        # logical and; concatenate strings (?)
    ('oder', LogicalOr),        # logical or
    ('not', LogicalNot),        # logical not
    ('so', SoMarker),           # speed up program
    ('stark', ConstMarker),     # declare a constant
    ('mit', Arguments),         # introduce arguments
    ('also', RHAssign),         # right hand assignment <val> = <ident>
    ('ist', LHAssign),          # left hand assignment <ident> = <val>
    ('jens', Exit),             # exit program
    ('kris?', If),              # if
    ('kris??', Elif),           # else if
    ('patrick!', Break),        # break
    ('hä', Debug),              # acts as breakpoint for debugger
    ('softwareproblem', Raise), # raise error
    ('fähler', Raise),          # read last error
    ('oettinger', Nop),         # keine ahnung
]

KEYWORDS = []
SYN_TREE = {}

def setup():
    global KEYWORDS
    global SYN_TREE

    # add keywords
    KEYWORDS = list(map(lambda x: x[0], SYN_KEYWORDS))

    # add operators
    KEYWORDS.extend(list(map(lambda x: x[0], SYN_OPERATORS)))

    for parts, tag in map(lambda x: (x[0].split(' '), x[1]), SYN_PHRASES):
        node = SYN_TREE
        for k in parts:
            if k not in KEYWORDS:
                KEYWORDS.append(k)

            if k not in node:
                new_node = {}
                node[k] = new_node
                node = new_node
            else:
                node = node[k]
        node['_op'] = tag

    for k, tag in SYN_KEYWORDS:
        if k not in SYN_TREE:
            SYN_TREE[k] = { '_op': tag }
        else:
            SYN_TREE[k]['_op'] = tag

    for k, tag in SYN_OPERATORS:
        if k not in SYN_TREE:
            SYN_TREE[k] = { '_op': tag }
        else:
            SYN_TREE[k]['_op'] = tag

setup()
