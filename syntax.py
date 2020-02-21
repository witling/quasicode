from ast import *

SYN_PHRASES = [
    ('action please', Marker), # main method
    ('passt so', Operator), # rounding nums: <value> passt so 
    ('das ist', Operator),  # comparison
    ('im quadrat', Operator), # square something
    ('und zwar', Statement),  # function declaration: und zwar <ident> mit <ident1>
    ('und fertig', Statement),  # return from a function: <value> und fertig
    ('das holen wir nach', Statement), # repeat last statement
]

SYN_KEYWORDS = [
    ('uzbl', Constant),     # True
    ('nuzbl', Constant),     # False
    ('quasi', Statement),    # output value
    ('und', Operator),      # logical and; concatenate strings (?)
    ('oder', Operator),     # logical or
    ('so', Statement),       # speed up program
    ('also', Statement),     # right hand assignment <val> = <ident>
    ('stark', Statement),    # declare a constant
    ('ist', Statement),      # left hand assignment <ident> = <val>
    ('jens', Statement),     # exit program
    ('kris?', Statement),    # if
    ('kris??', Statement),   # else if
    ('patrick!', Statement), # break
    ('softwareproblem', Statement), # raise error
    ('fähler', Statement),  # raise error
    ('oettinger', Statement) # keine ahnung
]

KEYWORDS = []
SYN_TREE = {}

def setup():
    global KEYWORDS
    global SYN_TREE

    KEYWORDS = list(map(lambda x: x[0], SYN_KEYWORDS))

    for parts, tag in map(lambda x: (x[0].split(' '), x[1]), SYN_PHRASES):
        tree_node = SYN_TREE
        for k in parts:
            if k not in KEYWORDS:
                KEYWORDS.append(k)

            if k not in tree_node:
                new_node = {}
                tree_node[k] = new_node
                tree_node = new_node
            else:
                tree_node = tree_node[k]
        tree_node['_op'] = tag

    for k, tag in SYN_KEYWORDS:
        if k not in SYN_TREE:
            SYN_TREE[k] = { '_op': tag }
        else:
            SYN_TREE[k]['_op'] = tag

setup()
