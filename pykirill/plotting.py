import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.font_manager
import logging
import math
import typing
import numpy as np


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup() -> None:
    sns.set_theme(context="notebook", style="whitegrid", palette="colorblind")
    plt.rcParams["image.cmap"] = "viridis"
    plt.rcParams['figure.autolayout'] = True

    arial_available = False
    for font in matplotlib.font_manager.fontManager.ttflist:
        if 'Arial' in font.name:
            arial_available = True
            break

    if arial_available:
        plt.rcParams["font.family"] = "Arial"
        logger.info(
            "Arial font is available and has been set as the default font.")
    else:
        plt.rcParams["font.family"] = "sans-serif"
        logger.info(
            "Arial font is not available. Defaulting to sans-serif font.")

    try:
        import IPython
    except ImportError:
        logger.warning(
            "IPython is not installed, IPython-specific configurations are skipped.")
        return

    ipython = IPython.get_ipython()
    if not ipython:
        logger.info(
            "Not running in an IPython environment. IPython-specific configurations are skipped.")
        return

    ipython.run_line_magic("matplotlib", "inline")
    ipython.run_line_magic("config", "InlineBackend.figure_format = 'retina'")


class SubplotsManager:
    """
    Manages the creation and iteration of subplots in a Matplotlib figure.

    Attributes:
        ROWS_SCALING_FACTOR (int): Scaling factor for the height of each row.
        COLUMNS_SCALING_FACTOR (int): Scaling factor for the width of each column.
        figure (plt.Figure): The Matplotlib figure containing the subplots.
        axes (np.ndarray[plt.Axes]): Array of Matplotlib Axes objects representing the subplots.
        n_plots (int): The total number of subplots.
        current_iteration_index (int): The index of the next subplot to be accessed.
    """

    ROWS_SCALING_FACTOR: int = 5
    COLUMNS_SCALING_FACTOR: int = 6

    def __init__(self, dimensions: int | tuple[int, int]) -> None:
        """
        Initializes the SubplotsManager with the given dimensions.

        Args:
            dimensions (int | tuple[int, int]): The number of subplots or a tuple specifying (rows, columns).
        """
        self.figure: plt.Figure
        self.axes: np.ndarray[plt.Axes]
        self.n_plots: int
        self.figure, self.axes, self.n_plots = self.create_subplots(dimensions)
        self.current_iteration_index: int = 0

    def calculate_dimensions(self, dimensions: int | tuple[int, int]) -> tuple[int, int]:
        """
        Calculates the number of rows and columns for the subplots based on the given dimensions.

        Args:
            dimensions (int | tuple[int, int]): The number of subplots or a tuple specifying (rows, columns).

        Returns:
            tuple[int, int]: The number of rows and columns.
        """
        if isinstance(dimensions, tuple):
            n_rows, n_columns = dimensions
            return n_rows, n_columns

        if isinstance(dimensions, int):
            n_columns = math.ceil(math.sqrt(dimensions))
            n_rows = math.ceil(dimensions / n_columns)
            return n_rows, n_columns

        raise ValueError("Dimensions must be int or tuple")

    def create_subplots(self, dimensions: int | tuple[int, int]) -> tuple[plt.Figure, np.ndarray[plt.Axes], int]:
        """
        Creates the subplots and returns the figure, axes array, and the total number of plots.

        Args:
            dimensions (int | tuple[int, int]): The number of subplots or a tuple specifying (rows, columns).

        Returns:
            tuple[plt.Figure, np.ndarray[plt.Axes], int]: The figure, axes array, and the total number of plots.
        """
        n_rows, n_columns = self.calculate_dimensions(dimensions)
        n_plots = n_rows * n_columns

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

    def show(self) -> None:
        """
        Displays the figure with a tight layout.
        """
        self.figure.tight_layout()
        self.figure.show()

    def next(self) -> plt.Axes:
        """
        Returns the next available subplot Axes object.

        Returns:
            plt.Axes: The next available subplot Axes object.

        Raises:
            IndexError: If no more subplots are available.
        """
        if self.current_iteration_index < self.n_plots:
            ax = self.axes[self.current_iteration_index]
            self.current_iteration_index += 1
            return ax
        raise IndexError("No more subplots available")

    def __getitem__(self, idx: int) -> plt.Axes:
        """
        Returns the subplot Axes object at the given index.

        Args:
            idx (int): The index of the subplot Axes object to return.

        Returns:
            plt.Axes: The subplot Axes object at the given index.

        Raises:
            IndexError: If the index is out of range.
        """
        if idx < self.n_plots:
            return self.axes[idx]
        raise IndexError("Index out of range")

    def __iter__(self) -> typing.Iterator[plt.Axes]:
        """
        Returns an iterator over the subplot Axes objects.

        Returns:
            iter[plt.Axes]: An iterator over the subplot Axes objects.
        """
        return iter(self.axes)


def image_show(image, ax=None, cmap='gray', show_grid=False, hide_ticks=True, **kwargs):
    """
    Displays an image on the given Matplotlib Axes.

    Parameters:
        image (ndarray): The image to display.
        ax (matplotlib.axes.Axes, optional): The Axes on which to display the image. If None, uses the current Axes.
        cmap (str, optional): The colormap to use. Default is 'gray'.
        show_grid (bool, optional): Whether to display a grid. Default is False.
        hide_ticks (bool, optional): Whether to hide axis ticks and labels. Default is True.
        **kwargs: Additional keyword arguments to pass to ax.imshow().

    Returns:
        matplotlib.axes.Axes: The Axes with the displayed image.
    """
    if ax is None:
        ax = plt.gca()

    ax.imshow(image, cmap=cmap, **kwargs)

    if not show_grid:
        ax.grid(False)

    if hide_ticks:
        ax.tick_params(axis='both', which='both', bottom=False,
                       left=False, labelbottom=False, labelleft=False)

    return ax
