=====================================
fixedint: simple fixed-width integers
=====================================

This module provides fixed-size integer classes which retain their fixed nature across
arithmetic operations. It is geared towards users who need to emulate machine integers.

It provides flexible classes for defining integers with a fixed number of bits, as well
as predefined classes for common machine integer sizes. These classes can be used as
drop-in replacements for int/long, and can be sliced to extract bitfields.

Mutable versions of these integers are provided, enabling usages such as emulation of
machine registers.



Basic Usage
===========

A collection of predefined fixed-width integers for widths 8, 16, 32 and 64 are available
in signed and unsigned varieties. Mutable and immutable versions of each type are provided.

These are named as ``[Mutable][U]Int<N>``, e.g. ``UInt64`` or ``MutableInt8``. Use these
classes as you would ``int``; arithmetic operations involving these classes will preserve
fixed width. For example::

    x = UInt32(0)
    print(hex(~x)) # prints 0xffffffff

Mutable instances can be modified in-place, preserving their type::

    x = MutableUInt32(0)
    y = x
    x += 100
    print(y) # prints 100

To set a mutable integer without losing its type, use slicing::

    x = MutableUInt32(0)
    x[:] = -1
    print(hex(x)) # prints 0xffffffff


Arithmetic Operations
=====================

``FixedInt`` instances support all arithmetic operators. For binary operators, both
operands are converted to plain Python ``int`` and then operated on. With a few
exceptions, the result will be cast back to a ``FixedInt`` large enough to hold either
operand, provided one of the operands was a ``FixedInt``. Note that the resulting
``FixedInt`` may not be large enough to hold the complete result, in which case the
result will be truncated.

The exceptions are as follows:

* ``divmod`` returns a tuple of plain ``int`` s
* true division returns a float
* ``**``, ``<<`` and ``>>`` will return a ``FixedInt`` if the left operand was a
  ``FixedInt``, and plain ``int`` otherwise.

Mutable instances additionally support in-place operations, which will modify the
value without altering its type.


Arithmetic operations between two integers of different sizes follow C integer promotion
rules when determining the type of the final result. These rules boil down to the
following:

* If the operands are both signed, or both unsigned, the wider of the two operand types is chosen.
* Otherwise, if the unsigned operand is wider, the unsigned operand is chosen.
* Otherwise, the signed operand is chosen.




Slicing
=======

``FixedInt`` instances support slicing. Slicing with a single integer produces a single
Boolean value representing the bit at that position. Slicing with a range produces a
``FixedInt`` containing the range of bits. Mutable instances additionally support slice
assignment. This makes e.g. manipulating a flag register straightforward, without needing
to use bitwise operations.

All indexing operations treat the least-significant bit (LSB) as bit 0. Currently, only
contiguous bit sections can be obtained; for more flexibility consider using a module
such as `bitarray`.

Getting a slice results in a ``FixedInt`` instance with exactly as many bits as the range.
This can be used to perform wraparound arithmetic on a bit field.

Slices support two main syntaxes::

    value[<start>:<end>]
    value[<start>:<length>j]

The latter syntax is more convenient when dealing with fixed-width fields. Either of the
slice arguments may be omitted, in which case they will default to the LSB and MSB of
the ``FixedInt`` respectively.



Byte Conversion
===============

``FixedInt`` instances can be converted to and from raw byte representations by using the
``.to_bytes`` instance method and the ``.from_bytes`` classmethod. The usage of these
methods matches that of Python 3.4's ``int.to_bytes`` and ``int.from_bytes`` methods, but
the length is automatically inferred from the integer width.



.. __CUT__

Build Status
============

.. image:: https://github.com/nneonneo/fixedint/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/nneonneo/fixedint/actions/workflows/python-package.yml
