# User Guide

This guide provides a comprehensive walkthrough of everything `autooutlier` can do. It covers the core workflow, automatic mode, manual overrides, summary reports, and best practices.

---

## Table of Contents

- [Core Workflow](#core-workflow)
- [Automatic Outlier Detection](#automatic-outlier-detection)
- [Automatic Outlier Handling](#automatic-outlier-handling)
- [The `handle_outliers()` Function](#the-handle_outliers-function)
- [Pre-Cleaning Summary Reports](#pre-cleaning-summary-reports)
- [Post-Cleaning Reports](#post-cleaning-reports)
- [Manual Method Selection](#manual-method-selection)
- [Custom Value Replacement](#custom-value-replacement)
- [Working with Multiple Columns](#working-with-multiple-columns)
- [Statistical Analysis Functions](#statistical-analysis-functions)
- [Data Validation](#data-validation)
- [Best Practices](#best-practices)

---

## Core Workflow

The typical `autooutlier` workflow consists of three steps:

1. **Inspect** — Use `before_cleaning_summary()` to understand your data.
2. **Detect** — Use `detect_outliers()` to identify outlier rows.
3. **Handle** — Use `handle_outliers()` to clean the data.

```python
import pandas as pd
from autooutlier import before_cleaning_summary, detect_outliers, handle_outliers

df = pd.DataFrame({"values": [10, 12, 14, 11, 13, 100, 15, 12, 14, 11]})

# Step 1: Inspect
summary = before_cleaning_summary(df, "values")
print(summary)

# Step 2: Detect
outliers = detect_outliers(df, "values")
print(f"Outlier count: {outliers.sum()}")

# Step 3: Handle
cleaned_df, report = handle_outliers(df.copy(), "values")
print(report)
```

---

## Automatic Outlier Detection

When you call `detect_outliers()` or use `detection_method='auto'` in `handle_outliers()`, the package automatically selects the best detection method based on the **skewness** of your data:

| Data Distribution | Skewness Range | Method Selected |
|---|---|---|
| Perfectly Symmetric | `skew == 0` | Z-Score |
| Approximately Symmetric | `-0.5 ≤ skew ≤ 0.5` | Z-Score |
| Moderately Skewed | `0.5 < |skew| ≤ 1` | Modified Z-Score |
| Highly Skewed | `|skew| > 1` | Modified Z-Score |

You can check which method the package will choose for your data:

```python
from autooutlier import detect_outlier_method

method = detect_outlier_method(df, "column_name")
print(f"Selected method: {method}")
# Output: "z_score", "modified_z_score", or "Iqr_method"
```

> [!NOTE]
> The automatic detection logic uses the `skew_measurment()` function from the statistics module to classify the distribution. See [Detection Methods](detection_methods.md) for detailed explanations of each algorithm.

---

## Automatic Outlier Handling

When you use `replacement='auto'` in `handle_outliers()`, the package selects the best handling strategy based on multiple data characteristics:

| Condition | Priority | Method Selected |
|---|---|---|
| Time series data (`datetime` column) | 1st | Interpolation |
| Continuous/monotonic data | 2nd | Interpolation |
| Outlier percentage ≤ 5% | 3rd | Winsorization |
| Skewed distribution | 4th | Median replacement |
| Symmetric distribution | 5th | Mean replacement |
| Fallback | Last | Median replacement |

The automatic handler evaluates these conditions in order, selecting the first applicable strategy.

```python
from autooutlier.handling import detect_handler

handler = detect_handler(df, "column_name")
print(f"Selected handler: {handler}")
# Output: "interpolate", "winsorization", "median", or "mean"
```

> [!TIP]
> The automatic handler considers whether your data is a time series, continuous, and what percentage of values are outliers — making it a smart default for most use cases.

---

## The `handle_outliers()` Function

This is the primary function of the package. It detects outliers, handles them, and returns both the cleaned data and a summary report.

### Signature

```python
handle_outliers(data, column, detection_method='auto', replacement='auto', value=None)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `pd.DataFrame` | *required* | The input DataFrame. |
| `column` | `str` | *required* | The name of the column to process. |
| `detection_method` | `str` | `'auto'` | The outlier detection method. Options: `'auto'`, `'Iqr_method'`, `'z_score'`, `'modified_z_score'`, `'percentile'`. |
| `replacement` | `str` | `'auto'` | The outlier handling method. Options: `'auto'`, `'interpolate'`, `'winsorization'`, `'median'`, `'mean'`, `'mode'`, `'custom'`, `'remove'`, `'bfill'`, `'ffill'`. |
| `value` | numeric or `None` | `None` | The custom replacement value when `replacement='custom'`. |

### Returns

A **tuple** of `(cleaned_data, after_cleaning_report)`:

- **`cleaned_data`** (`pd.DataFrame`) — The DataFrame with outliers handled.
- **`after_cleaning_report`** (`pd.DataFrame`) — A summary report with columns: `Column`, `Detection Method`, `Handling Method`, `Outlier Count`, `Outlier Percentage`, `Skewness`, `Distribution`.

> [!WARNING]
> `handle_outliers()` may modify the input DataFrame in place for most handling methods. Always pass `df.copy()` if you need to preserve the original data.

### Example

```python
# Fully automatic
cleaned_df, report = handle_outliers(df.copy(), "salary")

# Manual detection, automatic handling
cleaned_df, report = handle_outliers(df.copy(), "salary", detection_method="z_score")

# Automatic detection, manual handling
cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="median")

# Fully manual
cleaned_df, report = handle_outliers(
    df.copy(), "salary",
    detection_method="Iqr_method",
    replacement="winsorization"
)
```

---

## Pre-Cleaning Summary Reports

Use `before_cleaning_summary()` to generate a diagnostic report **before** any data modification:

```python
from autooutlier import before_cleaning_summary

summary = before_cleaning_summary(df, "salary")
print(summary)
```

The report includes:

| Field | Description |
|---|---|
| `Column` | The column name being analyzed. |
| `Suggested_Detection Method` | The detection method the package recommends. |
| `Handling Method` | The handling method the package recommends. |
| `Skewness` | The skewness coefficient of the data. |
| `Distribution` | Human-readable distribution classification. |
| `Outlier Count` | Number of detected outliers. |
| `Outlier Percentage` | Percentage of data points that are outliers. |

> [!TIP]
> Use `before_cleaning_summary()` in exploratory data analysis (EDA) to quickly assess which columns have outlier problems before deciding on a cleaning strategy.

---

## Post-Cleaning Reports

The second return value from `handle_outliers()` is an after-cleaning report:

```python
cleaned_df, report = handle_outliers(df.copy(), "salary")
print(report)
```

The post-cleaning report includes:

| Field | Description |
|---|---|
| `Column` | The column name that was cleaned. |
| `Detection Method` | The detection method that was used. |
| `Handling Method` | The handling method that was applied. |
| `Outlier Count` | Number of remaining outliers after cleaning. |
| `Outlier Percentage` | Percentage of remaining outliers. |
| `Skewness` | Skewness of the data after cleaning. |
| `Distribution` | Distribution classification after cleaning. |

This lets you verify that the cleaning was effective and compare before/after statistics.

---

## Manual Method Selection

### Choosing a Detection Method

```python
# IQR Method — robust for most distributions
cleaned_df, report = handle_outliers(df.copy(), "col", detection_method="Iqr_method")

# Z-Score — best for normally distributed data
cleaned_df, report = handle_outliers(df.copy(), "col", detection_method="z_score")

# Modified Z-Score — robust against skewed data
cleaned_df, report = handle_outliers(df.copy(), "col", detection_method="modified_z_score")

# Percentile — flags values outside the 5th–95th percentile
cleaned_df, report = handle_outliers(df.copy(), "col", detection_method="percentile")
```

### Choosing a Handling Method

```python
# Replace with median
cleaned_df, report = handle_outliers(df.copy(), "col", replacement="median")

# Replace with mean
cleaned_df, report = handle_outliers(df.copy(), "col", replacement="mean")

# Replace with mode
cleaned_df, report = handle_outliers(df.copy(), "col", replacement="mode")

# Winsorization — cap at IQR fences
cleaned_df, report = handle_outliers(df.copy(), "col", replacement="winsorization")

# Interpolation — estimate from neighbors
cleaned_df, report = handle_outliers(df.copy(), "col", replacement="interpolate")

# Forward fill — use the last valid value
cleaned_df, report = handle_outliers(df.copy(), "col", replacement="ffill")

# Backward fill — use the next valid value
cleaned_df, report = handle_outliers(df.copy(), "col", replacement="bfill")

# Remove outlier rows entirely
cleaned_df, report = handle_outliers(df.copy(), "col", replacement="remove")
```

---

## Custom Value Replacement

To replace outliers with a specific value:

```python
cleaned_df, report = handle_outliers(
    df.copy(), "salary",
    replacement="custom",
    value=0
)
```

> [!IMPORTANT]
> When using `replacement='custom'`, you **must** provide the `value` parameter. If `value` is `None`, the function will print a warning message.

---

## Working with Multiple Columns

`autooutlier` processes one column at a time. To handle multiple columns, loop through them:

```python
import pandas as pd
from autooutlier import handle_outliers, before_cleaning_summary

df = pd.DataFrame({
    "salary": [35000, 42000, 250000, 40000, 38000],
    "age":    [25, 30, 28, 95, 32],
    "score":  [85, 90, 88, 92, 500],
})

numeric_columns = ["salary", "age", "score"]

# Generate summaries for all columns
for col in numeric_columns:
    summary = before_cleaning_summary(df, col)
    print(f"\n--- {col} ---")
    print(summary.to_string(index=False))

# Clean all columns
cleaned_df = df.copy()
for col in numeric_columns:
    cleaned_df, report = handle_outliers(cleaned_df, col)
    print(f"\n{col} cleaning report:")
    print(report.to_string(index=False))
```

---

## Statistical Analysis Functions

The `autooutlier.statistics` module provides foundational statistical functions used internally by the detection and handling algorithms. You can also use them directly:

```python
from autooutlier.statistics import (
    mean, median, mode, std, var, data_range,
    q1, q3, iqr, skew, skew_measurment,
    is_normal, kurtosis, kurtosis_measurement
)

series = df["salary"]

print(f"Mean: {mean(series)}")
print(f"Median: {median(series)}")
print(f"Std Dev: {std(series)}")
print(f"IQR: {iqr(series)}")
print(f"Skewness: {skew(series)}")
print(f"Distribution: {skew_measurment(series)}")
print(f"Is Normal: {is_normal(series)}")
print(f"Kurtosis: {kurtosis(series)}")
print(f"Kurtosis Type: {kurtosis_measurement(series)}")
```

---

## Data Validation

`autooutlier` includes built-in validation checks:

### Non-Numeric Columns

If you pass a non-numeric column, functions return an error message:

```python
df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})

result = handle_outliers(df, "name")
print(result)  # "It is Not a Numerical Data"
```

### Binary Columns

If a column has exactly 2 unique values, `handle_outliers()` will print a warning:

```python
df = pd.DataFrame({"flag": [0, 1, 0, 1, 0, 1]})

cleaned_df, report = handle_outliers(df.copy(), "flag")
# Prints: "Binary columns are not suitable for outlier detection"
```

> [!NOTE]
> The function still proceeds with outlier handling for binary columns — the message is a warning, not an error.

---

## Best Practices

1. **Always use `df.copy()`** — Pass a copy to `handle_outliers()` to preserve your original data.

2. **Inspect before cleaning** — Use `before_cleaning_summary()` to understand the data before making changes.

3. **Verify after cleaning** — Check the post-cleaning report to ensure outliers were handled effectively.

4. **Start with automatic mode** — Let `autooutlier` choose the methods first, then override only if needed.

5. **Process columns individually** — Handle one column at a time for maximum control and transparency.

6. **Consider domain knowledge** — Not all statistical outliers are errors. Use your domain expertise to decide whether to remove or replace them.

7. **Use visualization** — Visualize data before and after cleaning with `box_plot()` to verify results. See [Visualization](visualization.md).

---

## Next Steps

- **[Detection Methods](detection_methods.md)** — Deep dive into each detection algorithm.
- **[Handling Methods](handling_methods.md)** — Understand every replacement strategy.
- **[API Reference](api_reference.md)** — Complete function and parameter reference.
- **[Examples](examples.md)** — Practical, end-to-end examples.

---

**Next:** [Detection Methods →](detection_methods.md)
