import numpy as np
import pytest

from pykirill.transforms import log_scale


class TestLogScale:
    def test_positive_values(self):
        # Only positive values for log_scale
        x = np.array([1, 2, 3, 4], dtype=np.float32)
        log_scaled_x = log_scale(x)

        expected = np.array([-1.526072, -0.19470063, 0.5841019, 1.1366711], dtype=np.float32)

        assert np.all(np.isfinite(log_scaled_x)), "Result contains NaN or inf"

        np.testing.assert_array_almost_equal(log_scaled_x, expected, err_msg="Incorrect result")

        np.testing.assert_array_almost_equal(log_scaled_x.mean(), 0.0, err_msg="Mean is not zero")
        np.testing.assert_array_almost_equal(log_scaled_x.std(), 1.0, err_msg="Standard deviation is not one")

    def test_with_nan(self):
        # Only positive values for log_scale
        x = np.array([np.nan, 2, 3, 4, 5, 6], dtype=np.float32)
        log_scaled_x = log_scale(x)
        # Since exact values are hard to predict due to log, we check if result is finite
        expected = np.array(
            [np.nan, -1.6050358, -0.5599373, 0.1815718, 0.75673103, 1.2266703],
            dtype=np.float32,
        )

        assert np.sum(np.isfinite(log_scaled_x)) > 1, "Result contains more then one NaN or inf"

        np.testing.assert_array_almost_equal(log_scaled_x, expected, err_msg="Incorrect result")

        np.testing.assert_array_almost_equal(np.nanmean(log_scaled_x), 0.0, err_msg="Mean is not zero")
        np.testing.assert_array_almost_equal(np.nanstd(log_scaled_x), 1.0, err_msg="Standard deviation is not one")

    def test_with_zero_elements(self):
        # Input contains zero, should handle gracefully without errors
        x = np.array([0, 0, 1, 2, 3], dtype=np.float32)
        log_scaled_x = log_scale(x)

        assert np.all(np.isfinite(log_scaled_x))

    @pytest.mark.filterwarnings("ignore:Degrees of freedom <= 0 for slice")
    @pytest.mark.filterwarnings("ignore:Mean of empty slice")
    @pytest.mark.filterwarnings("ignore:invalid value encountered in log")
    def test_with_negative(self):
        # Input contains negative values, should result in NaNs or infs
        x = np.array([-1, -2, -3, -4], dtype=np.float32)
        result = log_scale(x)
        assert np.all(np.isnan(result) | np.isinf(result))
