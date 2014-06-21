import unittest

from fixedint import *

tests = []

# ----------------------------------------------------------------------------
class ClassTests(unittest.TestCase):
    def test_subclass_base(self):
        self.assertRaises(Exception, type, 'TestClass', (FixedInt,), {})
        self.assertRaises(Exception, type, 'TestClass', (MutableFixedInt,), {})

    def test_class_cache(self):
        self.assertEqual(FixedInt(99), FixedInt(99))
        self.assertEqual(MutableFixedInt(42), MutableFixedInt(42))
tests.append(ClassTests)

# ----------------------------------------------------------------------------
class BasicTests(unittest.TestCase):
    def test_signed(self):
        f10 = FixedInt(10)
        self.assertEqual(f10.width, 10)
        self.assertEqual(f10.mutable, False)
        self.assertEqual(f10.signed, True)
        self.assertEqual(f10.minval, -512)
        self.assertEqual(f10.maxval, 511)

        self.assertEqual(int(f10(1024)), 0)
        self.assertEqual(int(f10(1025)), 1)
        self.assertEqual(int(f10(511)), 511)
        self.assertEqual(int(f10(512)), -512)
        self.assertEqual(int(f10(511) + 1), -512)
tests.append(BasicTests)

# ----------------------------------------------------------------------------
def run(verbosity=1, repeat=1):
    suite = unittest.TestSuite()
    for cls in tests:
        for _ in range(repeat):
            suite.addTest(unittest.makeSuite(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

if __name__ == '__main__':
    run()
