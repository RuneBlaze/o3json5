import pytest
from o3json5 import loads, load, DecodeError
from pathlib import Path
import math


# Basic type tests
def test_parse_null():
    assert loads("null") is None


def test_parse_boolean():
    assert loads("true") is True
    assert loads("false") is False


def test_parse_numbers():
    assert loads("42") == 42
    assert loads("-42") == -42
    assert loads("3.14") == 3.14
    assert loads("-3.14") == -3.14
    assert loads("1e-10") == 1e-10
    assert loads("1.5e+5") == 1.5e5


def test_parse_strings():
    assert loads('"hello"') == "hello"
    assert loads("'hello'") == "hello"  # JSON5 feature
    assert loads('"hello\\nworld"') == "hello\nworld"


# Array tests
def test_parse_empty_array():
    assert loads("[]") == []


def test_parse_simple_array():
    assert loads("[1,2,3]") == [1, 2, 3]


def test_parse_array_with_trailing_comma():
    # JSON5 feature
    assert loads("[1,2,3,]") == [1, 2, 3]


# Object tests
def test_parse_empty_object():
    assert loads("{}") == {}


def test_parse_simple_object():
    assert loads('{"a": 1, "b": 2}') == {"a": 1, "b": 2}


def test_parse_object_trailing_comma():
    # JSON5 feature
    assert loads('{"a": 1, "b": 2,}') == {"a": 1, "b": 2}


def test_parse_object_unquoted_keys():
    # JSON5 feature
    assert loads("{a: 1, b: 2}") == {"a": 1, "b": 2}


# Whitespace handling
def test_parse_whitespace():
    assert loads(" { a : 1 } ") == {"a": 1}
    assert loads("\n{\na\n:\n1\n}\n") == {"a": 1}
    assert loads("\t{\ta:\t1\t}\t") == {"a": 1}


# Comments
def test_parse_line_comments():
    # JSON5 feature
    assert loads("// comment\n{a: 1}") == {"a": 1}
    assert loads("{a: 1 // comment\n}") == {"a": 1}


def test_parse_block_comments():
    # JSON5 feature
    assert loads("/* comment */{a: 1}") == {"a": 1}
    assert loads("{a: /* comment */ 1}") == {"a": 1}


# Error cases
def test_invalid_json():
    with pytest.raises(DecodeError):
        loads("{")


def test_invalid_string():
    with pytest.raises(DecodeError):
        loads('"unclosed string')


# File loading tests
def test_load_from_file(tmp_path: Path):
    test_file = tmp_path / "test.json5"
    test_file.write_text('{"a": 1}')
    assert load(test_file) == {"a": 1}


def test_load_from_file_handle(tmp_path: Path):
    test_file = tmp_path / "test.json5"
    test_file.write_text('{"a": 1}')
    with open(test_file) as f:
        assert load(f) == {"a": 1}


# Input type tests
def test_bytes_input():
    assert loads(b'"hello"') == "hello"


def test_bytearray_input():
    assert loads(bytearray(b'"hello"')) == "hello"


# Complex nested structures
def test_nested_structures():
    data = """
    {
        array: [1, "2", true, null],
        object: {
            nested: {
                value: 42
            }
        },
        multiline_string: "hello\
world"
    }
    """
    expected = {
        "array": [1, "2", True, None],
        "object": {"nested": {"value": 42}},
        "multiline_string": "helloworld",
    }
    assert loads(data) == expected


# Special number formats (JSON5 features)
def test_special_numbers():
    assert loads("Infinity") == float("inf")
    assert loads("-Infinity") == float("-inf")
    assert loads("NaN") != loads("NaN")  # NaN is never equal to itself
    assert math.isnan(loads("NaN"))
    assert loads("+42") == 42  # Leading plus
    assert loads(".5") == 0.5  # Leading decimal point


def test_hex_numbers():
    assert loads("0xdeadbeef") == 0xDEADBEEF


KITCHEN_SINK = r"""
{
  // comments
  unquoted: 'and you can quote me on that',
  singleQuotes: 'I can use "double quotes" here',
  lineBreaks: "Look, Mom! \
No \\n's!",
  hexadecimal: 0xdecaf,
  leadingDecimalPoint: .8675309, andTrailing: 8675309.,
  positiveSign: +1,
  trailingComma: 'in objects', andIn: ['arrays',],
  "backwardsCompatible": "with JSON",
}
"""


def test_kitchen_sink():
    assert loads(KITCHEN_SINK) == {
        "unquoted": "and you can quote me on that",
        "singleQuotes": 'I can use "double quotes" here',
        "lineBreaks": r"Look, Mom! No \n's!",
        "hexadecimal": 0xDECAF,
        "leadingDecimalPoint": 0.8675309,
        "andTrailing": 8675309.0,
        "positiveSign": 1,
        "trailingComma": "in objects",
        "andIn": [
            "arrays",
        ],
        "backwardsCompatible": "with JSON",
    }
