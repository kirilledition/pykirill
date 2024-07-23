import numpy as np
from numpy import typing as npt


def scale(x: npt.NDArray) -> npt.NDArray:
    """
    Scales the input array by subtracting the mean and dividing by the standard deviation.

    Args:
        x (npt.NDArray): Input array to be scaled.

    Returns:
        npt.NDArray: Scaled array with mean 0 and standard deviation 1.

    Usage:
        # For NumPy arrays
        scaled_x = scale(x)

        # For Pandas DataFrames
        scaled_df = df.apply(transforms.scale, engine='numba', raw=True, engine_kwargs={'parallel': True})
    """
    mean = np.nanmean(x, dtype=x.dtype)
    std = np.nanstd(x, dtype=x.dtype)
    return (x - mean) / std


def log_scale(x: npt.NDArray) -> npt.NDArray:
    """
    Applies a logarithmic transformation to the input array and then scales it.

    Args:
        x (npt.NDArray): Input array to be log-transformed and scaled.

    Returns:
        npt.NDArray: Log-transformed and scaled array.
    """
    epsilon = np.finfo(x.dtype).eps
    log_x = np.log(x + epsilon, dtype=x.dtype)
    return scale(log_x)
