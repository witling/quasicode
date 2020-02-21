from context import Context

from .assign import *
from .branch import *
from .builtin import *
from .decl import *
from .marker import *
from .operator import *
from .value import *

def isof(var, cls) -> bool:
    return isinstance(var, cls) or any(isof(cls, b) for b in var.__class__.__bases__ if b.__name__ != 'object')
