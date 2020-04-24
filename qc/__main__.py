import sys

try:
    from qclib import *
except:
    from os.path import abspath, dirname, join
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from qclib import *

def load_source(fname):
    with open(fname, 'r') as src:
        return src.read()

def retrieve_program(fname):
    from os.path import splitext

    _, fext = splitext(fname)

    if fext == Program.FEXT:
        src = load_source(sys.argv[1])
        compiler = Compiler()
        return compiler.compile(src)

    elif fext == Program.FEXTC:
        return Program.load(fname)

    raise Exception('unsupported file extension')

def main():
    if len(sys.argv) < 2:
        print('no file given')
        return

    program = retrieve_program(sys.argv[1])
    interpreter = Interpreter()

    if '--listing' in sys.argv:
        print(program)

    if '--debug' in sys.argv:
        from pudb import set_trace
        set_trace()

    if '--nichluschdich' in sys.argv:
        interpreter.disable_funny_mode()

    interpreter.load(program)
    interpreter.run()

if __name__ == '__main__':
    main()
