#  📖 Overview

This is my personal Python package, `pykirill`, which includes a collection of utilities and functions that I frequently use during scientific exploration. This package is especially designed to be portable, making it suitable for environments like Google Colab where setup needs to be minimal.

## Installation

There are several ways to install `pykirill`

### PyPI

You can use regualar `pip install` from PyPI

```bash
pip install pykirill
```

### GitHub source

You can use pip to install directly from GitHub. This method ensures you always get the latest version. Also gives access to experimental features in development

```bash
pip install git+https://github.com/kirilledition/pykirill.git@main
```

### GitHub release

You also can use link to wheel from github releases

```bash
pip install https://github.com/kirilledition/pykirill/releases/download/2024.1.0/pykirill-2024.1.0-py3-none-any.whl
```

### GitHub Container Registry
And finally package is also runnable as docker container from GitHub Container Registry

```bash
docker run --rm -it ghcr.io/kirilledition/pykirill:2024.1.0
```


## Usage

Here are quick examples of how to use `pykirill`:

### Plotting
```python
from pykirill import plotting

plotting.setup()

axm = plotting.SubplotsManager(4)

for trajectory_fragment in range(4):
  frame_values = ...

  ax = axm.nextax()
  ax.hist(frame_values)
  ax.set_title(f"Histogram of intensity values of {trajectory_fragment}")
  ax.set_xlabel("Intensity")
  ax.set_ylabel("Frequency")

axm.show()
```

### Transforms
```python
from pykirill import transforms

# For NumPy arrays
x = np.array([1, 2, 3, 4], dtype=np.float32)
log_scaled_x = transforms.log_scale(x)

# For Pandas DataFrames
log_scaled_df = df.apply(transforms.log_scale)
```