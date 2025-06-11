from __future__ import annotations

import typing

import jax
import jax.numpy as jnp
import numpy as np
import pandas as pd

if typing.TYPE_CHECKING:
    from .results import OLSResults


class OLS:
    """Ordinary Least Squares Regression."""

    def __init__(
        self,
        endog: typing.Union[pd.Series, np.ndarray, jax.Array],
        exog: typing.Union[pd.DataFrame, np.ndarray, jax.Array],
        hasconst: typing.Optional[bool] = None,
    ):
        """Initializes the OLS model.

        Args:
            endog: The dependent variable.
            exog: The independent variables.
            hasconst: Indicates whether the independent variables include a constant.
        """
        self.endog_name: str = endog.name if hasattr(endog, "name") else "y"
        self.exog_names: typing.List[str]
        if hasattr(exog, "columns"):
            self.exog_names = list(exog.columns)
        else:
            self.exog_names = [f"x{i+1}" for i in range(exog.shape[1])]

        self.endog: jax.Array = jnp.asarray(endog)
        exog_np: np.ndarray = np.asarray(exog)

        if hasconst is None:
            if not np.any(exog_np.std(axis=0) == 0):
                exog_np = np.c_[np.ones(exog_np.shape[0]), exog_np]
                self.exog_names.insert(0, "const")

        self.exog: jax.Array = jnp.asarray(exog_np)

    def fit(self) -> OLSResults:
        """Fits the OLS model.

        Returns:
            The results of the OLS regression.
        """
        from .results import OLSResults

        params = self._calculate_params(self.exog, self.endog)
        return OLSResults(self, params)

    @staticmethod
    @jax.jit
    def _calculate_params(exog: jax.Array, endog: jax.Array) -> jax.Array:
        """Calculates the OLS parameters using JAX.

        Args:
            exog: The independent variables.
            endog: The dependent variable.

        Returns:
            The OLS parameters.
        """
        xtx = exog.T @ exog
        xty = exog.T @ endog
        params = jnp.linalg.inv(xtx) @ xty
        return params 