import sys

from compiler import Compiler
from interpreter import Interpreter
from parser import Parser

def load_source(fname):
    with open(fname, 'r') as src:
        return src.read()

def main():
    if len(sys.argv) < 2:
        print('no file given')
        return

    interpreter = Interpreter()
    parser = Parser()
    compiler = Compiler()

    src = load_source(sys.argv[1])
    parsed = parser.parse(src)
    program = compiler.compile(parsed)

    print(program)

    interpreter.load(program)

    interpreter.run()

if __name__ == '__main__':
    main()
