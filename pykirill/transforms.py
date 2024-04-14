import numpy as np
from numpy import typing as npt


def scale(x: npt.NDArray) -> npt.NDArray:
    mean = np.nanmean(x)
    std = np.nanstd(x)
    return (x - mean) / std


def log_scale(x: npt.NDArray) -> npt.NDArray:
    epsilon = np.finfo(x.dtype).eps
    log_x = np.log(x + epsilon)
    return scale(log_x)
