import o3json5

# Basic usage - parsing a JSON5 string
json5_str = """{
    // This is a JSON5 comment
    name: 'Example',
    numbers: [1, 2, 3],
    details: {
        active: true,
        ratio: .5,      // Trailing comma is OK
    },
}"""

try:
    data = o3json5.loads(json5_str)
    print("Parsed JSON5:")
    print(f"- Name: {data['name']}")
    print(f"- Numbers: {data['numbers']}")
    print(f"- Active: {data['details']['active']}")
    print(f"- Ratio: {data['details']['ratio']}")
except o3json5.DecodeError as e:
    print(f"Failed to parse JSON5: {e}")

# Demonstrating error handling with invalid JSON5
invalid_json5 = """{
    unterminated: "string
}"""

try:
    o3json5.loads(invalid_json5)
except o3json5.DecodeError as e:
    print(f"\nExpected error with invalid JSON5:")
    print(f"DecodeError: {e}")
