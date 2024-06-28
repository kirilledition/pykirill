import logging
import math

from matplotlib import pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup() -> None:
    sns.set_theme(context="notebook", style="whitegrid", palette="colorblind")
    plt.rcParams["image.cmap"] = "viridis"

    # add check for font availability
    # plt.rcParams["font.family"] = ["Arial", "sans-serif"]

    try:
        import IPython
    except ImportError:
        logger.warning("IPython is not installed, IPython-specific configurations are skipped.")
        return

    ipython = IPython.get_ipython()
    if not ipython:
        logger.info("Not running in an IPython environment. IPython-specific configurations are skipped.")
        return

    ipython.run_line_magic("matplotlib", "inline")
    ipython.run_line_magic("config", "InlineBackend.figure_format = 'retina'")


class SubplotsManager:
    ROWS_SCALING_FACTOR = 4
    COLUMNS_SCALING_FACTOR = 5

    def __init__(self, dimensions):
        self.figure, self.axes, self.n_plots = self.create_subplots(dimensions)
        self.current_iteration_index = 0

    def create_subplots(self, dimensions):
        if isinstance(dimensions, int):
            n_rows, n_columns = self.calculate_dimensions(dimensions)
            n_plots = dimensions
        elif isinstance(dimensions, tuple):
            n_rows, n_columns = dimensions
            n_plots = n_rows * n_columns
        else:
            raise ValueError("Dimensions must be int or tuple")

        figure_size = (
            self.COLUMNS_SCALING_FACTOR * n_columns,
            self.ROWS_SCALING_FACTOR * n_rows
        )

        fig, axes = plt.subplots(
            n_rows,
            n_columns,
            figsize=figure_size
        )

        axes = axes.flatten() if n_plots > 1 else np.array([axes])
        return fig, axes, n_plots

    def calculate_dimensions(self, dimensions):
        n_columns = math.ceil(math.sqrt(dimensions))
        n_rows = math.ceil(dimensions / n_columns)
        return n_rows, n_columns

    def next(self):
        if self.current_iteration_index < self.n_plots:
            ax = self.axes[self.current_iteration_index]
            self.current_iteration_index += 1
            return ax
        else:
            raise IndexError("No more subplots available")

    def __getitem__(self, idx):
        if idx < self.n_plots:
            return self.axes[idx]
        else:
            raise IndexError("Index out of range")

    def __iter__(self):
        return iter(self.axes)
