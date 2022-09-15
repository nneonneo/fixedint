from typing import Optional, Type
import fixedint.base
from fixedint.aliases import *

# workaround for being unable to specify multiple inheritance in a type annotation
class _FixedInt(fixedint.base.FixedInt, int): ...  # type: ignore[misc]

def FixedInt(width: int, signed: bool=True, mutable: Optional[bool] = None) -> Type[_FixedInt]: ...
def MutableFixedInt(width: int, signed: bool=True) -> Type[fixedint.base.MutableFixedInt]: ...
