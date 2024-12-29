# O3JSON5

A fast JSON5 parser for Python, written in Rust 🦀

## Features

- Full JSON5 support (comments, trailing commas, unquoted keys, etc.)
- Simple, Pythonic API
- Blazing fast performance (see benchmarks below)
- Type hints included

Heavy-lifting done by https://github.com/callum-oakley/json5-rs in Rust.

## Installation

```bash
pip install o3json5
```

## Quick Start

```python
import o3json5

# Parse JSON5 with comments and modern features
json5_str = '''{ 
    // Comments are supported!
    name: 'O3JSON5',
    features: [
        'Fast',
        'Simple',
        'Reliable',
    ],
    performance: {
        isFast: true,
        speedRatio: .95, // Decimal points can start with .
    },
}'''

data = o3json5.loads(json5_str)
print(f"Name: {data['name']}")
```

## Reference

### Functions

- `loads(s: Union[str, bytes, bytearray]) -> Any`
  - Parses a JSON5 string or bytes-like object
  - Raises `DecodeError` if input is invalid JSON5
  - Raises `TypeError` if input type is not supported

- `load(fp: Union[str, Path, TextIO]) -> Any`
  - Parses JSON5 from a file path or file-like object
  - Accepts string path, Path object, or file-like object
  - Raises `DecodeError`, `TypeError`, or `OSError`

### Exceptions

- `DecodeError`
  - Subclass of `ValueError`
  - Raised when JSON5 parsing fails
  - Contains error message with details

That's it! Simple, fast, and reliable JSON5 parsing. 🚀

