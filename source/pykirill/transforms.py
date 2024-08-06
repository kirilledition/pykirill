"""
Data transformation functions
"""

import numpy as np
import scipy.stats
from numpy import typing as npt


def log_scale(x: npt.NDArray) -> npt.NDArray:
    """
    Applies a logarithmic transformation to the input array and then scales it.

    Args:
        x: Input array to be log-transformed and scaled.

    Returns:
        Log-transformed and scaled array.

    Usage:
        ```python
        # For NumPy arrays
        x = np.array([1, 2, 3, 4], dtype=np.float32)
        log_scaled_x = transforms.log_scale(x)

        # For Pandas DataFrames
        log_scaled_df = df.apply(transforms.log_scale)
        ```
    """

    epsilon = np.finfo(x.dtype).eps
    log_x = np.log(x + epsilon, dtype=x.dtype)
    return scipy.stats.zscore(log_x, nan_policy="omit")
