
import pandas as pd
import numpy as np
from typing import Dict, Any, Union

def generate_synthetic_data(
    num_records: int,
    include_text: bool,
    include_numeric: bool,
    include_categorical: bool
) -> pd.DataFrame:
    """
    Generates a synthetic dataset for simulation purposes, containing a mix of text,
    numerical, and categorical data points.

    Args:
        num_records (int): The number of records/rows to generate in the dataset.
        include_text (bool): Whether to include simulated text data.
        include_numeric (bool): Whether to include simulated numerical data.
        include_categorical (bool): Whether to include simulated categorical data.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the synthetic data.

    Raises:
        TypeError: If `num_records` is not an integer, or if `include_text`,
                   `include_numeric`, or `include_categorical` are not booleans.
        ValueError: If `num_records` is negative.
    """
    # --- Input Validation ---
    if not isinstance(num_records, int):
        raise TypeError("num_records must be an integer.")
    if num_records < 0:
        raise ValueError("num_records cannot be negative.")

    if not isinstance(include_text, bool):
        raise TypeError("include_text must be a boolean.")
    if not isinstance(include_numeric, bool):
        raise TypeError("include_numeric must be a boolean.")
    if not isinstance(include_categorical, bool):
        raise TypeError("include_categorical must be a boolean.")

    # --- Data Generation Logic ---
    data: Dict[str, np.ndarray] = {}

    if include_text:
        # Generate varied text data using a simple pattern and index
        # This ensures unique strings for each record and avoids external dependencies.
        text_data = np.array([f"synthetic_text_{i:05d}" for i in range(num_records)], dtype=str)
        data['text_data'] = text_data

    if include_numeric:
        # Generate random float data between 0.0 and 100.0
        numeric_data = np.random.rand(num_records) * 100.0
        data['numeric_data'] = numeric_data

    if include_categorical:
        # Generate categorical data by randomly selecting from a predefined set
        categories = ['CategoryA', 'CategoryB', 'CategoryC', 'CategoryD', 'CategoryE']
        categorical_data = np.random.choice(categories, size=num_records)
        data['categorical_data'] = categorical_data

    # --- DataFrame Construction ---
    if num_records == 0:
        # If 0 records are requested, return an empty DataFrame (0 rows, 0 columns)
        return pd.DataFrame()
    elif not data:
        # If no data types are requested but num_records > 0, return a DataFrame
        # with num_records rows and 0 columns (i.e., an index only).
        return pd.DataFrame(index=range(num_records))
    else:
        # Construct DataFrame from the generated data dictionary
        return pd.DataFrame(data)



import pandas as pd
import numpy as np
from typing import Dict, Any, Union

def generate_synthetic_data(
    num_records: int,
    include_text: bool,
    include_numeric: bool,
    include_categorical: bool
) -> pd.DataFrame:
    """
    Generates a synthetic dataset for simulation purposes, containing a mix of text,
    numerical, and categorical data points.

    Args:
        num_records (int): The number of records/rows to generate in the dataset.
        include_text (bool): Whether to include simulated text data.
        include_numeric (bool): Whether to include simulated numerical data.
        include_categorical (bool): Whether to include simulated categorical data.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the synthetic data.

    Raises:
        TypeError: If `num_records` is not an integer, or if `include_text`,
                   `include_numeric`, or `include_categorical` are not booleans.
        ValueError: If `num_records` is negative.
    """
    # --- Input Validation ---
    if not isinstance(num_records, int):
        raise TypeError("num_records must be an integer.")
    if num_records < 0:
        raise ValueError("num_records cannot be negative.")

    if not isinstance(include_text, bool):
        raise TypeError("include_text must be a boolean.")
    if not isinstance(include_numeric, bool):
        raise TypeError("include_numeric must be a boolean.")
    if not isinstance(include_categorical, bool):
        raise TypeError("include_categorical must be a boolean.")

    # --- Data Generation Logic ---
    data: Dict[str, np.ndarray] = {}

    if include_text:
        # Generate varied text data using a simple pattern and index
        # This ensures unique strings for each record and avoids external dependencies.
        text_data = np.array([f"synthetic_text_{i:05d}" for i in range(num_records)], dtype=str)
        data['text_data'] = text_data

    if include_numeric:
        # Generate random float data between 0.0 and 100.0
        numeric_data = np.random.rand(num_records) * 100.0
        data['numeric_data'] = numeric_data

    if include_categorical:
        # Generate categorical data by randomly selecting from a predefined set
        categories = ['CategoryA', 'CategoryB', 'CategoryC', 'CategoryD', 'CategoryE']
        categorical_data = np.random.choice(categories, size=num_records)
        data['categorical_data'] = categorical_data

    # --- DataFrame Construction ---
    if num_records == 0:
        # If 0 records are requested, return an empty DataFrame (0 rows, 0 columns)
        return pd.DataFrame()
    elif not data:
        # If no data types are requested but num_records > 0, return a DataFrame
        # with num_records rows and 0 columns (i.e., an index only).
        return pd.DataFrame(index=range(num_records))
    else:
        # Construct DataFrame from the generated data dictionary
        return pd.DataFrame(data)

