# Installation

This guide covers how to install `autooutlier` and verify your setup.

---

## Requirements

Before installing, make sure you have:

- **Python 3.8** or later
- **pip** (Python package manager)

---

## Install from PyPI

The recommended way to install `autooutlier` is from [PyPI](https://pypi.org/project/autooutlier/):

```bash
pip install autooutlier
```

This will automatically install all required dependencies.

---

## Install from Source

To install the latest development version directly from the GitHub repository:

```bash
git clone https://github.com/suruthika-cd/autooutlier.git
cd autooutlier
pip install -e .
```

> [!TIP]
> Using `pip install -e .` (editable mode) is recommended for development. Changes you make to the source code will be immediately available without reinstalling.

---

## Dependencies

`autooutlier` depends on the following packages, which are automatically installed:

| Package | Minimum Version | Purpose |
|---|---|---|
| [NumPy](https://numpy.org/) | `>= 1.21.0` | Numerical computations and percentile calculations |
| [Pandas](https://pandas.pydata.org/) | `>= 1.3.0` | DataFrame operations and data manipulation |
| [SciPy](https://scipy.org/) | `>= 1.7.0` | Statistical functions (skewness calculation) |
| [Matplotlib](https://matplotlib.org/) | `>= 3.4.0` | Base plotting library |
| [Seaborn](https://seaborn.pydata.org/) | `>= 0.11.0` | Box plot visualization |

---

## Verify Installation

After installing, verify that `autooutlier` is correctly set up:

```python
import autooutlier
print(autooutlier.__version__)
```

Expected output:

```
0.1.0
```

You can also run a quick smoke test to confirm everything works:

```python
import pandas as pd
from autooutlier import detect_outliers

df = pd.DataFrame({"values": [10, 12, 14, 11, 13, 100, 15, 12, 14, 11]})
outliers = detect_outliers(df, "values")
print(f"Outliers found: {outliers.sum()}")
```

If this runs without errors, you're ready to go!

---

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade autooutlier
```

---

## Uninstalling

To remove the package:

```bash
pip uninstall autooutlier
```

---

## Virtual Environments

> [!IMPORTANT]
> It is strongly recommended to install `autooutlier` inside a virtual environment to avoid dependency conflicts with other projects.

### Using `venv`

```bash
# Create a virtual environment
python -m venv myenv

# Activate it
# Windows:
myenv\Scripts\activate
# macOS/Linux:
source myenv/bin/activate

# Install autooutlier
pip install autooutlier
```

### Using `conda`

```bash
conda create -n outlier-env python=3.10
conda activate outlier-env
pip install autooutlier
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'autooutlier'`

- Make sure the package is installed in the correct Python environment.
- Check your active environment: `python -c "import sys; print(sys.executable)"`

### Dependency conflicts

- Try installing in a clean virtual environment.
- Check for version conflicts: `pip check`

### Permission errors

- On Linux/macOS, try: `pip install --user autooutlier`
- Alternatively, use a virtual environment (recommended).

---

**Next:** [Quick Start →](quickstart.md)
