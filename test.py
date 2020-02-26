from unittest import TestLoader, TextTestRunner

loader = TestLoader()
suite = loader.discover('qc')

runner = TextTestRunner()
runner.run(suite)
