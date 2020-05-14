#!/usr/bin/python3

def main():
    import sys

    if len(sys.argv) <= 1:
        print('no file given')
        exit()

    from os.path import abspath, dirname, join
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from qclib import Compiler, Interpreter

    with open(sys.argv[1], 'r') as fin:
        program = Compiler().compile(fin.read())

    interpreter = Interpreter()
    interpreter.disable_funny_mod()
    interpreter.load(program)
    interpreter.run()

if __name__ == '__main__':
    main()
