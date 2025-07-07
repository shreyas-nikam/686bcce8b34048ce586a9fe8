
import pytest
import pandas as pd
import numpy as np

# Keep the <your_module> block as it is. DO NOT REPLACE or REMOVE the block.
from <your_module> import generate_synthetic_data

@pytest.mark.parametrize("num_samples", [0, 1, 10, 100])
def test_generate_synthetic_data_valid_structure_and_types(num_samples):
    """
    Tests that generate_synthetic_data returns a pandas DataFrame with the correct
    number of rows and expected columns, and that column dtypes are appropriate.
    Covers edge cases like 0 and 1 samples to ensure correct empty/single-row DataFrame handling.
    """
    df = generate_synthetic_data(num_samples)

    assert isinstance(df, pd.DataFrame), "Output must be a pandas DataFrame."
    assert len(df) == num_samples, f"DataFrame should have {num_samples} rows, but has {len(df)}."

    expected_columns = ['numeric_data', 'categorical_data', 'timestamp']
    for col in expected_columns:
        assert col in df.columns, f"DataFrame is missing expected column: '{col}'."

    # Verify column data types based on whether the DataFrame is empty or not.
    # For num_samples > 0, specific data types are expected.
    # For num_samples = 0, columns should still exist, and their dtypes might be
    # 'object' if not explicitly set, or the target dtype if the implementation
    # initializes empty Series with specific dtypes.
    if num_samples > 0:
        assert pd.api.types.is_numeric_dtype(df['numeric_data']), "numeric_data column must be numeric for non-empty DataFrame."
        assert pd.api.types.is_string_dtype(df['categorical_data']) or \
               pd.api.types.is_object_dtype(df['categorical_data']) or \
               pd.api.types.is_categorical_dtype(df['categorical_data']), \
               "categorical_data column must be string, object, or categorical for non-empty DataFrame."
        assert pd.api.types.is_datetime64_any_dtype(df['timestamp']), "timestamp column must be datetime for non-empty DataFrame."
    else:
        # For an empty DataFrame (num_samples=0), check for expected dtypes or object dtype as a fallback.
        # Pandas often defaults empty Series to 'object' dtype if not explicitly specified.
        assert df['numeric_data'].dtype in [np.dtype('float64'), np.dtype('int64'), np.dtype('object')], \
            "numeric_data column for empty DF should be numeric or object."
        assert df['categorical_data'].dtype == np.dtype('object') or pd.api.types.is_categorical_dtype(df['categorical_data']), \
            "categorical_data column for empty DF should be object or categorical."
        assert df['timestamp'].dtype in [np.dtype('datetime64[ns]'), np.dtype('object')], \
            "timestamp column for empty DF should be datetime64[ns] or object."


@pytest.mark.parametrize("invalid_input, expected_exception, error_message_match", [
    (-5, ValueError, "num_samples must be a non-negative integer"),
    (0.5, TypeError, "num_samples must be an integer"),
    ("invalid", TypeError, "num_samples must be an integer"),
    (None, TypeError, "num_samples must be an integer"),
    ([1, 2], TypeError, "num_samples must be an integer"),
])
def test_generate_synthetic_data_invalid_inputs_raise_errors(invalid_input, expected_exception, error_message_match):
    """
    Tests that generate_synthetic_data raises appropriate exceptions for invalid
    `num_samples` values (e.g., negative integers, non-integers, wrong types).
    """
    with pytest.raises(expected_exception, match=error_message_match):
        generate_synthetic_data(invalid_input)
