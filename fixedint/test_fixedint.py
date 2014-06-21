import unittest
import sys

PY3K = sys.version_info[0] >= 3

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

    def test_aliases(self):
        self.assertEqual(FixedInt(8), Int8)
        self.assertEqual(FixedInt(16), Int16)
        self.assertEqual(FixedInt(32), Int32)
        self.assertEqual(FixedInt(64), Int64)
        self.assertEqual(FixedInt(8, signed=False), UInt8)
        self.assertEqual(FixedInt(16, signed=False), UInt16)
        self.assertEqual(FixedInt(32, signed=False), UInt32)
        self.assertEqual(FixedInt(64, signed=False), UInt64)

    def test_subclassing(self):
        from fixedint.util import HexFormattingMixin
        class MyUInt32(HexFormattingMixin, UInt32):
            pass
        self.assertEqual(str(MyUInt32(32)), '0x00000020')

tests.append(ClassTests)

# ----------------------------------------------------------------------------
class BasicTests(unittest.TestCase):
    def test_properties(self):
        f3 = FixedInt(3)
        self.assertEqual(f3.width, 3)
        self.assertEqual(f3.mutable, False)
        self.assertEqual(f3.signed, True)
        self.assertEqual(f3.minval, -4)
        self.assertEqual(f3.maxval, 3)

        f3 = MutableFixedInt(3)
        self.assertEqual(f3.width, 3)
        self.assertEqual(f3.mutable, True)
        self.assertEqual(f3.signed, True)
        self.assertEqual(f3.minval, -4)
        self.assertEqual(f3.maxval, 3)

        f3 = FixedInt(3, signed=False)
        self.assertEqual(f3.width, 3)
        self.assertEqual(f3.mutable, False)
        self.assertEqual(f3.signed, False)
        self.assertEqual(f3.minval, 0)
        self.assertEqual(f3.maxval, 7)

        f3 = MutableFixedInt(3, signed=False)
        self.assertEqual(f3.width, 3)
        self.assertEqual(f3.mutable, True)
        self.assertEqual(f3.signed, False)
        self.assertEqual(f3.minval, 0)
        self.assertEqual(f3.maxval, 7)

    def test_rectify(self):
        for f10 in [FixedInt(10), MutableFixedInt(10)]:
            self.assertEqual(int(f10(1024)), 0)
            self.assertEqual(int(f10(1025)), 1)
            self.assertEqual(int(f10(511)), 511)
            self.assertEqual(int(f10(512)), -512)

        for f10 in [FixedInt(10, signed=False), MutableFixedInt(10, signed=False)]:
            self.assertEqual(int(f10(1024)), 0)
            self.assertEqual(int(f10(1025)), 1)
            self.assertEqual(int(f10(511)), 511)
            self.assertEqual(int(f10(512)), 512)

    def test_simple_arith(self):
        for f8 in [Int8, MutableInt8]:
            a = f8(15)
            b = f8(10)
            self.assertEqual(int(a+b), 25)
            self.assertEqual(int(a-b), 5)
            self.assertEqual(int(a*b), (150-256))
            self.assertEqual(a.__truediv__(b), 1.5)
            self.assertEqual(int(a // b), 1)
            self.assertEqual(divmod(a, b), (1, 5))
            self.assertEqual(divmod(15, b), (1, 5))
            self.assertEqual(divmod(a, 10), (1, 5))
            self.assertEqual(int(a)**b, 15**10)
            self.assertEqual(int(a<<8), 0)
            self.assertEqual(8<<a, 8<<15)
            self.assertEqual(int(~a), ~15)
            self.assertEqual(int(-a), -15)
            self.assertEqual(int((~a) & 0xff), ~15)
        for f64 in [Int64, MutableInt64]:
            a = f64(15)
            b = f64(10)
            self.assertEqual(int(a+b), 25)
            self.assertEqual(int(a-b), 5)
            self.assertEqual(int(a*b), 150)
            self.assertEqual(a.__truediv__(b), 1.5)
            self.assertEqual(int(a // b), 1)
            self.assertEqual(divmod(a, b), (1, 5))
            self.assertEqual(divmod(15, b), (1, 5))
            self.assertEqual(divmod(a, 10), (1, 5))
            self.assertEqual(int(a)**b, 15**10)
            self.assertEqual(int(a<<8), 15<<8)
            self.assertEqual(8<<a, 8<<15)
            self.assertEqual(int(~a), ~15)
            self.assertEqual(int(-a), -15)

    def test_typecast(self):
        import math
        for f16 in [Int16, MutableInt16]:
            x = f16(42)
            self.assertEqual(int(x), 42)
            self.assertEqual(float(x), 42)
            self.assertEqual(complex(x), 42)
            self.assertEqual(round(x), 42)
            if not PY3K:
                self.assertEqual(long(x), 42)
            self.assertEqual(bool(x), True)
            self.assertEqual(list(range(100))[x], 42)
            if sys.version_info[:2] >= (2,6):
                self.assertEqual(math.trunc(x), 42)

            x = f16(0)
            self.assertEqual(bool(x), False)

    def test_compare(self):
        for f32 in [Int32, MutableInt32]:
            x = f32(1000000)
            self.assertEqual(x, 1000000)
            self.assertNotEqual(x, 1000000 + (1<<32))
            self.assertEqual(x, f32(1000000 + (1<<32)))
            self.assertNotEqual(x, 1000001)
            self.assertTrue(x <= 1000000)
            self.assertTrue(x >= 1000000)
            self.assertTrue(x < 1000001)
            self.assertTrue(x > 999999)
            if not PY3K:
                self.assertTrue(cmp(x, 999999) > 0)

    def test_implicit_conversion(self):
        f = FixedInt(72)
        x = f(32767)
        y = x
        self.assertEqual(x, y)
        x += 100
        self.assertNotEqual(x, y)
        x += FixedInt(80)(1<<79)
        self.assertEqual(x.width, 80)

    def test_inplace_operators(self):
        mf = MutableFixedInt(72)
        x = mf(32767)
        y = x
        self.assertEqual(x, y)
        x += 100
        self.assertEqual(x, y)
        x += MutableFixedInt(80)(1<<79)
        self.assertEqual(x.width, 72)
        x >>= 100
        self.assertEqual(x, 0)
        x += 2
        self.assertEqual(y, 2)
        x **= 70
        self.assertEqual(y, 2**70)


    def test_str(self):
        for ff in [FixedInt(12), MutableFixedInt(12), FixedInt(91), MutableFixedInt(91)]:
            self.assertEqual(str(ff(1)), '1')
            self.assertEqual(repr(ff(1)), '%s(1)' % ff.__name__)
            self.assertEqual(str(ff(-1)), '-1')
            self.assertEqual(hex(ff(1)), '0x1')

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
