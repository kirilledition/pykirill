import numpy as np
import pytest
import scipy
import statsmodels.api as sm
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression

from pykirill.regression import OLS


class TestOLS:
    """
    Tests for the OLS regression model.
    """

    @staticmethod
    @pytest.fixture(scope="class")
    def regression_data():
        """
        Generates a regression dataset for benchmarking.
        """
        X, y, _ = make_regression(
            n_samples=10_000,
            n_features=20,
            n_informative=15,
            n_targets=1,
            noise=50,
            coef=True,
            random_state=42,
        )
        return X, y

    @staticmethod
    def fit_pykirill_ols(X, y):
        """
        Fits the OLS model from pykirill.
        """
        model = OLS(endog=y, exog=X)
        model.fit()

    @staticmethod
    def fit_statsmodels_ols_full(X, y):
        """
        Fits the OLS model from statsmodels, including full results object creation.
        """
        X_sm = sm.add_constant(X)
        model = sm.OLS(y, X_sm)
        model.fit()

    @staticmethod
    def fit_statsmodels_ols_params_only(X, y):
        """
        Calculates only the coefficients for the statsmodels OLS model.
        """
        X_sm = sm.add_constant(X)
        model = sm.OLS(y, X_sm)
        model.initialize()
        pinv_wexog = scipy.linalg.pinv(model.wexog)
        pinv_wexog @ model.wendog

    @staticmethod
    def fit_sklearn_ols(X, y):
        """
        Fits the OLS model from scikit-learn.
        """
        model = LinearRegression()
        model.fit(X, y)

    def test_ols_vs_statsmodels(self):
        """
        Tests if the OLS implementation returns the same coefficients as statsmodels.
        """
        X, y, _ = make_regression(
            n_samples=100, n_features=5, n_informative=5, n_targets=1, noise=100, coef=True
        )
        X_sm = sm.add_constant(X)
        sm_model = sm.OLS(y, X_sm)
        sm_results = sm_model.fit()
        pk_model = OLS(y, X)
        pk_results = pk_model.fit()

        np.testing.assert_allclose(pk_results.params, sm_results.params, rtol=1e-5)

    def test_pykirill_ols_benchmark(self, benchmark, regression_data):
        """
        Benchmarks the pykirill OLS implementation.
        """
        X, y = regression_data
        benchmark(self.fit_pykirill_ols, X, y)

    def test_statsmodels_ols_full_benchmark(self, benchmark, regression_data):
        """
        Benchmarks the full statsmodels OLS implementation.
        """
        X, y = regression_data
        benchmark(self.fit_statsmodels_ols_full, X, y)

    def test_statsmodels_ols_params_only_benchmark(self, benchmark, regression_data):
        """
        Benchmarks only the coefficient calculation of statsmodels OLS.
        """
        X, y = regression_data
        benchmark(self.fit_statsmodels_ols_params_only, X, y)

    def test_sklearn_ols_benchmark(self, benchmark, regression_data):
        """
        Benchmarks the scikit-learn OLS implementation.
        """
        X, y = regression_data
        benchmark(self.fit_sklearn_ols, X, y) 