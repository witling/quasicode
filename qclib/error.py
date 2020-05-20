class OutOfOettingerException(Exception):
    def __init__(self):
        super().__init__('the program ran out of oettinger')

class LookupException(Exception):
    def __init__(self, name):
        super().__init__('cannot use `{}`, not found'.format(str(name)))

class AssertException(Exception):
    def __init__(self, condition):
        super().__init__('the assertion for `{}` failed', condition)

class RuntimeException(Exception):
    pass
