"""
O3JSON5 - A fast JSON5 parser for Python
"""
from typing import Any, TextIO, Union
from o3json5.o3json5 import loads as _loads
from o3json5.o3json5 import DecodeError as _DecodeError
from pathlib import Path

# Type for JSON-compatible input strings
JsonInput = Union[str, bytes, bytearray]

DecodeError = _DecodeError
"""Exception raised when JSON5 decoding fails, subclass of ValueError."""

loads = _loads
"""Parse a JSON5 string or bytes-like object.

Args:
    s: A string, bytes, or bytearray containing a JSON5 document

Returns:
    The Python object represented by the JSON5 document

Raises:
    DecodeError: If the input is not valid JSON5
    TypeError: If the input type is not supported
"""


def load(fp: Union[str, Path, TextIO]) -> Any:
    """Parse a JSON5 document from a file path or file-like object.

    Args:
        fp: A string file path, Path object, or file-like object containing a JSON5 document

    Returns:
        The Python object represented by the JSON5 document

    Raises:
        DecodeError: If the input is not valid JSON5
        TypeError: If the input type is not supported
        OSError: If there are file handling errors
    """
    if isinstance(fp, (str, Path)):
        with open(fp, "r") as f:
            return loads(f.read())
    return loads(fp.read())


__all__ = ["loads", "DecodeError", "load", "JsonInput"]
