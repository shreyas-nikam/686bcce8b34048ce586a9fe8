import pytest
import pandas as pd
from definition_d13b34bf64a74ea2b126989ebf1703ca import generate_synthetic_data

@pytest.mark.parametrize("num_samples", [
    1, 5, 100, # Standard positive integers
    True       # As bool is subclass of int, True evaluates to 1
])
def test_generate_synthetic_data_valid_positive_inputs(num_samples):
    df = generate_synthetic_data(num_samples)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == num_samples

    # Based on the specification, expect these general types of columns
    expected_columns = ['numeric_data', 'categorical_data', 'time_series_data']
    assert all(col in df.columns for col in expected_columns)

    # Check column data types for non-empty DataFrame
    if num_samples > 0:
        assert pd.api.types.is_numeric_dtype(df['numeric_data'])
        assert pd.api.types.is_string_dtype(df['categorical_data']) or pd.api.types.is_categorical_dtype(df['categorical_data'])
        assert pd.api.types.is_datetime64_any_dtype(df['time_series_data'])

@pytest.mark.parametrize("num_samples", [
    0,     # Zero samples
    False  # As bool is subclass of int, False evaluates to 0
])
def test_generate_synthetic_data_zero_samples_inputs(num_samples):
    df = generate_synthetic_data(num_samples)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0

    expected_columns = ['numeric_data', 'categorical_data', 'time_series_data']
    assert all(col in df.columns for col in expected_columns)
    # For 0-row DataFrames, dtypes are typically 'object' or inferred from potential column creation logic.
    # The main check is that columns exist and the frame is empty.

@pytest.mark.parametrize("invalid_input, expected_exception", [
    (-1, ValueError),      # Negative integer should raise ValueError
    (10.5, TypeError),     # Float is not an integer
    ("abc", TypeError),    # String is not an integer
    ([1, 2], TypeError),   # List is not an integer
    ({'a': 1}, TypeError), # Dictionary is not an integer
    (None, ValueError)     # None is not an integer. Following the example's pattern for None, treat as ValueError.
])
def test_generate_synthetic_data_invalid_inputs(invalid_input, expected_exception):
    with pytest.raises(expected_exception):
        generate_synthetic_data(invalid_input)