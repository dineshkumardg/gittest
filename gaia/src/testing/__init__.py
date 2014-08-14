from StringIO import StringIO
import unittest

def main(suite):
    results = StringIO()
    unittest.TextTestRunner(stream=results, verbosity=0).run(suite)
    print results.getvalue()
