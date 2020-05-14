import sys

from deps import *

c = Compiler()
with open(sys.argv[1], 'r') as fin:
    program = c.compile(fin.read())

    interpreter = Interpreter()
    interpreter.disable_funny_mode()
    interpreter.load(program)
    interpreter.run()
