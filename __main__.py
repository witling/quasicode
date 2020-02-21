import sys

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

    src = load_source(sys.argv[1])
    program = parser.parse(src)

    interpreter.load(program)

    interpreter.run()

if __name__ == '__main__':
    main()
