"""
This module contains functions for multiple association analysis like EWAS, GWAS and similar
This module eventually will become Glaphyra association package
"""

import collections
import string

import numpy as np
import pandas as pd
import scipy.stats
from tqdm import tqdm

StatisticalResult = collections.namedtuple("StatisticalResult", ["target", "feature", "statistic", "pvalue"])


def pearson_association(target: pd.Series, feature: pd.Series):
    """This function performs an association study using Pearson correlation"""
    model = scipy.stats.pearsonr(x=feature, y=target)
    return StatisticalResult(target=target.name, feature=feature.name, statistic=model.statistic, pvalue=model.pvalue)


def pearson_association_study(targets: pd.DataFrame, features: pd.DataFrame, dtype: np.dtype = np.float32):
    """This function performs an association study using Pearson correlation"""

    if isinstance(targets, pd.Series):
        targets = targets.to_frame()

    if isinstance(features, pd.Series):
        features = features.to_frame()

    targets = targets.astype(dtype)
    features = features.astype(dtype)
    n_associations = targets.shape[1] * features.shape[1]

    feature_name_length = features.columns.str.len().max()
    target_name_length = targets.columns.str.len().max()

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

            statistical_result = pearson_association(target=target, feature=feature)
            results[i] = statistical_result
            i += 1

    progress_bar.close()
    return pd.DataFrame(results, columns=StatisticalResult._fields)
