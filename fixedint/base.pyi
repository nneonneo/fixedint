from typing import Optional, Type, TypeVar, Union
from numbers import Integral

FSelf = TypeVar("FSelf", bound="FixedInt")
Other = Union[Integral, "FixedInt"]

class FixedInt:
    def __init__(self: FSelf, val: Union[int, str] = 0): ...

    def __pow__(self: FSelf, other: Other, modulo: Optional[Other]=None) -> FSelf: ...
    def __rpow__(self: FSelf, other: Other) -> FSelf: ...
    def __repr__(self: FSelf) -> str: ...
    def __str__(self: FSelf) -> str: ...
    def __getitem__(self: FSelf, item) -> FSelf: ...

    @classmethod
    def from_bytes(cls: Type[FSelf], bytes, byteorder: str='little', signed: Optional[bool]=None) -> FSelf: ...
    def to_bytes(self: FSelf, length: Optional[int]=None, byteorder: str='little') -> bytes: ...
    def __round__(self: FSelf, n: int=0) -> int: ...

    def __neg__(self: FSelf) -> FSelf: ...
    def __pos__(self: FSelf) -> FSelf: ...
    def __abs__(self: FSelf) -> FSelf: ...
    def __invert__(self: FSelf) -> FSelf: ...

    def __add__(self: FSelf, other: Other) -> FSelf: ...
    def __sub__(self: FSelf, other: Other) -> FSelf: ...
    def __mul__(self: FSelf, other: Other) -> FSelf: ...
    def __floordiv__(self: FSelf, other: Other) -> FSelf: ...
    def __mod__(self: FSelf, other: Other) -> FSelf: ...
    def __lshift__(self: FSelf, other: Other) -> FSelf: ...
    def __rshift__(self: FSelf, other: Other) -> FSelf: ...
    def __and__(self: FSelf, other: Other) -> FSelf: ...
    def __xor__(self: FSelf, other: Other) -> FSelf: ...
    def __or__(self: FSelf, other: Other) -> FSelf: ...

    def __radd__(self: FSelf, other: Other) -> FSelf: ...
    def __rsub__(self: FSelf, other: Other) -> FSelf: ...
    def __rmul__(self: FSelf, other: Other) -> FSelf: ...
    def __rfloordiv__(self: FSelf, other: Other) -> FSelf: ...
    def __rmod__(self: FSelf, other: Other) -> FSelf: ...
    def __rand__(self: FSelf, other: Other) -> FSelf: ...
    def __rxor__(self: FSelf, other: Other) -> FSelf: ...
    def __ror__(self: FSelf, other: Other) -> FSelf: ...
    # Note that rlshift/rrshift are not overridden as we do not want the LHS
    # to be forced to the same type if the fixed int is on the RHS

    width: int
    mutable: bool
    signed: bool
    maxval: int
    minval: int

MSelf = TypeVar("MSelf", bound="MutableFixedInt")

class MutableFixedInt(FixedInt):
    def __format__(self: MSelf, format_spec, /) -> str: ...
    def __ipow__(self: MSelf, other: Other, modulo: Optional[Other]=None) -> MSelf: ...
    def __setitem__(self: MSelf, item, value: Other) -> bool: ...

    def __iadd__(self: MSelf, other: Other) -> MSelf: ...
    def __isub__(self: MSelf, other: Other) -> MSelf: ...
    def __imul__(self: MSelf, other: Other) -> MSelf: ...
    def __ifloordiv__(self: MSelf, other: Other) -> MSelf: ...
    def __imod__(self: MSelf, other: Other) -> MSelf: ...
    def __ilshift__(self: MSelf, other: Other) -> MSelf: ...
    def __irshift__(self: MSelf, other: Other) -> MSelf: ...
    def __iand__(self: MSelf, other: Other) -> MSelf: ...
    def __ior__(self: MSelf, other: Other) -> MSelf: ...
    def __ixor__(self: MSelf, other: Other) -> MSelf: ...

    def __int__(self: MSelf, /) -> int: ...
    def __float__(self: MSelf, /) -> float: ...
    def __index__(self: MSelf, /) -> int: ...
    def __trunc__(self: MSelf) -> int: ...
    def __bool__(self: MSelf) -> bool: ...

    def __truediv__(self: MSelf, value: Other, /) -> float: ...
    def __rtruediv__(self: MSelf, value: Other, /) -> float: ...
    def __divmod__(self: MSelf, value: Other, /) -> tuple[int, int]: ...
    def __rdivmod__(self: MSelf, value: Other, /) -> tuple[int, int]: ...
    def __rlshift__(self: MSelf, value: Other, /) -> int: ...  # type: ignore[misc]
    def __rrshift__(self: MSelf, value: Other, /) -> int: ...  # type: ignore[misc]
    def __eq__(self: FSelf, value: object, /) -> bool: ...
    def __ne__(self: FSelf, value: object, /) -> bool: ...
    def __ge__(self: FSelf, value: Other, /) -> bool: ...
    def __gt__(self: FSelf, value: Other, /) -> bool: ...
    def __le__(self: FSelf, value: Other, /) -> bool: ...
    def __lt__(self: FSelf, value: Other, /) -> bool: ...