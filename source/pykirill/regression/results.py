from __future__ import annotations

import typing

import jax
import jax.numpy as jnp
import pandas as pd
import scipy.stats

if typing.TYPE_CHECKING:
    from .linear_model import OLS


class OLSResults:
    """Results of the OLS regression."""

    def __init__(self, model: OLS, params: jax.Array):
        """Initializes the OLSResults.

        Args:
            model: The OLS model instance.
            params: The fitted parameters.
        """
        self.model: OLS = model
        self._params: jax.Array = params

    @property
    def params(self) -> pd.Series:
        """The fitted parameters."""
        return pd.Series(self._params, index=self.model.exog_names, name="coef")

    @property
    def fittedvalues(self) -> jax.Array:
        """The predicted values from the model."""
        return self.model.exog @ self._params

    @property
    def resid(self) -> jax.Array:
        """The residuals of the model."""
        return self.model.endog - self.fittedvalues

    @property
    def ssr(self) -> jax.Array:
        """The sum of squared residuals."""
        return jnp.sum(self.resid**2)

    @property
    def tss(self) -> jax.Array:
        """The total sum of squares."""
        return jnp.sum((self.model.endog - self.model.endog.mean()) ** 2)

    @property
    def rsquared(self) -> jax.Array:
        """The R-squared of the model."""
        return 1 - self.ssr / self.tss

    @property
    def rsquared_adj(self) -> jax.Array:
        """The adjusted R-squared of the model."""
        return 1 - (1 - self.rsquared) * (self.n_obs - 1) / (self.n_obs - self.n_params)

    @property
    def ess(self) -> jax.Array:
        """The explained sum of squares."""
        return jnp.sum((self.fittedvalues - self.model.endog.mean()) ** 2)

    @property
    def fvalue(self) -> jax.Array:
        """The F-statistic of the model."""
        df_model = self.n_params - 1
        return (self.ess / df_model) / self.mse_resid

    @property
    def f_pvalue(self) -> float:
        """The p-value of the F-statistic."""
        df_model = self.n_params - 1
        df_resid = self.n_obs - self.n_params
        return scipy.stats.f.sf(self.fvalue, df_model, df_resid)

    @property
    def loglike(self) -> jax.Array:
        """The log-likelihood of the model."""
        return -self.n_obs / 2 * (jnp.log(2 * jnp.pi) + jnp.log(self.ssr / self.n_obs) + 1)

    @property
    def aic(self) -> jax.Array:
        """The Akaike Information Criterion."""
        return -2 * self.loglike + 2 * self.n_params

    @property
    def bic(self) -> jax.Array:
        """The Bayesian Information Criterion."""
        return -2 * self.loglike + self.n_params * jnp.log(self.n_obs)

    @property
    def n_obs(self) -> int:
        """The number of observations."""
        return self.model.exog.shape[0]

    @property
    def n_params(self) -> int:
        """The number of parameters."""
        return self.model.exog.shape[1]

    @property
    def mse_resid(self) -> jax.Array:
        """The mean squared error of the residuals."""
        return self.ssr / (self.n_obs - self.n_params)

    @property
    def cov_params(self) -> jax.Array:
        """The covariance matrix of the parameters."""
        return self.mse_resid * jnp.linalg.inv(self.model.exog.T @ self.model.exog)

    @property
    def bse(self) -> pd.Series:
        """The standard errors of the parameters."""
        _bse = jnp.sqrt(jnp.diag(self.cov_params))
        return pd.Series(_bse, index=self.model.exog_names, name="std err")

    @property
    def tvalues(self) -> pd.Series:
        """The t-statistics of the parameters."""
        return self.params / self.bse

    @property
    def pvalues(self) -> pd.Series:
        """The p-values of the parameters."""
        df_resid = self.n_obs - self.n_params
        p = 2 * scipy.stats.t.sf(jnp.abs(self.tvalues), df=df_resid)
        return pd.Series(p, index=self.model.exog_names, name="P>|t|")

    def conf_int(self, alpha: float = 0.05) -> pd.DataFrame:
        """The confidence intervals of the parameters.

        Args:
            alpha: The significance level.

        Returns:
            The confidence intervals.
        """
        df_resid = self.n_obs - self.n_params
        q = scipy.stats.t.ppf(1 - alpha / 2, df=df_resid)
        lower = self.params - q * self.bse
        upper = self.params + q * self.bse
        return pd.concat([lower, upper], axis=1, keys=["[0.025", "0.975]"])

    def summary(self) -> str:
        """Returns a summary of the regression results.

        Returns:
            A summary of the regression results.
        """
        summary_df = pd.DataFrame(
            {
                "coef": self.params,
                "std err": self.bse,
                "t": self.tvalues,
                "P>|t|": self.pvalues,
            }
        )
        conf_int_df = self.conf_int()
        summary_df = pd.concat([summary_df, conf_int_df], axis=1)

        header = f"""
OLS Regression Results
==============================================================================
Dep. Variable:                      {self.model.endog_name}   R-squared:                       {self.rsquared:.3f}
Model:                                  OLS   Adj. R-squared:                  {self.rsquared_adj:.3f}
Method:                       Least Squares   F-statistic:                     {self.fvalue:.2f}
Date:                          {pd.Timestamp.now().strftime('%a, %d %b %Y')}   Prob (F-statistic):              {self.f_pvalue:.3f}
Time:                          {pd.Timestamp.now().strftime('%H:%M:%S')}   Log-Likelihood:                  {self.loglike:.3f}
AIC:                                  {self.aic:.3f}   BIC:                             {self.bic:.3f}
No. Observations:                   {self.n_obs}
Df Residuals:                       {self.n_obs - self.n_params}
Df Model:                           {self.n_params - 1}
==============================================================================
"""
        return header + summary_df.to_string() 