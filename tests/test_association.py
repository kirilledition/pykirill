import numpy as np
import scipy.stats
import pandas as pd
from pykirill.association import StatisticalResult, statistical_result_to_string, pearson, pearson_association_study


class TestStatisticalResult:
    def test_creation(self):
        # Create a StatisticalResult
        result = StatisticalResult(target="target1", feature="feature1", statistic=0.5, pvalue=0.01)
        # Check that the attributes are correct
        assert result.target == "target1"
        assert result.feature == "feature1"
        assert result.statistic == 0.5
        assert result.pvalue == 0.01

    def test_conversion(self):
        result = StatisticalResult(target="target1", feature="feature1", statistic=0.5, pvalue=0.01)
        result_str = statistical_result_to_string(result)
        expected_str = "statistic=0.50, pvalue=1.00e-02"
        assert result_str == expected_str


class TestPearson:
    def test_basic(self):
        # Create sample data
        np.random.seed(0)
        x = pd.Series(np.random.rand(100), name="feature1")
        y = pd.Series(np.random.rand(100), name="target1")
        # Compute Pearson correlation using our function
        result = pearson(target=y, feature=x)
        # Compute Pearson correlation using scipy directly
        expected_statistic, expected_pvalue = scipy.stats.pearsonr(x, y)
        # Check that the results match
        assert result.statistic == expected_statistic
        assert result.pvalue == expected_pvalue
        assert result.target == "target1"
        assert result.feature == "feature1"

    def test_with_mismatched_indices(self):
        # Create sample data with mismatched indices
        x = pd.Series(np.arange(100), index=np.arange(100), name="feature1")
        y = pd.Series(np.arange(100, 200), index=np.arange(100, 200), name="target1")
        # Compute Pearson correlation
        result = pearson(target=y, feature=x)
        # Since the data indices are mismatched but the values are sequential, correlation should be 1.0
        np.testing.assert_array_almost_equal(result.statistic, 1.0)


class TestPearsonAssociationStudy:
    def test_basic(self):
        # Create sample data
        np.random.seed(0)
        features = pd.DataFrame({"feature1": np.random.rand(100), "feature2": np.random.rand(100)})
        targets = pd.DataFrame({"target1": np.random.rand(100), "target2": np.random.rand(100)})
        # Run the association study
        results_df = pearson_association_study(targets=targets, features=features, dtype=np.float64)
        # The number of associations should be 4 (2 targets * 2 features)
        assert len(results_df) == 4
        # Check that the columns are correct
        expected_columns = ["target", "feature", "statistic", "pvalue", "corrected_pvalue", "significant"]
        assert list(results_df.columns) == expected_columns
        # Compute expected results
        expected_results = []
        n_associations = 4
        for target_name, target in targets.items():
            for feature_name, feature in features.items():
                statistic, pvalue = scipy.stats.pearsonr(target, feature)
                corrected_pvalue = pvalue * n_associations
                significant = corrected_pvalue < 0.05
                expected_results.append(
                    {
                        "target": target_name,
                        "feature": feature_name,
                        "statistic": statistic,
                        "pvalue": pvalue,
                        "corrected_pvalue": corrected_pvalue,
                        "significant": significant,
                    }
                )
        expected_df = pd.DataFrame(expected_results)
        # Sort the expected_df as in the function
        expected_df = expected_df.sort_values(by=["significant", "statistic"], ascending=[False, False])
        # Reset index
        expected_df = expected_df.reset_index(drop=True)
        # Reset index in results_df
        results_df = results_df.reset_index(drop=True)

        print(results_df)
        print("XOXOXO")
        print(expected_df)
        print("XOXOXO")
        # Now check that results_df matches expected_df
        pd.testing.assert_frame_equal(results_df, expected_df)

    def test_with_series(self):
        # Create sample data
        np.random.seed(0)
        features = pd.Series(np.random.rand(100), name="feature1")
        targets = pd.Series(np.random.rand(100), name="target1")
        # Run the association study
        results_df = pearson_association_study(targets=targets, features=features, dtype=np.float64)
        # The number of associations should be 1
        assert len(results_df) == 1
        # Check that the columns are correct
        expected_columns = ["target", "feature", "statistic", "pvalue", "corrected_pvalue", "significant"]
        assert list(results_df.columns) == expected_columns
        # Check that the results are correct
        statistic, pvalue = scipy.stats.pearsonr(targets, features)
        expected_df = pd.DataFrame(
            [
                {
                    "target": "target1",
                    "feature": "feature1",
                    "statistic": statistic,
                    "pvalue": pvalue,
                    "corrected_pvalue": pvalue,
                    "significant": pvalue < 0.05,
                }
            ]
        )
        # Now check that results_df matches expected_df
        print(results_df.reset_index(drop=True))
        print("XOXOXO")
        print(expected_df)
        pd.testing.assert_frame_equal(results_df.reset_index(drop=True), expected_df)

    def test_with_unnamed_series(self):
        # Create sample data
        np.random.seed(0)
        features = pd.Series(np.random.rand(100))
        targets = pd.Series(np.random.rand(100))
        # Run the association study
        results_df = pearson_association_study(targets=targets, features=features)
        # The names should have been set to 'target' and 'feature'
        assert results_df["target"].iloc[0] == "target"
        assert results_df["feature"].iloc[0] == "feature"

    def test_dtype(self):
        # Create sample data
        np.random.seed(0)
        features = pd.DataFrame({"feature1": np.random.rand(100), "feature2": np.random.rand(100)})
        targets = pd.DataFrame({"target1": np.random.rand(100), "target2": np.random.rand(100)})
        # Run the association study with dtype=np.float64
        results_df = pearson_association_study(targets=targets, features=features, dtype=np.float64)
        # Check that the 'statistic' and 'pvalue' columns are of dtype float64
        assert results_df["statistic"].dtype == np.float64
        assert results_df["pvalue"].dtype == np.float64

    def test_progress_bar_suppressed(self, capsys):
        # Create sample data
        np.random.seed(0)
        features = pd.DataFrame({"feature1": np.random.rand(10)})
        targets = pd.DataFrame({"target1": np.random.rand(10)})
        # Run the association study
        pearson_association_study(targets=targets, features=features)
        # Capture the output
        captured = capsys.readouterr()
        # Check that the progress bar output is present
        assert "Processing (" in captured.err  # tqdm writes to stderr
