from ast import *

SYN_PHRASES = [
    ('action please', Marker), # main method
    ('passt so', Operator), # rounding nums: <value> passt so 
    ('das ist', Operator),  # comparison
    ('im quadrat', Operator), # square something
    ('und zwar', Declaration),  # function declaration: und zwar <ident> mit <ident1>
    ('und fertig', Return),  # return from a function: <value> und fertig
    ('das holen wir nach', Repeat), # repeat last statement
]

SYN_KEYWORDS = [
    ('uzbl', Constant),         # True
    ('nuzbl', Constant),        # False
    ('quasi', Statement),       # output value
    ('und', Operator),          # logical and; concatenate strings (?)
    ('oder', Operator),         # logical or
    ('not', Operator),          # logical not
    ('so', Statement),          # speed up program
    ('stark', Marker),          # declare a constant
    ('also', Statement),        # right hand assignment <val> = <ident>
    ('ist', Statement),         # left hand assignment <ident> = <val>
    ('jens', Exit),             # exit program
    ('kris?', If),              # if
    ('kris??', Elif),           # else if
    ('patrick!', Break),        # break
    ('softwareproblem', Raise), # raise error
    ('fähler', Raise),          # raise error
    ('oettinger', Nop)          # keine ahnung
]

KEYWORDS = []
SYN_TREE = {}

def setup():
    global KEYWORDS
    global SYN_TREE

    KEYWORDS = list(map(lambda x: x[0], SYN_KEYWORDS))

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

setup()
