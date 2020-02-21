from ast import *
from program import *

class Compiler:
    def __init__(self):
        pass

    def compile(self, parsed) -> Program:
        program = Program()
        for item in parsed:
            if isof(item, Declaration):
                if item.is_main():
                    program.set_entry_point(item.name())
                program.ident(item.name(), Function(item.block()))
        return program
