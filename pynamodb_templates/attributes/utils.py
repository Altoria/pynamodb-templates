from typing import *

try:
    from typing import Unpack  # noqa
except ImportError:
    from typing_extensions import Unpack


_T = TypeVar("_T")

__all__ = ["AttributeKwargs", "Unpack"]


class AttributeKwargs(TypedDict):
    hash_key: bool
    range_key: bool
    null: Optional[bool]
    default: Optional[Union[_T, Callable[..., _T]]]
    default_for_new: Optional[Union[Any, Callable[..., _T]]]
    attr_name: Optional[str]
