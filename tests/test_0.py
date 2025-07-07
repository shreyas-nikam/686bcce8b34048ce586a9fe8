import pytest
import pandas as pd
import numpy as np # Often used by pandas for numerical data under the hood

from definition_cb512fb92bd94218aeccc05ec3e48a50 import generate_synthetic_data

@pytest.mark.parametrize(
    "num_records, include_text, include_numeric, include_categorical, expected_cols_list, expected_exception",
    [
        # --- Valid Combinations (Positive Tests) ---
        # 1. All data types included
        (5, True, True, True, ['text_data', 'numeric_data', 'categorical_data'], None),
        # 2. Only text data
        (1, True, False, False, ['text_data'], None),
        # 3. Only numeric data
        (10, False, True, False, ['numeric_data'], None),
        # 4. Only categorical data
        (3, False, False, True, ['categorical_data'], None),
        # 5. Text and Numeric data
        (5, True, True, False, ['text_data', 'numeric_data'], None),
        # 6. Text and Categorical data
        (5, True, False, True, ['text_data', 'categorical_data'], None),
        # 7. Numeric and Categorical data
        (5, False, True, True, ['numeric_data', 'categorical_data'], None),

        # --- Edge Cases for num_records ---
        # 8. num_records = 0: Should result in an empty DataFrame (0 rows, 0 columns)
        (0, True, True, True, [], None),
        (0, False, False, False, [], None), # 0 records, no types requested
        # 9. No data types requested, but num_records > 0: Should result in DataFrame with num_records rows and 0 columns
        (5, False, False, False, [], None),

        # --- Invalid num_records (Negative Tests) ---
        # 10. num_records < 0 should raise ValueError
        (-1, True, True, True, None, ValueError),
        # 11. num_records is not an integer should raise TypeError
        (1.5, True, True, True, None, TypeError),
        ("5", True, True, True, None, TypeError),
        (None, True, True, True, None, TypeError),

        # --- Invalid include_x flags (Negative Tests) ---
        # 12. include_text is not a boolean
        (5, "True", True, True, None, TypeError),
        (5, 0, True, True, None, TypeError), 
        (5, None, True, True, None, TypeError),
        # 13. include_numeric is not a boolean
        (5, True, 1, True, None, TypeError),
        (5, True, "False", True, None, TypeError),
        (5, True, None, True, None, TypeError),
        # 14. include_categorical is not a boolean
        (5, True, True, "False", None, TypeError),
        (5, True, True, 0, None, TypeError),
        (5, True, True, None, None, TypeError),
    ]
)
def test_generate_synthetic_data(num_records, include_text, include_numeric, include_categorical, expected_cols_list, expected_exception):
    if expected_exception:
        # Test cases where an exception (e.g., TypeError, ValueError) is expected
        with pytest.raises(expected_exception):
            generate_synthetic_data(num_records, include_text, include_numeric, include_categorical)
    else:
        # Test cases where a pandas DataFrame is expected
        df = generate_synthetic_data(num_records, include_text, include_numeric, include_categorical)

        # 1. Verify the return type is a pandas.DataFrame
        assert isinstance(df, pd.DataFrame)

        # 2. Verify the number of rows in the DataFrame
        assert len(df) == num_records

        # 3. Verify the columns based on num_records and include flags
        if num_records == 0:
            # If 0 records are requested, the DataFrame should have 0 columns regardless of include flags
            assert len(df.columns) == 0
            assert df.empty
        elif not include_text and not include_numeric and not include_categorical:
            # If no data types are requested (and num_records > 0), the DataFrame should have 0 columns
            assert len(df.columns) == 0
            # But still should have num_records rows (an index with num_records entries)
            assert len(df) == num_records
        else:
            # For valid cases with data types requested, check that only the expected columns are present
            assert sorted(df.columns.tolist()) == sorted(expected_cols_list)

            # 4. Verify data types and non-emptiness of included columns (for num_records > 0)
            if num_records > 0:
                if 'text_data' in df.columns:
                    # Text data is typically 'object' or 'string' dtype in pandas
                    assert pd.api.types.is_object_dtype(df['text_data']) or pd.api.types.is_string_dtype(df['text_data'])
                    assert not df['text_data'].empty
                    assert not df['text_data'].isnull().all() # Ensure column is not entirely NaN
                if 'numeric_data' in df.columns:
                    # Numeric data can be int, float, etc.
                    assert pd.api.types.is_numeric_dtype(df['numeric_data'])
                    assert not df['numeric_data'].empty
                    assert not df['numeric_data'].isnull().all()
                if 'categorical_data' in df.columns:
                    # Categorical data can be 'object' or pandas 'CategoricalDtype'
                    assert pd.api.types.is_object_dtype(df['categorical_data']) or pd.api.types.is_categorical_dtype(df['categorical_data'])
                    assert not df['categorical_data'].empty
                    assert not df['categorical_data'].isnull().all()
