# -*- coding: utf-8 -*-

import functools
import sys
from fixedint.compat import *
from weakref import WeakValueDictionary

class FixedProperty(object):
    def __init__(self, val):
        self.val = val
    def __get__(self, obj, type=None):
        return self.val
    def __set__(self, obj, value):
        raise AttributeError("property is read-only")

class FixedMetaProperty(object):
    def __init__(self, name):
        self.name = name
    def __get__(self, obj, type=None):
        prop = obj.__dict__[self.name]
        return prop.__get__(obj)
    def __set__(self, obj, value):
        raise AttributeError("property %s is read-only" % self.name)

if not PY3K:
    # While it'd be nice to put machine-sized integers into Python 2.x "int"s,
    # it turns out that the int methods occasionally freak out when given longs.
    # So, we use arbitrary-precision ints for all Pythons.
    int = long

_class_cache = WeakValueDictionary()

_subclass_token = object()
class _FixedIntBaseMeta(type):
    def __new__(cls, name, bases, dict):
        if dict.get('_subclass_enable', None) == _subclass_token:
            del dict['_subclass_enable']
            return type.__new__(cls, name, bases, dict)

        for base in bases:
            if issubclass(base, FixedInt):
                basename = base.__name__
                raise Exception("Cannot subclass %s; use the %s constructor to produce new subclasses." % (basename, basename))
        raise Exception("Cannot subclass this class.")

    def __call__(self, width, signed=True, mutable=None):
        signed = bool(signed)
        if mutable is None:
            # Take mutable from constructor used (FixedInt or MutableFixedInt)
            mutable = self._mutable

        cachekey = (width, signed, mutable)
        try:
            return _class_cache[cachekey]
        except KeyError:
            pass
            
        if signed:
            min = -1<<(width-1)
            max = (1<<(width-1))-1
        else:
            min = 0
            max = (1<<width)-1

        if mutable:
            bases = (MutableFixedInt,)
        else:
            bases = (FixedInt, int)

        dict = {}
        dict['width'] = FixedProperty(width)
        dict['signed'] = FixedProperty(signed)
        dict['mutable'] = FixedProperty(mutable)
        dict['minval'] = FixedProperty(min)
        dict['maxval'] = FixedProperty(max)

        if signed:
            _mask = (1<<width) - 1
            _mask2 = 1<<(width-1)
            def _rectify(val):
                val = val & _mask
                return int(val - 2*(val & _mask2))
        else:
            _mask = (1<<width) - 1
            def _rectify(val):
                return int(val & _mask)
        dict['_rectify'] = staticmethod(_rectify)

        if not mutable:
            intbase = bases[1]
            def _newfunc(cls, val=0):
                ''' Convert an integer into a fixed-width integer. '''
                return intbase.__new__(cls, _rectify(val))
            _newfunc.__name__ = '__new__'
            dict['__new__'] = _newfunc

        name = ''.join(['Mutable'*mutable, 'U'*(not signed), 'Int', str(width)])

        cls = _FixedIntMeta(name, bases, dict)
        _class_cache[cachekey] = cls
        return cls

    width = FixedMetaProperty('width')
    signed = FixedMetaProperty('signed')
    mutable = FixedMetaProperty('mutable')
    minval = FixedMetaProperty('minval')
    maxval = FixedMetaProperty('maxval')

class _FixedIntMeta(_FixedIntBaseMeta):
    __new__ = type.__new__
    __call__ = type.__call__


def int_method(f):
    if isinstance(f, str):
        def wrapper(f2):
            f2.__name__ = f
            return int_method(f2)
        return wrapper
    else:
        f.__doc__ = getattr(int, f.__name__).__doc__
        return f

class FixedInt:
    __slots__ = ()
    _mutable = False
    _subclass_enable = _subclass_token

    # width, signed, mutable, minval, maxval defined in metaclass
    # _rectify defined in metaclass
    # __new__ defined in metaclass

    if not PY3K:
        @int_method
        def __hex__(self):
            return '%#x' % int(self)
        def __oct__(self):
            return '%#o' % int(self)

    @int_method
    def __pow__(self, other, modulo=None):
        return type(self)(int.__pow__(int(self), int(other), modulo))

    @int_method
    def __rpow__(self, other):
        return type(other)(int.__rpow__(int(self), int(other)))

    @int_method
    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)

    @int_method
    def __str__(self):
        return str(int(self))

    if PY3K:
        @int_method
        def __round__(self, n=0):
            return int(self)

    # Inherited methods which are fine as-is:
    # complex, int, long, float, index
    # truediv, rtruediv, divmod, rdivmod, rlshift, rrshift
    # format

FixedInt = add_metaclass(_FixedIntBaseMeta)(FixedInt)


class MutableFixedInt(FixedInt):
    _mutable = True
    _subclass_enable = _subclass_token

    def __init__(self, val=0, base=None):
        ''' Convert an integer into a fixed-width integer. '''
        if base is not None:
            val = int(val, base)

        self._val = self._rectify(val)

    if PY3K:
        @int_method
        def __format__(self, format_spec):
            return format(self._val, format_spec)

## Arithmetic methods
def _arith_unary_factory(name, mutable):
    ''' Factory function producing methods for unary operations. '''
    intfunc = getattr(int, name)
    if mutable:
        @int_method(name)
        def _f(self):
            return type(self)(intfunc(self._val))
    else:
        @int_method(name)
        def _f(self):
            return type(self)(intfunc(self))
    return _f

_arith_unary = 'neg pos abs invert'.split()
for f in _arith_unary:
    s = '__%s__' % f
    setattr(FixedInt, s, _arith_unary_factory(s, mutable=False))
    setattr(MutableFixedInt, s, _arith_unary_factory(s, mutable=True))


def _arith_convert(t1, t2):
    if not issubclass(t2, FixedInt):
        return t1

    # Follow C conversion rules (ISO/IEC 9899:TC3 §6.3.1.8)
    if t1.signed == t2.signed:
        # If both are signed or both are unsigned, return the larger type.
        if t1.width >= t2.width:
            return t1
        return t2

    if not t1.signed:
        ut, st = t1, t2
    else:
        ut, st = t2, t1

    if ut.width >= st.width:
        # If the unsigned type has rank >= the signed type, convert the signed type to the unsigned type.
        return ut
    else:
        return st

def _arith_binfunc_factory(name):
    ''' Factory function producing methods for arithmetic operators '''
    intfunc = getattr(int, name)
    @int_method(name)
    def _f(self, other):
        nt = _arith_convert(type(self), type(other))
        return nt(intfunc(int(self), int(other)))
    return _f

# divmod, rdivmod, truediv, rtruediv are considered non-arithmetic since they don't return ints
# pow, rpow, rlshift, and rrshift are special since the LHS and RHS are very different
_arith_binfunc = 'add sub mul floordiv mod lshift rshift and xor or'.split()
_arith_binfunc += 'radd rsub rmul rfloordiv rmod rand rxor ror'.split()
if not PY3K:
    _arith_binfunc += 'div rdiv'.split()

for f in _arith_binfunc:
    s = '__%s__' % f
    setattr(FixedInt, s, _arith_binfunc_factory(s))


## Non-arithmetic methods (Mutable only)
def _nonarith_unary_factory_mutable(name):
    ''' Factory function producing methods for unary operations. '''
    intfunc = getattr(int, name)
    @int_method(name)
    def _f(self):
        return intfunc(self._val)
    return _f

_mutable_unary = 'int float index'.split()
if sys.version_info[:2] >= (2,6):
    _mutable_unary += ['trunc']
if PY3K:
    _mutable_unary += 'bool'.split()
else:
    _mutable_unary += 'nonzero long'.split()

for f in _mutable_unary:
    s = '__%s__' % f
    setattr(MutableFixedInt, s, _nonarith_unary_factory_mutable(s))


def _nonarith_binfunc_factory_mutable(name):
    ''' Factory function producing methods for non-arithmetic binary operators on Mutable instances. '''
    intfunc = getattr(int, name)
    @int_method(name)
    def _f(self, other):
        return intfunc(self._val, int(other))
    return _f

_mutable_binfunc = 'truediv rtruediv divmod rdivmod rlshift rrshift'.split()
if hasattr(int, '__cmp__'):
    _mutable_binfunc += ['cmp']
else:
    _mutable_binfunc += 'lt le eq ne gt ge'.split()
for f in _mutable_binfunc:
    s = '__%s__' % f
    setattr(MutableFixedInt, s, _nonarith_binfunc_factory_mutable(s))


## In-place operators
def _inplace_factory_mutable(iname, name, op):
    ''' Factory function producing methods for augmented assignments on Mutable instances. '''
    intfunc = getattr(int, name)
    def _f(self, other):
        self._val = self._rectify(intfunc(self._val, int(other)))
        return self
    _f.__name__ = iname
    doc = list.__iadd__.__doc__
    if doc:
        _f.__doc__ = doc.replace('__iadd__', name).replace('+=', op)
    return _f

# pow is special because it takes three arguments.
_inplace_func = 'add,+ sub,- mul,* truediv,/ floordiv,// mod,% lshift,<< rshift,<< and,& or,| xor,^'.split()
if not PY3K:
    _inplace_func += ['div,/']
for f in _inplace_func:
    fn, op = f.split(',')
    si = '__i%s__' % fn
    so = '__%s__' % fn
    setattr(MutableFixedInt, si, _inplace_factory_mutable(si, so, op+'='))
