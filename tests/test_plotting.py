import sys

from unittest import mock
import seaborn as sns
from matplotlib import pyplot as plt
from pykirill.plotting import (
    setup,
)


class TestSetup:
    def test_setup_seaborn_context(self):
        setup()
        # Retrieve the current context to check its properties
        current_context = sns.plotting_context()

        # Check specific properties to ensure the context is set to "notebook"
        assert (
            current_context["font.size"] == 12
        ), "Font size should be 12 for 'notebook' context"
        assert (
            current_context["axes.titlesize"] == 12
        ), "Axes title size should be 12 for 'notebook' context"

    def test_setup_seaborn_palette(self):
        setup()
        # Retrieve the current palette to check its colors
        current_palette = sns.color_palette()
        expected_colorblind = sns.color_palette("colorblind")

        # Compare the current palette with the expected "colorblind" palette
        assert all(
            [a == b for a, b in zip(current_palette, expected_colorblind)]
        ), "Palette should be 'colorblind', but it's not set correctly"

    @mock.patch.dict(sys.modules, {"IPython": None})
    def test_setup_without_ipython(self):
        # Simulate IPython not being present by returning None
        with mock.patch("logging.Logger.warning") as mock_warning:
            setup()
            mock_warning.assert_called_once_with(
                "IPython is not installed, IPython-specific configurations are skipped."
            )

    @mock.patch("IPython.get_ipython")
    def test_setup_with_ipython_not_running(self, mock_get_ipython):
        # Simulate running in a non-IPython environment
        mock_get_ipython.return_value = None
        with mock.patch("logging.Logger.info") as mock_info:
            setup()
            mock_info.assert_called_once_with(
                "Not running in an IPython environment. IPython-specific configurations are skipped."
            )

    @mock.patch("IPython.get_ipython")
    def test_setup_with_ipython_running(self, mock_get_ipython):
        # Simulate running in an IPython environment
        mock_ipy_instance = mock.Mock()
        mock_get_ipython.return_value = mock_ipy_instance
        setup()
        mock_ipy_instance.run_line_magic.assert_any_call("matplotlib", "inline")
        mock_ipy_instance.run_line_magic.assert_any_call(
            "config", "InlineBackend.figure_format = 'retina'"
        )

    def test_matplotlib_and_seaborn_configurations(self):
        setup()
        assert (
            plt.rcParams["image.cmap"] == "viridis"
        ), "Matplotlib colormap should be 'viridis'"
        current_style = sns.axes_style()
        assert current_style["axes.grid"], "Seaborn grid should be on"
