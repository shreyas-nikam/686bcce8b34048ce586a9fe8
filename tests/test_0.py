import pytest
import pandas as pd
import numpy as np
from definition_b4d3f9213f6d478cb5c2cf7e704eb3bb import generate_synthetic_data

# Define expected column names based on the specification
EXPECTED_COLUMNS = ['numeric_value', 'categorical_variable', 'time_series_data', 'text_description']

@pytest.mark.parametrize(
    "num_samples, expected_type, expected_rows, expected_exception",
    [
        # Valid cases: Positive integers and zero
        (0, pd.DataFrame, 0, None),
        (1, pd.DataFrame, 1, None),
        (10, pd.DataFrame, 10, None),
        (100, pd.DataFrame, 100, None),
        (1000, pd.DataFrame, 1000, None),

        # Invalid cases: Incorrect types for num_samples
        (5.5, None, None, TypeError),      # Float input
        ("ten", None, None, TypeError),    # String input
        ([5], None, None, TypeError),      # List input
        (None, None, None, TypeError),     # None input
        (True, None, None, TypeError),     # Boolean input
        ({}, None, None, TypeError),       # Dictionary input

        # Invalid cases: Negative integer for num_samples
        # A negative number of samples is typically not allowed for "number of rows".
        (-1, None, None, ValueError),
        (-10, None, None, ValueError),
    ]
)
def test_generate_synthetic_data_basic(num_samples, expected_type, expected_rows, expected_exception):
    """
    Tests the generate_synthetic_data function for various inputs,
    checking for correct return type, number of rows, and expected exceptions.
    """
    if expected_exception:
        with pytest.raises(expected_exception):
            generate_synthetic_data(num_samples)
    else:
        df = generate_synthetic_data(num_samples)

        # 1. Check if the returned object is a pandas DataFrame
        assert isinstance(df, expected_type), f"Expected type {expected_type}, got {type(df)}"

        # 2. Check if the DataFrame has the correct number of rows
        assert len(df) == expected_rows, f"Expected {expected_rows} rows, got {len(df)}"

        # 3. Check if all expected columns are present and in order
        assert list(df.columns) == EXPECTED_COLUMNS, \
            f"Expected columns {EXPECTED_COLUMNS}, got {list(df.columns)}"

        # 4. If the DataFrame is not empty, check column data types and content
        if expected_rows > 0:
            # Check data types of specific columns
            assert pd.api.types.is_numeric_dtype(df['numeric_value']), \
                "Expected 'numeric_value' to be numeric"
            assert pd.api.types.is_object_dtype(df['categorical_variable']) or \
                   pd.api.types.is_string_dtype(df['categorical_variable']), \
                "Expected 'categorical_variable' to be object/string"
            assert pd.api.types.is_datetime64_any_dtype(df['time_series_data']), \
                "Expected 'time_series_data' to be datetime"
            assert pd.api.types.is_object_dtype(df['text_description']) or \
                   pd.api.types.is_string_dtype(df['text_description']), \
                "Expected 'text_description' to be object/string"

            # Check that generated data is not all null (i.e., data was actually generated)
            assert not df['numeric_value'].isnull().all(), "'numeric_value' column should not be all null"
            assert not df['categorical_variable'].isnull().all(), "'categorical_variable' column should not be all null"
            assert not df['time_series_data'].isnull().all(), "'time_series_data' column should not be all null"
            assert not df['text_description'].isnull().all(), "'text_description' column should not be all null"

            # Based on the spec, 'categorical_variable' is a random choice from 'A', 'B', 'C'.
            # Ensure generated categories are within this expected set or not empty.
            unique_categories = df['categorical_variable'].unique()
            # If the number of samples is small, not all categories might appear,
            # but they should at least be valid or the column shouldn't be empty.
            if len(unique_categories) > 0:
                assert all(cat in ['A', 'B', 'C'] for cat in unique_categories), \
                    f"Unexpected values in 'categorical_variable': {unique_categories}"

            # Check the range/characteristics of numeric data (conceptual, assuming standard ranges)
            # This is a loose check as exact ranges are not specified in the docstring.
            # It just ensures values are not extremely out of bounds if they were meant to be e.g. 0-1.
            assert df['numeric_value'].min() >= -1000 and df['numeric_value'].max() <= 1000, \
                "Numeric values seem out of a reasonable synthetic range (-1000 to 1000)"

            # Check time series data for logical progression (e.g., within a reasonable date range)
            # Assuming current year +/- a few years or recent past, but not decades in future/past.
            # This is a weak check, a stronger check would depend on the implementation.
            current_year = pd.Timestamp.now().year
            assert df['time_series_data'].min().year >= current_year - 5 and \
                   df['time_series_data'].max().year <= current_year + 5, \
                "Time series data dates seem outside a reasonable range (current_year +/- 5 years)"

