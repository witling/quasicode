class OutOfOettingerException(Exception):
    pass

class LookupException(Exception):
    def __init__(self, name):
        super().__init__('cannot use `{}`, not found'.format(str(name)))

class RuntimeException(Exception):
    pass
