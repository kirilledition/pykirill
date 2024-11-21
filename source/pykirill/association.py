"""
This module contains functions for multiple association analysis like EWAS, GWAS and similar
This module eventually will become Glaphyra association package
"""

import string
import typing

import numpy as np
import pandas as pd
import scipy.stats
from tqdm import tqdm


class StatisticalResult(typing.NamedTuple):
    """
    A named tuple to store the results of an association study.

    Attributes:
        target: The target variable.
        feature: The feature variable.
        statistic: The statistical test statistic.
        pvalue: The p-value of the test.

    Usage:
        ```python
        result = StatisticalResult(target="target", feature="feature", statistic=0.5, pvalue=0.01)
        print(f"Statistic: {result.statistic:.2f}, P-value: {result.pvalue:.2e}")
        ```
    """

    target: str
    feature: str
    statistic: typing.Type[np.floating]
    pvalue: typing.Type[np.floating]


def statistical_result_to_string(result: StatisticalResult) -> str:
    """
    Converts a StatisticalResult to a string

    Args:
        result: The StatisticalResult to convert

    Returns:
        A string representation of the StatisticalResult

    Usage:
        ```python
        result = StatisticalResult(target="target", feature="feature", statistic=0.5, pvalue=0.01)
        print(statistical_result_to_string(result))
        ```
    """
    return f"statistic={result.statistic:.2f}, pvalue={result.pvalue:.2e}"


def pearson(target: pd.Series, feature: pd.Series) -> StatisticalResult:
    """
    This function performs an association study using Pearson correlation

    Args:
        target: The target variable
        feature: The feature variable

    Returns:
        A named tuple containing the target and feature names, the Pearson correlation statistic, and the pvalue

    Usage:
        ```python
        result = association.pearson(target, feature)
        print(f"Statistic: {result.statistic:.2f}, P-value: {result.pvalue:.2e}")
        ```
    """
    model = scipy.stats.pearsonr(x=feature, y=target)
    return StatisticalResult(target=target.name, feature=feature.name, statistic=model.statistic, pvalue=model.pvalue)


def pearson_association_study(
    targets: pd.DataFrame, features: pd.DataFrame, dtype: typing.Type[np.floating] = np.float32
) -> pd.DataFrame:
    """
    This function performs a multiple association study using Pearson correlation

    Args:
        targets: A DataFrame containing the target variables
        features: A DataFrame containing the feature variables
        dtype: The data type to use for the results

    Returns:
        A DataFrame containing the results of the association study

    Usage:
        ```python
        results = association.pearson_association_study(targets, features)
        print(results.head())
        ```
    """

    if isinstance(targets, pd.Series):
        if targets.name is None:
            targets.name = "target"
        targets = targets.to_frame()

    if isinstance(features, pd.Series):
        if features.name is None:
            features.name = "feature"
        features = features.to_frame()

    targets = targets.astype(dtype)
    features = features.astype(dtype)
    n_associations = targets.shape[1] * features.shape[1]

    feature_name_length = features.columns.astype(str).str.len().max()
    target_name_length = targets.columns.astype(str).str.len().max()

    StatisticalResultDtype = np.dtype(
        [
            ("target", f"U{target_name_length}"),
            ("feature", f"U{feature_name_length}"),
            ("statistic", dtype),
            ("pvalue", dtype),
        ]
    )

    results = np.empty(n_associations, dtype=StatisticalResultDtype)

    progress_bar = tqdm(total=n_associations)
    description_template = string.Template("Processing (${target_name}, ${feature_name})")

    i = 0
    for target_name, target in targets.items():
        for feature_name, feature in features.items():
            progress_bar.set_description(
                description_template.substitute(target_name=target_name, feature_name=feature_name)
            )
            progress_bar.update()

            statistical_result = pearson(target=target, feature=feature)
            results[i] = statistical_result
            i += 1

    progress_bar.close()

    results_df = (
        pd.DataFrame(results, columns=StatisticalResult._fields)
        .assign(corrected_pvalue=lambda df: df["pvalue"] * n_associations)
        .assign(significant=lambda df: df["corrected_pvalue"] < 0.05)
    ).sort_values(by=["significant", "statistic"], ascending=[False, False])

    return results_df
