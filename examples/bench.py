import json
import json5
import o3json5
import time
import random
import statistics
from pathlib import Path
from typing import Any, Dict, List


def generate_complex_json(size: int = 10000) -> Dict[str, Any]:
    """Generate a complex JSON structure of approximately given size."""
    data = {
        "string_field": "Hello" * (size // 100),
        "number_field": 12345.6789,
        "scientific": 1.23e-4,
        "boolean_field": True,
        "null_field": None,
        "array_of_numbers": [random.random() for _ in range(size // 100)],
        "nested_objects": [],
    }

    # Add nested objects to increase complexity
    for i in range(size // 1000):
        nested = {
            "id": i,
            "name": f"Object {i}",
            "values": [random.randint(1, 1000) for _ in range(10)],
            "metadata": {
                "created": "2024-03-14T12:00:00Z",
                "tags": ["test", "benchmark", str(i)],
            },
        }
        data["nested_objects"].append(nested)

    return data


def benchmark_parser(parser, data: str, iterations: int = 5) -> List[float]:
    """Benchmark a parser's performance."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        parser(data)
        end = time.perf_counter()
        times.append(end - start)
    return times


def format_stats(times: List[float]) -> str:
    """Format timing statistics."""
    mean = statistics.mean(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0
    return f"{mean*1000:.2f}ms ± {stdev*1000:.2f}ms"


def main():
    # Create benchmark directory if it doesn't exist
    bench_dir = Path("benchmark_data")
    bench_dir.mkdir(exist_ok=True)

    # Test different sizes
    sizes = [10_000, 100_000, 1_000_000]

    print("Generating test data and running benchmarks...\n")

    for size in sizes:
        print(f"\nBenchmarking with approximate {size:,} bytes of data")
        print("-" * 60)

        # Generate and save test data
        data = generate_complex_json(size)
        test_file = bench_dir / f"test_data_{size}.json"

        with open(test_file, "w") as f:
            json.dump(data, f)

        # Read the file content
        with open(test_file, "r") as f:
            content = f.read()

        actual_size = len(content)
        print(f"Actual file size: {actual_size:,} bytes")

        # Benchmark each parser
        parsers = {"json": json.loads, "json5": json5.loads, "o3json5": o3json5.loads}

        results = {}
        for name, parser in parsers.items():
            try:
                times = benchmark_parser(parser, content)
                results[name] = format_stats(times)
                print(f"{name:>10}: {results[name]}")
            except Exception as e:
                print(f"{name:>10}: Error - {str(e)}")

        print()


if __name__ == "__main__":
    main()
