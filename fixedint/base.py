#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import sys

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

_subclass_token = object()
class _FixedIntBaseMeta(type):
    def __new__(cls, name, bases, dict):
        if dict.get('_subclass_enable', None) == _subclass_token:
            del dict['_subclass_enable']
            return type.__new__(cls, name, bases, dict)

        for base in bases:
            if issubclass(base, FixedInt):
                raise Exception("Cannot subclass {0}; use the {0} constructor to produce new subclasses.".format(base.__name__))
        raise Exception("Cannot subclass this class.")

    def __call__(self, width, signed=True, mutable=None, hex=False, name=None):
        signed = bool(signed)
        if mutable is None:
            # Take mutable from constructor used (FixedInt or MutableFixedInt)
            mutable = self._mutable
        hex = bool(hex)
        
        if signed:
            min = -1<<(width-1)
            max = (1<<(width-1))-1
        else:
            min = 0
            max = (1<<width)-1

        if mutable:
            bases = (MutableFixedInt,)
        elif max <= sys.maxint:
            bases = (FixedInt, int)
        else:
            bases = (FixedInt, long)

        dict = {}
        dict['width'] = FixedProperty(width)
        dict['signed'] = FixedProperty(signed)
        dict['mutable'] = FixedProperty(mutable)
        dict['minval'] = FixedProperty(min)
        dict['maxval'] = FixedProperty(max)
        dict['hex'] = hex

        if signed:
            _mask = (1<<width) - 1
            _mask2 = 1<<(width-1)
            def _rectify(val):
                val = val & _mask
                val = val - 2*(val & _mask2)
                return val
        else:
            _mask = (1<<width) - 1
            def _rectify(val):
                return val & _mask
        dict['_rectify'] = staticmethod(_rectify)

        if not mutable:
            intbase = bases[1]
            def _newfunc(cls, val=0):
                ''' Convert an integer into a fixed-width integer. '''
                return intbase.__new__(cls, _rectify(val))
            _newfunc.__name__ = '__new__'
            dict['__new__'] = _newfunc

        if name is None:
            name = ''.join(['Mutable'*mutable, 'U'*(not signed), 'Int', str(width)])

        return _FixedIntMeta(name, bases, dict)

    width = FixedMetaProperty('width')
    signed = FixedMetaProperty('signed')
    mutable = FixedMetaProperty('mutable')
    minval = FixedMetaProperty('minval')
    maxval = FixedMetaProperty('maxval')

class _FixedIntMeta(_FixedIntBaseMeta):
    __new__ = type.__new__
    __call__ = type.__call__


def int_method(f):
    f.__doc__ = getattr(int, f.__name__).__doc__
    return f

class FixedInt:
    __slots__ = ()
    _mutable = False
    _subclass_enable = _subclass_token
    __metaclass__ = _FixedIntBaseMeta

    # width, signed, mutable, minval, maxval, hex defined in metaclass
    # _rectify defined in metaclass
    # __new__ defined in metaclass

    @int_method
    def __hex__(self):
        width = (self.width + 3) // 4
        return '0x%0*x' % (width, int(self))

    @int_method
    def __oct__(self):
        width = (self.width + 2) // 3
        return '0x%0*o' % (width, int(self))

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
        if self.hex:
            return hex(self)
        return str(int(self))

class MutableFixedInt(FixedInt):
    _mutable = True
    _subclass_enable = _subclass_token

    def __init__(self, val=0, base=None):
        ''' Convert an integer into a fixed-width integer. '''
        if base is not None:
            val = int(val, base)

        self._val = self._rectify(val)

    @int_method
    def __int__(self):
        return self._val

    @int_method
    def __index__(self):
        return self._val

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
    def _f(self, other):
        nt = _arith_convert(type(self), type(other))
        return nt(intfunc(int(self), int(other)))
    functools.update_wrapper(_f, intfunc)
    return _f

def _misc_binfunc_factory(name):
    ''' Factory function producing methods for non-arithmetic operators '''
    intfunc = getattr(int, name)
    def _f(self, other):
        return intfunc(int(self), int(other))
    functools.update_wrapper(_f, intfunc)
    return _f

def _arith_unary_factory(name):
    intfunc = getattr(int, name)
    def _f(self):
        nt = type(self)
        return nt(intfunc(int(self)))
    functools.update_wrapper(_f, intfunc)
    return _f

def _misc_unary_factory(name):
    ''' Factory function producing methods for non-arithmetic operators '''
    intfunc = getattr(int, name)
    def _f(self):
        return intfunc(int(self))
    functools.update_wrapper(_f, intfunc)
    return _f
