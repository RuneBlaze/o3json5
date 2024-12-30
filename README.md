# O3JSON5

A fast JSON5 parser for Python, written in Rust 🦀

## Features

- Full JSON5 support (comments, trailing commas, unquoted keys, etc.)
- Simple, Pythonic API
- Fast performance (up to 100x faster than pure Python implementations)
- Type hints included

Heavy-lifting done by https://github.com/callum-oakley/json5-rs in Rust.

## Installation

```bash
pip install o3json5 # or use uv, pdm, poetry, etc. your favorite package manager
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

## Benchmarks

O3JSON5 is significantly faster than pure Python JSON5 implementations, approaching native JSON speeds. Click below for detailed benchmarks.

<details>
<summary>View detailed benchmark results</summary>

```
> python examples/bench.py
Generating test data and running benchmarks...


Benchmarking with approximate 10,000 bytes of data
------------------------------------------------------------
Actual file size: 4,459 bytes
      json: 0.04ms ± 0.01ms
     json5: 40.28ms ± 1.03ms
   o3json5: 0.35ms ± 0.18ms


Benchmarking with approximate 100,000 bytes of data
------------------------------------------------------------
Actual file size: 43,416 bytes
      json: 0.28ms ± 0.02ms
     json5: 383.36ms ± 3.38ms
   o3json5: 2.72ms ± 0.11ms


Benchmarking with approximate 1,000,000 bytes of data
------------------------------------------------------------
Actual file size: 435,373 bytes
      json: 2.94ms ± 0.13ms
     json5: 3870.65ms ± 28.20ms
   o3json5: 28.32ms ± 0.10ms
```

</details>

Note: micro-benchmarks don't say much, and we are already doing JSON5 -> Rust in-memory data structures -> Python in-memory data structures -- while the performance can be further improved, for most use cases, the performance is already good enough.

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
