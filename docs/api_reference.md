# API Reference

Complete reference documentation for every public function and module in `autooutlier`.

---

## Table of Contents

- [Top-Level API](#top-level-api)
- [Module: `autooutlier.detection`](#module-autooutlierdetection)
- [Module: `autooutlier.handling`](#module-autooutlierhandling)
- [Module: `autooutlier.summary`](#module-autooutliersummary)
- [Module: `autooutlier.statistics`](#module-autooutlierstatistics)
- [Module: `autooutlier.visualization`](#module-autooutliervisualization)
- [Module: `autooutlier.utils`](#module-autooutlierutils)
- [Module: `autooutlier.version`](#module-autooutlierversion)

---

## Top-Level API

The following functions are available directly from the `autooutlier` namespace:

```python
from autooutlier import (
    handle_outliers,
    before_cleaning_summary,
    detect_outliers,
    detect_outlier_method,
    __version__,
)
```

| Name | Source Module | Description |
|---|---|---|
| `handle_outliers` | `autooutlier.handling` | Detect and handle outliers in a single call. |
| `before_cleaning_summary` | `autooutlier.summary` | Generate a pre-cleaning diagnostic report. |
| `detect_outliers` | `autooutlier.detection` | Automatically detect outliers and return a boolean mask. |
| `detect_outlier_method` | `autooutlier.detection` | Return the suggested detection method name. |
| `__version__` | `autooutlier.version` | Package version string. |

---

## Module: `autooutlier.detection`

Outlier detection algorithms.

```python
from autooutlier.detection import (
    Iqr_method,
    z_score_method,
    modified_z_score,
    percentile_method,
    detect_outlier_method,
    detect_outliers,
)
```

---

### `Iqr_method(data, column)`

Detect outliers using the Interquartile Range method.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the numeric column to analyze. |

**Returns:** `pd.Series` of `bool` — `True` for outlier rows and `False` for non-outlier rows.

**Algorithm:** Values beyond Q1 − 1.5×IQR (lower fence) or Q3 + 1.5×IQR (upper fence) are marked as outliers.

**Example:**

```python
from autooutlier.detection import Iqr_method

outlier_mask = Iqr_method(df, "salary")
print(df[outlier_mask])  # Show rows with outliers
```

---

### `z_score_method(data, column)`

Detect outliers using the Z-Score method.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the numeric column to analyze. |

**Returns:** `pd.Series` of `bool` — `True` for outlier rows.

**Algorithm:** Computes `z = (x - mean) / std`. Values with `|z| > 3` are marked as outliers. If the standard deviation is 0, returns all `False`.

**Example:**

```python
from autooutlier.detection import z_score_method

outlier_mask = z_score_method(df, "temperature")
```

---

### `modified_z_score(data, column)`

Detect outliers using the Modified Z-Score method (MAD-based).

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the numeric column to analyze. |

**Returns:** `pd.Series` of `bool` — `True` for outlier rows.

**Algorithm:** Computes `modified_z = 0.6745 × (x - median) / MAD`. Values with `|modified_z| > 3.5` are marked as outliers. If MAD is 0, returns all `False`.

**Example:**

```python
from autooutlier.detection import modified_z_score

outlier_mask = modified_z_score(df, "income")
```

---

### `percentile_method(data, column)`

Detect outliers using the Percentile method.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the numeric column to analyze. |

**Returns:** `pd.Series` of `bool` — `True` for outlier rows.

**Algorithm:** Values below the 5th percentile or above the 95th percentile are marked as outliers.

**Example:**

```python
from autooutlier.detection import percentile_method

outlier_mask = percentile_method(df, "scores")
```

---

### `detect_outlier_method(data, column)`

Determine the best outlier detection method for the given data based on skewness.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the numeric column to analyze. |

**Returns:** `str` — One of `'z_score'`, `'modified_z_score'`, `'Iqr_method'`, or `"It is not a numerical Column"` if the column is non-numeric.

**Example:**

```python
from autooutlier import detect_outlier_method

method = detect_outlier_method(df, "salary")
print(method)  # e.g., "modified_z_score"
```

---

### `detect_outliers(data, column)`

Automatically detect outliers using the best method for the data.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the numeric column to analyze. |

**Returns:** `pd.Series` of `bool` — `True` for outlier rows.

**Behavior:** Calls `detect_outlier_method()` to determine the best method, then applies it.

**Example:**

```python
from autooutlier import detect_outliers

outlier_mask = detect_outliers(df, "salary")
print(f"Found {outlier_mask.sum()} outliers")
```

---

## Module: `autooutlier.handling`

Outlier handling and replacement strategies.

```python
from autooutlier.handling import (
    winsorization,
    interpolate,
    replace_with_mean,
    replace_with_median,
    replace_with_mode,
    replace_with_custom_value,
    replace_with_forward_fill,
    replace_with_backward_fill,
    remove_outliers,
    is_binary,
    detect_handler,
    handle_outliers,
)
```

---

### `handle_outliers(data, column, detection_method='auto', replacement='auto', value=None)`

**The primary function of the package.** Detects and handles outliers in a single call.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `pd.DataFrame` | *required* | The input DataFrame. |
| `column` | `str` | *required* | Name of the numeric column to process. |
| `detection_method` | `str` | `'auto'` | Detection method to use. Options: `'auto'`, `'Iqr_method'`, `'z_score'`, `'modified_z_score'`, `'percentile'`. |
| `replacement` | `str` | `'auto'` | Handling method to use. Options: `'auto'`, `'interpolate'`, `'winsorization'`, `'median'`, `'mean'`, `'mode'`, `'custom'`, `'remove'`, `'bfill'`, `'ffill'`. |
| `value` | numeric or `None` | `None` | Custom replacement value. Required when `replacement='custom'`. |

**Returns:** `tuple` of `(pd.DataFrame, pd.DataFrame)`:

1. **Cleaned DataFrame** — Data with outliers handled.
2. **After-cleaning report** — DataFrame with columns: `Column`, `Detection Method`, `Handling Method`, `Outlier Count`, `Outlier Percentage`, `Skewness`, `Distribution`.

**Returns:** `str` — If the column is non-numeric, returns `"It is Not a Numerical Data"`.

> [!WARNING]
> This function may modify the input DataFrame in place. Always pass `df.copy()` if you need to preserve the original.

**Example:**

```python
from autooutlier import handle_outliers

# Fully automatic
cleaned_df, report = handle_outliers(df.copy(), "salary")

# Manual detection and handling
cleaned_df, report = handle_outliers(
    df.copy(), "salary",
    detection_method="z_score",
    replacement="median"
)

# Custom value replacement
cleaned_df, report = handle_outliers(
    df.copy(), "salary",
    replacement="custom",
    value=0
)
```

---

### `winsorization(data, column)`

Cap outlier values at the IQR fence boundaries.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame (modified in place). |
| `column` | `str` | Name of the column to process. |

**Returns:** `pd.DataFrame` — The DataFrame with values capped.

> [!NOTE]
> This function converts the column to `float` dtype internally.

---

### `interpolate(data, column, outliers)`

Replace outliers using linear interpolation.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame (modified in place). |
| `column` | `str` | Name of the column to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask from a detection method. |

**Returns:** `pd.DataFrame` — The DataFrame with outliers interpolated.

---

### `replace_with_mean(data, column, outliers)`

Replace outlier values with the column mean.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame (modified in place). |
| `column` | `str` | Name of the column to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask from a detection method. |

**Returns:** `pd.DataFrame` — The DataFrame with outliers replaced by the mean.

---

### `replace_with_median(data, column, outliers)`

Replace outlier values with the column median.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame (modified in place). |
| `column` | `str` | Name of the column to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask from a detection method. |

**Returns:** `pd.DataFrame` — The DataFrame with outliers replaced by the median.

---

### `replace_with_mode(data, column, outliers)`

Replace outlier values with the column mode.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame (modified in place). |
| `column` | `str` | Name of the column to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask from a detection method. |

**Returns:** `pd.DataFrame` — The DataFrame with outliers replaced by the mode.

---

### `replace_with_custom_value(data, column, outliers, value)`

Replace outlier values with a user-specified value.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame (modified in place). |
| `column` | `str` | Name of the column to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask from a detection method. |
| `value` | numeric | The replacement value. |

**Returns:** `pd.DataFrame` — The DataFrame with outliers replaced by the custom value.

---

### `replace_with_forward_fill(data, column, outliers)`

Replace outlier values using forward fill (last valid observation), with backward fill as fallback.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame (modified in place). |
| `column` | `str` | Name of the column to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask from a detection method. |

**Returns:** `pd.DataFrame` — The DataFrame with outliers forward-filled.

---

### `replace_with_backward_fill(data, column, outliers)`

Replace outlier values using backward fill (next valid observation), with forward fill as fallback.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame (modified in place). |
| `column` | `str` | Name of the column to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask from a detection method. |

**Returns:** `pd.DataFrame` — The DataFrame with outliers backward-filled.

---

### `remove_outliers(data, column, outliers)`

Remove rows identified as outliers from the DataFrame.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the column (used for identification). |
| `outliers` | `pd.Series` (bool) | Boolean mask from a detection method. |

**Returns:** `pd.DataFrame` — A new DataFrame with outlier rows removed.

> [!CAUTION]
> This is the only handling method that changes the number of rows.

---

### `is_binary(data, column)`

Check if a column contains exactly 2 unique values.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the column to check. |

**Returns:** `bool` — `True` if the column has exactly 2 unique values.

---

### `detect_handler(data, column)`

Determine the best outlier handling method based on data characteristics.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the numeric column to analyze. |

**Returns:** `str` — One of `'interpolate'`, `'winsorization'`, `'median'`, `'mean'`, or `"It is not a numerical Column"`.

---

## Module: `autooutlier.summary`

Summary report generation.

```python
from autooutlier.summary import before_cleaning_summary
```

---

### `before_cleaning_summary(data, column)`

Generate a pre-cleaning diagnostic report for a column.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the numeric column to analyze. |

**Returns:** `pd.DataFrame` — A single-row DataFrame with the following columns:

| Column | Type | Description |
|---|---|---|
| `Column` | `str` | The column name analyzed. |
| `Suggested_Detection Method` | `str` | Recommended detection method. |
| `Handling Method` | `str` | Recommended handling method. |
| `Skewness` | `float` | Skewness coefficient. |
| `Distribution` | `str` | Distribution classification. |
| `Outlier Count` | `int` | Number of detected outliers. |
| `Outlier Percentage` | `float` | Percentage of outliers. |

**Example:**

```python
from autooutlier import before_cleaning_summary

summary = before_cleaning_summary(df, "salary")
print(summary.to_string(index=False))
```

---

## Module: `autooutlier.statistics`

Statistical functions for data analysis and distribution classification.

```python
from autooutlier.statistics import (
    mean, median, mode, std, var, data_range,
    q1, q3, iqr, skew, skew_measurment,
    is_normal, kurtosis, kurtosis_measurement,
)
```

---

### `mean(data)`

Compute the arithmetic mean.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `median(data)`

Compute the median.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `mode(data)`

Compute the mode (most frequent value).

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `pd.Series` — A Series of mode values (may have multiple modes).

---

### `std(data)`

Compute the standard deviation.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `var(data)`

Compute the variance.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `data_range(data)`

Compute the range (max − min).

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `q1(data)`

Compute the first quartile (25th percentile).

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `q3(data)`

Compute the third quartile (75th percentile).

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `iqr(data)`

Compute the interquartile range (Q3 − Q1).

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `skew(data)`

Compute the skewness using SciPy's unbiased estimator.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `skew_measurment(data)`

Classify the distribution based on skewness.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `str` — One of:

| Return Value | Skewness Range |
|---|---|
| `"Perfectly Symmetric"` | `s == 0` |
| `"Approximately Symmetric"` | `-0.5 ≤ s ≤ 0.5` |
| `"Moderately Right Skewed"` | `0.5 ≤ s ≤ 1` |
| `"Moderately Left Skewed"` | `-1 ≤ s ≤ -0.5` |
| `"Highly Right Skewed"` | `s > 1` |
| `"Highly Left Skewed"` | `s < -1` |

---

### `is_normal(data)`

Check if the data is approximately normally distributed (based on skewness).

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `bool` — `True` if `|skewness| < 0.5`.

---

### `kurtosis(data)`

Compute the excess kurtosis.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `float`

---

### `kurtosis_measurement(data)`

Classify the distribution tail weight based on kurtosis.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` | A numeric Series. |

**Returns:** `str` — One of:

| Return Value | Kurtosis Value |
|---|---|
| `"Normal Distribution"` | `k == 0` |
| `"Heavier Tail"` | `k > 0` (leptokurtic) |
| `"Lighter Tail"` | `k < 0` (platykurtic) |

---

## Module: `autooutlier.visualization`

Visualization tools for outlier analysis.

```python
from autooutlier.visualization import box_plot
```

---

### `box_plot(data)`

Display a Seaborn box plot for the given data.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.Series` or array-like | Numerical data to visualize. |

**Returns:** `None` — Displays the plot via `plt.show()`.

**Example:**

```python
from autooutlier.visualization import box_plot

box_plot(df["salary"])
```

> [!NOTE]
> Seaborn and Matplotlib are imported lazily inside this function.

---

## Module: `autooutlier.utils`

Internal utility functions for data validation and outlier statistics.

```python
from autooutlier.utils import (
    is_numeric,
    is_time_series,
    is_continous,
    outlier_count,
    outlier_percentage,
)
```

---

### `is_numeric(data, column)`

Check if a column contains numeric data.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the column to check. |

**Returns:** `bool`

---

### `is_time_series(data, column)`

Check if a column contains datetime data.

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the column to check. |

**Returns:** `bool`

---

### `is_continous(data, column)`

Check if a numeric column is continuous (monotonically increasing or decreasing).

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Name of the column to check. |

**Returns:** `bool` — `True` if the column is numeric **and** monotonic.

---

### `outlier_count(outliers)`

Count the number of outliers in a boolean mask.

| Parameter | Type | Description |
|---|---|---|
| `outliers` | `pd.Series` (bool) | Boolean outlier mask. |

**Returns:** `int`

---

### `outlier_percentage(outliers)`

Calculate the percentage of outliers in a boolean mask.

| Parameter | Type | Description |
|---|---|---|
| `outliers` | `pd.Series` (bool) | Boolean outlier mask. |

**Returns:** `float` — Percentage (0–100).

---

## Module: `autooutlier.version`

Package version information.

```python
from autooutlier.version import __version__
```

### `__version__`

**Type:** `str`

The current package version. Currently: `"0.1.0"`.

---

## Related Pages

- **[User Guide](user_guide.md)** — How to use these functions in practice.
- **[Detection Methods](detection_methods.md)** — Theory behind detection algorithms.
- **[Handling Methods](handling_methods.md)** — Theory behind handling strategies.
- **[Examples](examples.md)** — Practical usage examples.

---

**Next:** [Examples →](examples.md)
