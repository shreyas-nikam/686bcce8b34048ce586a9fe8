import pytest
import pandas as pd
# Assuming the module where generate_synthetic_data is defined is called 'your_module'
from definition_a4ad88193db54f36a6c1e956018c4dfd import generate_synthetic_data

@pytest.mark.parametrize(
    "num_samples, expected_rows, expected_exception, expected_column_names",
    [
        # Valid cases for num_samples
        (0, 0, None, ['numeric_data_1', 'numeric_data_2', 'categorical_data', 'timestamp_data']),
        (1, 1, None, ['numeric_data_1', 'numeric_data_2', 'categorical_data', 'timestamp_data']),
        (5, 5, None, ['numeric_data_1', 'numeric_data_2', 'categorical_data', 'timestamp_data']),
        (100, 100, None, ['numeric_data_1', 'numeric_data_2', 'categorical_data', 'timestamp_data']),

        # Invalid input types for num_samples (TypeError)
        ("invalid_string", None, TypeError, None),
        (5.5, None, TypeError, None),
        (None, None, TypeError, None),
        ([1, 2, 3], None, TypeError, None),
        ({'a': 1}, None, TypeError, None),

        # Invalid value for num_samples (ValueError for negative)
        (-1, None, ValueError, None),
        (-10, None, ValueError, None),
    ]
)
def test_generate_synthetic_data(num_samples, expected_rows, expected_exception, expected_column_names):
    if expected_exception:
        # Test for expected exceptions when invalid input is provided
        with pytest.raises(expected_exception):
            generate_synthetic_data(num_samples)
    else:
        # Test for valid outputs
        df = generate_synthetic_data(num_samples)

        # 1. Verify the return type is a pandas DataFrame
        assert isinstance(df, pd.DataFrame)

        # 2. Verify the number of rows matches num_samples
        assert len(df) == expected_rows

        # 3. Verify the presence and count of expected columns
        # The specific column names are assumed based on the specification's description
        # of numeric, categorical, and time-series data.
        assert all(col in df.columns for col in expected_column_names)
        assert len(df.columns) == len(expected_column_names)

        # 4. Verify the data types of the columns (only if DataFrame is not empty)
        if expected_rows > 0:
            # Check numeric columns
            assert pd.api.types.is_numeric_dtype(df['numeric_data_1'])
            assert pd.api.types.is_numeric_dtype(df['numeric_data_2'])
            
            # Check categorical column (can be object or specific 'category' dtype)
            assert pd.api.types.is_string_dtype(df['categorical_data']) or \
                   pd.api.types.is_object_dtype(df['categorical_data']) or \
                   df['categorical_data'].dtype == 'category'

            # Check time-series column
            assert pd.api.types.is_datetime64_any_dtype(df['timestamp_data'])

        # 5. Optional: Check for non-null values in columns if num_samples > 0
        if expected_rows > 0:
            assert not df.isnull().any().any()