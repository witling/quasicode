import sys

from generate import Compiler
from interpreter import Interpreter

def load_source(fname):
    with open(fname, 'r') as src:
        return src.read()

def retrieve_program(fname):
    from os.path import splitext

    _, fext = splitext(fname)

    if fext == '.qc':
        src = load_source(sys.argv[1])
        compiler = Compiler()
        return compiler.compile(src)

    elif fext == '.qcc':
        return Program.load(fname)

    raise Exception('unsupported file extension')

def main():
    if len(sys.argv) < 2:
        print('no file given')
        return

    program = retrieve_program(sys.argv[1])

    if '--listing' in sys.argv:
        print(program)

    if '--debug' in sys.argv:
        from pudb import set_trace
        set_trace()

    interpreter = Interpreter()
    interpreter.load(program)
    interpreter.run()

if __name__ == '__main__':
    main()
