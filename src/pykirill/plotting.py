import logging

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
        logger.warning(
            "IPython is not installed, IPython-specific configurations are skipped."
        )
        return

    ipython = IPython.get_ipython()
    if not ipython:
        logger.info(
            "Not running in an IPython environment. IPython-specific configurations are skipped."
        )
        return

    ipython.run_line_magic("matplotlib", "inline")
    ipython.run_line_magic("config", "InlineBackend.figure_format = 'retina'")
