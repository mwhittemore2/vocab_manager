import unittest

if __name__ == "__main__":
    tests = unittest.TestLoader().discover('testing')
    unittest.TextTestRunner(verbosity=2).run(tests)