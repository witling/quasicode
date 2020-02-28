from unittest import TestLoader, TextTestRunner

loader = TestLoader()
suite = loader.discover('test')

runner = TextTestRunner()
runner.run(suite)
