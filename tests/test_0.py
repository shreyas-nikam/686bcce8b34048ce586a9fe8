import pytest
import numpy as np

# DO NOT REPLACE or REMOVE the block below
# definition_e99705428fe7486aa29011b7090117b8
class MockModule:
    def generate_multivariate_normal_samples(mean, cov, n_samples, n_dims):
        """
        Mock implementation to simulate the behavior of generate_multivariate_normal_samples
        for testing purposes, including expected error handling.
        """
        # --- Type and Value Validation ---
        if not isinstance(mean, np.ndarray) or not isinstance(cov, np.ndarray):
            raise TypeError("Mean and covariance must be numpy arrays.")
        if not isinstance(n_samples, int) or not isinstance(n_dims, int):
            raise TypeError("n_samples and n_dims must be integers.")

        if n_samples < 0:
            raise ValueError("n_samples must be non-negative.")
        # A multivariate normal distribution inherently has at least 1 dimension
        if n_dims < 1:
            raise ValueError("n_dims must be at least 1.")

        # --- Shape Validation ---
        if mean.ndim != 1 or mean.shape[0] != n_dims:
            raise ValueError(f"Mean vector must be 1-dimensional and have shape ({n_dims},). Got shape {mean.shape}.")
        if cov.ndim != 2 or cov.shape != (n_dims, n_dims):
            raise ValueError(f"Covariance matrix must be 2-dimensional and have shape ({n_dims}, {n_dims}). Got shape {cov.shape}.")

        # --- Covariance Matrix Properties Validation (mimicking numpy/scipy behavior) ---
        # Check for symmetry
        if not np.allclose(cov, cov.T):
            raise np.linalg.LinAlgError("Covariance matrix must be symmetric.")
        
        # Check for positive semi-definiteness
        try:
            # np.linalg.cholesky requires positive definite, adding a small epsilon
            # to handle numerically singular but theoretically valid semi-definite matrices.
            # If it still fails, it's likely not positive semi-definite enough for sampling.
            np.linalg.cholesky(cov + 1e-10 * np.eye(n_dims)) 
        except np.linalg.LinAlgError:
            raise np.linalg.LinAlgError("Covariance matrix is not positive semi-definite.")

        # --- Sample Generation ---
        if n_samples == 0:
            return np.empty((0, n_dims), dtype=np.float64) # Ensure float dtype for consistency

        try:
            samples = np.random.multivariate_normal(mean, cov, size=n_samples)
            # Ensure output shape is (n_samples, n_dims) even for n_dims=1 where numpy might return (n_samples,)
            if n_dims == 1 and samples.ndim == 1:
                samples = samples.reshape(-1, 1)
            return samples
        except Exception as e:
            # Re-raise any unexpected errors during numpy generation
            raise RuntimeError(f"An unexpected error occurred during sample generation: {e}")

generate_multivariate_normal_samples = MockModule.generate_multivariate_normal_samples
# </your_module>


@pytest.mark.parametrize("mean, cov, n_samples, n_dims, expected_shape, expected_exception", [
    # --- Happy Path / Valid Inputs ---
    # 2D case, standard
    (np.array([0, 0]), np.array([[1, 0.5], [0.5, 1]]), 100, 2, (100, 2), None),
    # 1D case
    (np.array([5]), np.array([[1.0]]), 50, 1, (50, 1), None),
    # Higher dimension (3D)
    (np.array([1, 2, 3]), np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 200, 3, (200, 3), None),
    # Different number of samples
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), 10, 2, (10, 2), None),
    # Single sample
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), 1, 2, (1, 2), None),
    # Zero samples (should return empty array of correct shape and dtype)
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), 0, 2, (0, 2), None),
    # Identity covariance
    (np.array([0, 0]), np.eye(2), 100, 2, (100, 2), None),
    # Diagonal covariance
    (np.array([0, 0]), np.diag([2, 3]), 100, 2, (100, 2), None),

    # --- Edge Cases / Invalid Argument Values ---
    # n_samples is negative
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), -10, 2, None, ValueError),
    # n_dims is zero (not valid for a multivariate distribution)
    (np.array([]), np.array([[]]), 10, 0, None, ValueError),
    # n_dims is negative
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), 10, -2, None, ValueError),

    # --- Type Errors for Inputs ---
    # mean not a numpy array
    ([0, 0], np.array([[1, 0], [0, 1]]), 100, 2, None, TypeError),
    # cov not a numpy array
    (np.array([0, 0]), [[1, 0], [0, 1]], 100, 2, None, TypeError),
    # mean is None
    (None, np.array([[1, 0], [0, 1]]), 100, 2, None, TypeError),
    # cov is None
    (np.array([0, 0]), None, 100, 2, None, TypeError),
    # n_samples not an int
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), 100.5, 2, None, TypeError),
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), "100", 2, None, TypeError),
    # n_dims not an int
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), 100, 2.0, None, TypeError),
    (np.array([0, 0]), np.array([[1, 0], [0, 1]]), 100, "2", None, TypeError),

    # --- Shape/Dimension Mismatch Errors ---
    # mean.ndim is not 1 (e.g., 2D mean vector)
    (np.array([[0, 0]]), np.array([[1, 0], [0, 1]]), 100, 2, None, ValueError), 
    # mean.shape[0] != n_dims
    (np.array([0]), np.array([[1, 0], [0, 1]]), 100, 2, None, ValueError), # mean 1D, n_dims 2
    (np.array([0, 0, 0]), np.array([[1, 0], [0, 1]]), 100, 2, None, ValueError), # mean 3D, n_dims 2
    # cov.ndim is not 2 (e.g., 1D cov vector)
    (np.array([0, 0]), np.array([1, 0]), 100, 2, None, ValueError), 
    # cov is not square
    (np.array([0, 0]), np.array([[1, 0, 0], [0, 1, 0]]), 100, 2, None, ValueError), # 2x3 cov
    # cov dimensions don't match n_dims
    (np.array([0, 0]), np.array([[1.0]]), 100, 2, None, ValueError), # cov 1x1, n_dims 2
    (np.array([0, 0, 0]), np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 100, 2, None, ValueError), # n_dims 2, cov 3x3

    # --- Covariance Matrix Property Errors ---
    # Covariance matrix not symmetric
    (np.array([0, 0]), np.array([[1, 2], [3, 4]]), 100, 2, None, np.linalg.LinAlgError),
    # Covariance matrix is singular/degenerate (all zeros)
    (np.array([0, 0]), np.array([[0, 0], [0, 0]]), 100, 2, None, np.linalg.LinAlgError),
    # Covariance matrix not positive semi-definite (e.g., negative eigenvalue)
    (np.array([0, 0]), np.array([[-1, 0], [0, -1]]), 100, 2, None, np.linalg.LinAlgError),
])
def test_generate_multivariate_normal_samples(mean, cov, n_samples, n_dims, expected_shape, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            generate_multivariate_normal_samples(mean, cov, n_samples, n_dims)
    else:
        samples = generate_multivariate_normal_samples(mean, cov, n_samples, n_dims)
        assert isinstance(samples, np.ndarray)
        assert samples.shape == expected_shape

        if n_samples > 0:
            # Check data type (should be float)
            assert samples.dtype in [np.float32, np.float64, np.float16], \
                f"Expected float dtype for samples, but got {samples.dtype}"

            # For a sufficient number of samples, the sample mean and covariance
            # should be statistically close to the true values.
            # These are statistical checks and might have slight variations,
            # so tolerances are set loosely.
            if n_samples >= max(10, n_dims + 1): # Need enough samples for meaningful statistics
                # Check sample mean
                actual_mean = np.mean(samples, axis=0)
                np.testing.assert_allclose(actual_mean, mean, atol=0.5, rtol=0.1,
                                           err_msg=f"Sample mean {actual_mean} not close to expected mean {mean}")

                # Check sample covariance (np.cov requires n_samples > n_dims for full covariance)
                if n_samples > n_dims:
                    actual_cov = np.cov(samples, rowvar=False)
                    np.testing.assert_allclose(actual_cov, cov, atol=0.5, rtol=0.1,
                                               err_msg=f"Sample cov:\n{actual_cov}\nnot close to expected cov:\n{cov}")