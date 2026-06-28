# autooutlier

**Automatic Outlier Detection and Handling for Python**
# autooutlier

**Automatic Outlier Detection and Handling for Python**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/autooutlier.svg)](https://pypi.org/project/autooutlier/)

**Documentation:** https://autooutlier.readthedocs.io/

---

---

## Overview

`autooutlier` is a Python package that **automatically detects, analyzes, and handles outliers** in numerical data. It intelligently selects the best detection and handling methods based on data distribution — requiring **zero configuration** from the user.

Simply pass your DataFrame and column name, and `autooutlier` handles the rest.

---

## Features

- **Automatic Detection** — Selects the optimal outlier detection method (Z-Score, Modified Z-Score, IQR, Percentile) based on data skewness.
- **Automatic Handling** — Chooses the best outlier replacement strategy (winsorization, mean/median/mode replacement, interpolation, etc.) based on data characteristics.
- **Statistical Analysis** — Provides mean, median, mode, standard deviation, variance, skewness, kurtosis, and distribution classification.
- **Pre-Cleaning Summary** — Generates a comprehensive report before cleaning, including detection method, handling strategy, outlier count, and percentage.
- **Post-Cleaning Report** — Returns both the cleaned dataset and an after-cleaning summary report.
- **Flexible Manual Control** — Override automatic selections with manual detection and handling methods when needed.
- **Visualization** — Built-in box plot support via Seaborn.

---

## Installation

```bash
pip install autooutlier
```

Or install from source:

```bash
git clone https://github.com/suruthika-cd/autooutlier.git
cd autooutlier
pip install -e .
```

### Dependencies

- Python >= 3.8
- NumPy >= 1.21.0
- Pandas >= 1.3.0
- SciPy >= 1.7.0
- Seaborn >= 0.11.0
- Matplotlib >= 3.4.0

---

## Quick Start

```python
import pandas as pd
from autooutlier import handle_outliers, before_cleaning_summary, detect_outliers

# Load your data
df = pd.DataFrame({"values": [10, 12, 14, 11, 13, 100, 15, 12, 14, 11]})

# Get a pre-cleaning summary report
summary = before_cleaning_summary(df, "values")
print(summary)

# Automatically detect and handle outliers
cleaned_data, report = handle_outliers(df, "values")
print(report)
print(cleaned_data)
```

---

## Usage Examples

### Automatic Outlier Detection

```python
from autooutlier import detect_outliers

outlier_mask = detect_outliers(df, "column_name")
print(f"Outliers found: {outlier_mask.sum()}")
```

### Automatic Outlier Handling

```python
from autooutlier import handle_outliers

# Fully automatic — detection and handling methods are chosen for you
cleaned_df, report = handle_outliers(df, "column_name")
```

### Manual Detection Method

```python
# Use a specific detection method
cleaned_df, report = handle_outliers(df, "column_name", detection_method="z_score")
```

Available detection methods: `'auto'`, `'Iqr_method'`, `'z_score'`, `'modified_z_score'`, `'percentile'`

### Manual Handling Method

```python
# Use a specific replacement strategy
cleaned_df, report = handle_outliers(df, "column_name", replacement="median")
```

Available replacement methods: `'auto'`, `'interpolate'`, `'winsorization'`, `'median'`, `'mean'`, `'mode'`, `'custom'`, `'remove'`, `'bfill'`, `'ffill'`

### Custom Value Replacement

```python
cleaned_df, report = handle_outliers(df, "column_name", replacement="custom", value=0)
```

### Pre-Cleaning Summary

```python
from autooutlier import before_cleaning_summary

summary = before_cleaning_summary(df, "column_name")
print(summary)
```

Output includes: suggested detection method, handling method, skewness, distribution type, outlier count, and outlier percentage.

---

## API Overview

### Public API

| Function | Description |
|---|---|
| `handle_outliers(data, column, detection_method='auto', replacement='auto', value=None)` | Detect and handle outliers. Returns `(cleaned_data, report)`. |
| `detect_outliers(data, column)` | Detect outliers automatically. Returns a boolean mask. |
| `detect_outlier_method(data, column)` | Returns the suggested detection method name. |
| `before_cleaning_summary(data, column)` | Returns a DataFrame summary report before cleaning. |

### Module Reference

| Module | Contents |
|---|---|
| `autooutlier.statistics` | `mean`, `median`, `mode`, `std`, `var`, `data_range`, `q1`, `q3`, `iqr`, `skew`, `skew_measurment`, `is_normal`, `kurtosis`, `kurtosis_measurement` |
| `autooutlier.detection` | `Iqr_method`, `z_score_method`, `modified_z_score`, `percentile_method`, `detect_outlier_method`, `detect_outliers` |
| `autooutlier.handling` | `winsorization`, `interpolate`, `replace_with_mean`, `replace_with_median`, `replace_with_mode`, `replace_with_custom_value`, `replace_with_forward_fill`, `replace_with_backward_fill`, `remove_outliers`, `detect_handler`, `handle_outliers` |
| `autooutlier.summary` | `before_cleaning_summary` |
| `autooutlier.visualization` | `box_plot` |
| `autooutlier.utils` | `is_numeric`, `is_time_series`, `is_continous`, `outlier_count`, `outlier_percentage` |

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for all notable changes.
