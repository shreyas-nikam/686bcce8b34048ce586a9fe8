
import numpy as np
from typing import Union

def generate_multivariate_normal_samples(mean: np.ndarray, cov: np.ndarray, n_samples: int, n_dims: int) -> np.ndarray:
    """
    Generates samples from a multivariate normal distribution with specified mean and covariance matrix.

    This function performs rigorous validation of input arguments for type, value, and shape.
    It also checks the properties of the covariance matrix (symmetry, positive semi-definiteness,
    and non-singularity) to ensure valid input for NumPy's multivariate normal distribution sampler.

    Args:
        mean: A 1-dimensional NumPy array representing the mean vector of the
              multivariate normal distribution. Its shape must be (n_dims,).
        cov: A 2-dimensional NumPy array representing the covariance matrix of the
             multivariate normal distribution. It must be square and its shape
             must be (n_dims, n_dims). It must also be symmetric and positive definite.
             Singular (rank-deficient) or non-positive semi-definite matrices will
             raise a `numpy.linalg.LinAlgError`.
        n_samples: The number of samples to generate. Must be a non-negative integer.
        n_dims: The dimensionality of the samples. Must be a positive integer (>= 1).

    Returns:
        A NumPy array of shape (n_samples, n_dims) containing the generated samples.
        If `n_samples` is 0, an empty array of shape (0, n_dims) with float64 dtype is returned.

    Raises:
        TypeError: If `mean` or `cov` are not NumPy arrays, or if `n_samples` or `n_dims`
                   are not integers.
        ValueError: If `n_samples` is negative, `n_dims` is less than 1, or if the
                    shapes of `mean` or `cov` are incorrect or inconsistent with `n_dims`.
        numpy.linalg.LinAlgError: If the covariance matrix is not symmetric, not positive
                                  semi-definite (e.g., has negative eigenvalues), or is singular
                                  (e.g., zero matrix or rank-deficient).
        RuntimeError: If an unexpected error occurs during sample generation by NumPy.
    """
    # 1. Type Validation
    if not isinstance(mean, np.ndarray) or not isinstance(cov, np.ndarray):
        raise TypeError("Mean and covariance must be numpy arrays.")
    if not isinstance(n_samples, int) or not isinstance(n_dims, int):
        raise TypeError("n_samples and n_dims must be integers.")

    # 2. Value Validation
    if n_samples < 0:
        raise ValueError("n_samples must be non-negative.")
    if n_dims < 1:
        raise ValueError("n_dims must be at least 1.")

    # 3. Shape Validation
    if mean.ndim != 1 or mean.shape[0] != n_dims:
        raise ValueError(f"Mean vector must be 1-dimensional and have shape ({n_dims},). Got shape {mean.shape}.")
    if cov.ndim != 2 or cov.shape != (n_dims, n_dims):
        raise ValueError(f"Covariance matrix must be 2-dimensional and have shape ({n_dims}, {n_dims}). Got shape {cov.shape}.")

    # 4. Covariance Matrix Properties Validation
    # Check for symmetry with a reasonable tolerance for floating point numbers
    if not np.allclose(cov, cov.T, atol=1e-9):
        raise np.linalg.LinAlgError("Covariance matrix must be symmetric.")
    
    # Check for positive definiteness/semi-definiteness by examining eigenvalues.
    # A symmetric matrix is positive semi-definite if all its eigenvalues are non-negative.
    # It is positive definite if all its eigenvalues are strictly positive.
    # We require it to be positive definite for sampling to avoid issues with singular matrices.
    try:
        # Use eigvalsh for symmetric matrices for numerical stability
        eigenvalues = np.linalg.eigvalsh(cov)

        # Check if any eigenvalue is effectively negative (not positive semi-definite)
        if np.any(eigenvalues < -1e-9): # Allow for very small negative values due to floating point precision
            raise np.linalg.LinAlgError("Covariance matrix is not positive semi-definite (has negative eigenvalues).")

        # Check if the matrix is singular (i.e., not positive definite, smallest eigenvalue is effectively zero).
        # This covers cases like [[0,0],[0,0]] or other rank-deficient matrices.
        # np.random.multivariate_normal requires a non-singular covariance matrix.
        if np.any(eigenvalues < 1e-9): # If any eigenvalue is effectively zero, it's singular
            raise np.linalg.LinAlgError("Covariance matrix is singular (not positive definite).")

    except np.linalg.LinAlgError as e:
        # Catch LinAlgError from eigvalsh itself (e.g., if matrix is ill-conditioned or has NaNs/Infs)
        raise np.linalg.LinAlgError(f"Error during covariance matrix eigenvalue decomposition: {e}")
    except Exception as e:
        # Catch any other unexpected errors during eigenvalue decomposition.
        raise RuntimeError(f"An unexpected error occurred during covariance matrix validation: {e}")

    # 5. Sample Generation
    if n_samples == 0:
        # Return an empty array of the correct shape and a consistent float dtype.
        return np.empty((0, n_dims), dtype=np.float64)

    try:
        # Generate samples using NumPy's multivariate_normal function.
        # The prior validation ensures `cov` is symmetric and positive definite.
        samples = np.random.multivariate_normal(mean, cov, size=n_samples)
        
        # NumPy's multivariate_normal can return a 1D array if n_dims=1 and n_samples > 1.
        # Ensure the output always has shape (n_samples, n_dims) for consistency.
        if n_dims == 1 and samples.ndim == 1:
            samples = samples.reshape(-1, 1)
            
        return samples
    except Exception as e:
        # This catch is a fallback for any unforeseen issues during the actual sampling,
        # though robust pre-validation should prevent most common errors.
        raise RuntimeError(f"An unexpected error occurred during sample generation: {e}")
