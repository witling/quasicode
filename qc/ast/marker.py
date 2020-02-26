from .generic import Keyword

class Marker(Keyword):
    def __str__(self):
        return 'Marker'

class ConstMarker(Marker):
    pass

class MainMarker(Marker):
    pass

class SoMarker(Marker):
    pass
