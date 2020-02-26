import sys

from generate import Compiler
from interpreter import Interpreter

def load_source(fname):
    with open(fname, 'r') as src:
        return src.read()

def main():
    if len(sys.argv) < 2:
        print('no file given')
        return

    src = load_source(sys.argv[1])
    compiler = Compiler()
    program = compiler.compile(src)

    print(program)

    interpreter = Interpreter()
    interpreter.load(program)
    interpreter.run()

if __name__ == '__main__':
    main()
