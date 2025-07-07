
import pandas as pd
import numpy as np
import datetime

def generate_synthetic_data(num_samples: int) -> pd.DataFrame:
    """
    Generates a synthetic pandas DataFrame to simulate diverse data characteristics for demonstration purposes.

    Arguments:
        num_samples (int): The number of rows to generate in the DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame with 'numeric_value', 'categorical_variable', 'time_series_data',
                          and 'text_description' columns.

    Raises:
        TypeError: If `num_samples` is not an integer.
        ValueError: If `num_samples` is a negative integer.
    """
    # --- Input Validation ---
    if not isinstance(num_samples, int):
        raise TypeError("num_samples must be an integer.")
    if num_samples < 0:
        raise ValueError("num_samples cannot be negative.")

    # --- Handle zero samples case explicitly ---
    # Return an empty DataFrame with the correct column names to satisfy test cases
    # regarding column presence and order for zero rows.
    if num_samples == 0:
        return pd.DataFrame(columns=['numeric_value', 'categorical_variable', 'time_series_data', 'text_description'])

    # --- Data Generation ---
    # 1. 'numeric_value': Random floats uniformly distributed between -100 and 100.
    numeric_values = np.random.uniform(-100.0, 100.0, num_samples)

    # 2. 'categorical_variable': Random choices from a predefined set of categories.
    categories = np.random.choice(['A', 'B', 'C'], size=num_samples)

    # 3. 'time_series_data': Random datetime objects within a range around the current date.
    #    Generate timestamps within +/- 3 years of the current date.
    base_timestamp = pd.Timestamp.now()
    # Random days between -3 years and +3 years (inclusive of 3 years)
    random_days = np.random.randint(-3 * 365, 3 * 365 + 1, num_samples)
    time_deltas = pd.to_timedelta(random_days, unit='D')
    time_series_data = base_timestamp + time_deltas

    # 4. 'text_description': Synthetic text descriptions.
    #    Combine a random phrase from a pool with a sequential index.
    text_phrase_pool = [
        "Data record {idx}.",
        "Sample {idx} observation.",
        "Entry {idx} details.",
        "Record {idx} information.",
        "Item {idx} description."
    ]
    text_descriptions = [
        np.random.choice(text_phrase_pool).format(idx=i + 1)
        for i in range(num_samples)
    ]

    # --- DataFrame Construction ---
    data = {
        'numeric_value': numeric_values,
        'categorical_variable': categories,
        'time_series_data': time_series_data,
        'text_description': text_descriptions
    }
    df = pd.DataFrame(data)

    return df


import pandas as pd
import numpy as np
import datetime

def generate_synthetic_data(num_samples: int) -> pd.DataFrame:
    """
    Generates a synthetic pandas DataFrame to simulate diverse data characteristics for demonstration purposes.

    Arguments:
        num_samples (int): The number of rows to generate in the DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame with 'numeric_value', 'categorical_variable', 'time_series_data',
                          and 'text_description' columns.

    Raises:
        TypeError: If `num_samples` is not an integer.
        ValueError: If `num_samples` is a negative integer.
    """
    # --- Input Validation ---
    if not isinstance(num_samples, int):
        raise TypeError("num_samples must be an integer.")
    if num_samples < 0:
        raise ValueError("num_samples cannot be negative.")

    # --- Handle zero samples case explicitly ---
    # Return an empty DataFrame with the correct column names to satisfy test cases
    # regarding column presence and order for zero rows.
    if num_samples == 0:
        return pd.DataFrame(columns=['numeric_value', 'categorical_variable', 'time_series_data', 'text_description'])

    # --- Data Generation ---
    # 1. 'numeric_value': Random floats uniformly distributed between -100 and 100.
    numeric_values = np.random.uniform(-100.0, 100.0, num_samples)

    # 2. 'categorical_variable': Random choices from a predefined set of categories.
    categories = np.random.choice(['A', 'B', 'C'], size=num_samples)

    # 3. 'time_series_data': Random datetime objects within a range around the current date.
    #    Generate timestamps within +/- 3 years of the current date.
    base_timestamp = pd.Timestamp.now()
    # Random days between -3 years and +3 years (inclusive of 3 years)
    random_days = np.random.randint(-3 * 365, 3 * 365 + 1, num_samples)
    time_deltas = pd.to_timedelta(random_days, unit='D')
    time_series_data = base_timestamp + time_deltas

    # 4. 'text_description': Synthetic text descriptions.
    #    Combine a random phrase from a pool with a sequential index.
    text_phrase_pool = [
        "Data record {idx}.",
        "Sample {idx} observation.",
        "Entry {idx} details.",
        "Record {idx} information.",
        "Item {idx} description."
    ]
    text_descriptions = [
        np.random.choice(text_phrase_pool).format(idx=i + 1)
        for i in range(num_samples)
    ]

    # --- DataFrame Construction ---
    data = {
        'numeric_value': numeric_values,
        'categorical_variable': categories,
        'time_series_data': time_series_data,
        'text_description': text_descriptions
    }
    df = pd.DataFrame(data)

    return df
