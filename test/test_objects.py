import unittest

from .deps import *

class TestObjects(Test):
    def test_creation(self, internals):
        src = """
und zwar main action please
    obj1 ist menge
    
    obj1.x ist 1
    obj1.y ist 1
        """
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)
