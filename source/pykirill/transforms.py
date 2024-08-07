"""
Data transformation functions
"""

import typing

import numpy as np
import pandas as pd
import scipy.stats
import sklearn.decomposition
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


class PrincipalComponentAnalysisResult(typing.NamedTuple):
    pca: sklearn.decomposition.PCA  # pca_object
    scores: pd.DataFrame  # scores
    loadings: pd.DataFrame
    cumulative_explained_variance: pd.Series
    n_components: int

    def __repr__(self):
        explained_variance = self.cumulative_explained_variance[-1]
        scores_shape = self.scores.shape
        loadings_shape = self.loadings.shape

        return f"""{self.__class__.__name__}
        N components: {self.n_components}
        Explained variance: {explained_variance:.2f}
        Scores shape: {scores_shape}
        Loadings shape: {loadings_shape}
        """


def principal_component_analysis(
    data: pd.DataFrame,
    n_components: typing.Optional[int] = None,
    pca_object: typing.Optional[sklearn.decomposition.PCA] = None,
) -> PrincipalComponentAnalysisResult:
    """
    Performs PCA on the given data and returns the results in form of typed named tuple object dataframes
    """
    if pca_object is None:
        pca_object = sklearn.decomposition.PCA(n_components=n_components).fit(data)

    scores_array = pca_object.transform(data)

    components_names = [f"PC{i}" for i in range(1, n_components + 1)]
    scores = pd.DataFrame(scores_array, columns=components_names, index=data.index)
    loadings = pd.DataFrame(pca_object.components_.T, index=data.columns, columns=components_names)
    cumulative_explained_variance = pd.Series(
        pca_object.explained_variance_ratio_, index=components_names, name="Cumulative explained variance"
    ).cumsum()

    return PrincipalComponentAnalysisResult(
        pca=pca_object,
        scores=scores,
        loadings=loadings,
        cumulative_explained_variance=cumulative_explained_variance,
        n_components=pca_object.n_components_,
    )
