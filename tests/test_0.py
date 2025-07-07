import pytest
from definition_cc53a0709a57434c8fd1f04040087497 import create_symai_symbol

# Mock the symai.Symbol class for testing purposes.
# This mock is essential because `symai` might not be installed in the test environment,
# and it defines the expected interface (`.value` attribute) and behavior (`__eq__`).
# In a real test setup where `symai` is installed, you would import `symai.Symbol` directly
# and the function `create_symai_symbol` would return an instance of that actual class.
class MockSymaiSymbol:
    def __init__(self, data):
        # Use a non-public attribute name to mimic the internal storage of the wrapped data.
        # symai.Symbol instances typically expose this data via a `.value` property.
        self._value = data 

    @property
    def value(self):
        # This property mimics how symai.Symbol allows access to its wrapped data.
        return self._value

    def __eq__(self, other):
        # Defines equality for MockSymaiSymbol instances.
        # This allows direct comparison like `symbol_obj == expected_symbol_obj` in tests.
        if isinstance(other, MockSymaiSymbol):
            return self.value == other.value
        # If the actual symai.Symbol supports comparison with raw data directly,
        # this could be extended: `return self.value == other`
        return NotImplemented # Delegate to other's __eq__ or fall back to default comparison

    def __repr__(self):
        return f"MockSymaiSymbol(value={self.value!r})"

# Define a dummy custom class for testing an unsupported object type.
# This helps ensure that arbitrary complex objects are not silently accepted or cause errors.
class MyCustomClass:
    def __init__(self, value="custom_data"):
        self.value = value
    
    def __repr__(self):
        return f"MyCustomClass(value={self.value!r})"

@pytest.mark.parametrize("input_data, expected", [
    # --- Valid Text (string) Inputs ---
    ("Hello World", MockSymaiSymbol("Hello World")),
    ("", MockSymaiSymbol("")), # Empty string
    ("   Text with leading and trailing spaces   ", MockSymaiSymbol("   Text with leading and trailing spaces   ")),
    ("Multi-line\nText\tWithTabs", MockSymaiSymbol("Multi-line\nText\tWithTabs")),
    ("!@#$%^&*()_+", MockSymaiSymbol("!@#$%^&*()_+")), # String with special characters

    # --- Valid Numeric Inputs (int, float) ---
    (123, MockSymaiSymbol(123)), # Positive integer
    (0, MockSymaiSymbol(0)),     # Zero integer
    (-456, MockSymaiSymbol(-456)), # Negative integer
    (3.14159, MockSymaiSymbol(3.14159)), # Positive float
    (0.0, MockSymaiSymbol(0.0)),         # Zero float
    (-2.718, MockSymaiSymbol(-2.718)),   # Negative float
    (float('inf'), MockSymaiSymbol(float('inf'))), # Infinity
    (float('-inf'), MockSymaiSymbol(float('-inf'))), # Negative Infinity
    (float('nan'), MockSymaiSymbol(float('nan'))), # NaN (Note: NaN == NaN is false, but MockSymaiSymbol should wrap correctly)

    # --- Valid List Inputs ---
    ([1, 2, 3], MockSymaiSymbol([1, 2, 3])), # List of integers
    (["apple", "banana", "cherry"], MockSymaiSymbol(["apple", "banana", "cherry"])), # List of strings
    ([1, "text", True, 3.14, None], MockSymaiSymbol([1, "text", True, 3.14, None])), # Mixed-type list
    ([], MockSymaiSymbol([])), # Empty list
    ([[1, 2], ["a", "b"], [True, False]], MockSymaiSymbol([[1, 2], ["a", "b"], [True, False]])), # Nested list

    # --- Other Commonly Supported Basic Python Types ---
    (True, MockSymaiSymbol(True)), # Boolean True
    (False, MockSymaiSymbol(False)), # Boolean False
    ({"key1": "value1", "key2": 123}, MockSymaiSymbol({"key1": "value1", "key2": 123})), # Dictionary
    ({}, MockSymaiSymbol({})), # Empty dictionary
    (None, MockSymaiSymbol(None)), # None type
    ((1, 2, "three"), MockSymaiSymbol((1, 2, "three"))), # Tuple
    ({1, 2, 3}, MockSymaiSymbol({1, 2, 3})), # Set (note: set equality is order-independent)
    (frozenset({1, 2}), MockSymaiSymbol(frozenset({1, 2}))), # Frozenset

    # --- Invalid / Unsupported Types (Expecting Exceptions) ---
    # The docstring explicitly lists "string, int, float, list" as examples.
    # Complex, non-serializable, or executable objects are typically not wrapped directly
    # and should result in a TypeError or ValueError.
    (object(), TypeError), # A generic instance of `object`
    (type, TypeError), # A type object (e.g., `int`, `str`, `list`, `dict`)
    (lambda x: x, TypeError), # A lambda function
    (create_symai_symbol, TypeError), # A reference to the function itself
    (pytest, TypeError), # A module object (e.g., `pytest`, `os`, `sys`)
    (MyCustomClass(), TypeError), # An instance of a custom class
])
def test_create_symai_symbol(input_data, expected):
    """
    Test cases for `create_symai_symbol` function.
    It covers various valid data types (text, numbers, lists, etc.)
    and handles invalid data types by expecting specific exceptions.
    """
    try:
        result_symbol = create_symai_symbol(input_data)
        
        # Assert that the function returned an instance of our MockSymaiSymbol.
        # In a real environment with `symai` installed, this would be
        # `assert isinstance(result_symbol, symai.Symbol)`.
        assert isinstance(result_symbol, MockSymaiSymbol)
        
        # Assert that the MockSymaiSymbol's wrapped value matches the expected value.
        # This leverages the __eq__ method of MockSymaiSymbol for direct comparison.
        # Explicitly checking `.value` also ensures the correct data is encapsulated.
        assert result_symbol == expected
        assert result_symbol.value == expected.value
        
        # Special check for NaN: float('nan') == float('nan') is False, so we check using math.isnan
        if isinstance(input_data, float) and input_data != input_data: # Checks for NaN
            import math
            assert math.isnan(result_symbol.value)
            assert math.isnan(expected.value) # Expected must also be NaN

    except Exception as e:
        # If an exception is expected, assert that the raised exception is of the expected type.
        assert isinstance(e, expected)