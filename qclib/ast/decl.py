from .generic import *
from .marker import *
from .value import *

class Declaration(NestedStatement):
    def __init__(self):
        super().__init__()
        self._is_main = False
        self._args = []
        self._name = None

    def name(self):
        return self._name.name()

    def set_name(self, name: Ident):
        self._name = name

    def args(self):
        return self._args

    def set_args(self, args):
        self._args = args

    def is_main(self):
        return self._is_main

    def add_marker(self, marker: Marker):
        if isof(marker, MainMarker):
            self._is_main = True

    def __str__(self):
        return 'Declaration'
