A simple fixed-width integer library for Python.

The library is geared towards users who need to emulate machine integers.

It provides flexible classes for defining integers with a fixed number of bits, as well
as predefined classes for common machine integer sizes. These classes can be used as
drop-in replacements for int/long, and can be sliced to extract bitfields.

Mutable versions of these integers are provided, enabling usages such as emulation of
machine registers.