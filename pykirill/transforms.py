import numpy as np
import scipy.stats
from numpy import typing as npt


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
    return scipy.stats.zscore(log_x, nan_policy="omit")
