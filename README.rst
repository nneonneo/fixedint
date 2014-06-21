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



Arithmetic Operations
=====================

``FixedInt`` instances support all arithmetic operators. For binary operators, both
operands are converted to plain Python ``int`` and then operated on. With a few
exceptions, the result will be cast back to a ``FixedInt`` large enough to hold either
operand, provided one of the operands was a ``FixedInt``. Note that the resulting
``FixedInt`` may not be large enough to hold the complete result, in which case the
result will be truncated.

The exceptions are as follows:

* ``divmod`` returns a tuple of plain ``int``s
* true division returns a float
* ``**``, ``<<`` and ``>>`` will return a ``FixedInt`` if the left operand was a
  ``FixedInt``, and plain ``int`` otherwise.

Mutable instances additionally support in-place operations, which will modify the
value without altering its type.
