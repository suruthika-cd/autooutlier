# autooutlier

**Automatic Outlier Detection and Handling for Python**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/autooutlier.svg)](https://pypi.org/project/autooutlier/)

---

## What is autooutlier?

`autooutlier` is a Python package that **automatically detects, analyzes, and handles outliers** in numerical data. It intelligently selects the best detection and handling methods based on data distribution — requiring **zero configuration** from the user.

Simply pass your DataFrame and column name, and `autooutlier` handles the rest.

```python
import pandas as pd
from autooutlier import handle_outliers

df = pd.DataFrame({"salary": [35000, 42000, 38000, 40000, 250000, 37000, 41000]})

cleaned_df, report = handle_outliers(df, "salary")
print(report)
```

---

## Key Features

| Feature | Description |
|---|---|
| **Automatic Detection** | Selects the optimal outlier detection method (Z-Score, Modified Z-Score, IQR, Percentile) based on data skewness. |
| **Automatic Handling** | Chooses the best replacement strategy (winsorization, mean/median/mode, interpolation, etc.) based on data characteristics. |
| **Statistical Analysis** | Provides mean, median, mode, standard deviation, variance, skewness, kurtosis, and distribution classification. |
| **Pre-Cleaning Summary** | Generates a comprehensive report before cleaning, including detection method, handling strategy, outlier count, and percentage. |
| **Post-Cleaning Report** | Returns both the cleaned dataset and an after-cleaning summary report. |
| **Flexible Manual Control** | Override automatic selections with manual detection and handling methods when needed. |
| **Visualization** | Built-in box plot support via Seaborn. |

---

## How It Works

`autooutlier` follows a simple three-step process:

1. **Analyze** — Evaluate the data distribution using skewness and other statistical measures.
2. **Detect** — Apply the most appropriate detection method based on the analysis.
3. **Handle** — Replace or remove outliers using the best-suited handling strategy.

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Your Data  │────▶│  Auto Detection  │────▶│  Auto Handling   │
│ (DataFrame) │     │  (IQR/Z-Score/…) │     │ (Mean/Median/…)  │
└─────────────┘     └──────────────────┘     └──────────────────┘
                                                       │
                                               ┌───────┴───────┐
                                               │ Cleaned Data  │
                                               │  + Report     │
                                               └───────────────┘
```

---

## Documentation

| Page | Description |
|---|---|
| [Installation](installation.md) | How to install the package and its dependencies. |
| [Quick Start](quickstart.md) | Get up and running in under 5 minutes. |
| [User Guide](user_guide.md) | Comprehensive guide to using autooutlier. |
| [Detection Methods](detection_methods.md) | In-depth explanation of all outlier detection algorithms. |
| [Handling Methods](handling_methods.md) | Detailed reference for all outlier replacement strategies. |
| [Visualization](visualization.md) | How to use the built-in visualization tools. |
| [API Reference](api_reference.md) | Complete reference for every public function and parameter. |
| [Examples](examples.md) | Practical, end-to-end usage examples. |
| [FAQ](faq.md) | Frequently asked questions and troubleshooting. |
| [Changelog](changelog.md) | Version history and release notes. |

---

## Quick Links

- **GitHub Repository**: [https://github.com/suruthika-cd/autooutlier](https://github.com/suruthika-cd/autooutlier)
- **PyPI Package**: [https://pypi.org/project/autooutlier/](https://pypi.org/project/autooutlier/)
- **Issue Tracker**: [https://github.com/suruthika-cd/autooutlier/issues](https://github.com/suruthika-cd/autooutlier/issues)
- **License**: [MIT License](https://opensource.org/licenses/MIT)

---

## Author

Created and maintained by **Suruthika C D**.

---

*This documentation is compatible with [MkDocs](https://www.mkdocs.org/) and [Read the Docs](https://readthedocs.org/).*
