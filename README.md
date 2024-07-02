# 🐗 pyKirill
This is my personal Python package, `pykirill`, which includes a collection of utilities and functions that I frequently use during scientific exploration. This package is especially designed to be portable, making it suitable for environments like Google Colab where setup needs to be minimal.

## Installation

To install `pykirill`, you can use pip directly from GitHub. This method ensures you always get the latest version. Here are the steps to follow:

```bash
pip install git+https://github.com/kirilledition/pykirill.git
```

## Usage

Here are quick examples of how to use `pykirill`:

### Plotting
```python
from pykirill import plotting as kplt

kplt.setup()
```

### Transforms
```python
from pykirill import transforms

x = np.array([1, 2, 3, 4], dtype=np.float32)
log_scaled_x = transforms.log_scale(x)
```

## License

`pykirill` is open-sourced under the MIT license. The details can be found in the [LICENSE](LICENSE) file.

## TODO
[] - Tests for plotting module
[] - Write usage for plotting functions
[] - Update usage for transforms in case of dataframes
[] - New release