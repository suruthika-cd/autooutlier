# Handling Methods

`autooutlier` provides ten different strategies for handling detected outliers. This page explains each method in detail, when it is automatically selected, and how to use it.

---

## Table of Contents

- [Overview](#overview)
- [Automatic Handler Selection](#automatic-handler-selection)
- [Winsorization](#winsorization)
- [Mean Replacement](#mean-replacement)
- [Median Replacement](#median-replacement)
- [Mode Replacement](#mode-replacement)
- [Interpolation](#interpolation)
- [Forward Fill](#forward-fill)
- [Backward Fill](#backward-fill)
- [Custom Value Replacement](#custom-value-replacement)
- [Remove Outliers](#remove-outliers)
- [Choosing the Right Method](#choosing-the-right-method)

---

## Overview

All handling methods are applied after outliers have been detected. They modify the DataFrame to replace or remove outlier values.

| Method | `replacement` Value | Modifies Shape? | Description |
|---|---|---|---|
| Winsorization | `'winsorization'` | No | Caps values at IQR fences |
| Mean | `'mean'` | No | Replaces outliers with column mean |
| Median | `'median'` | No | Replaces outliers with column median |
| Mode | `'mode'` | No | Replaces outliers with column mode |
| Interpolation | `'interpolate'` | No | Estimates values from neighbors |
| Forward Fill | `'ffill'` | No | Uses last valid observation |
| Backward Fill | `'bfill'` | No | Uses next valid observation |
| Custom Value | `'custom'` | No | Replaces with a user-specified value |
| Remove | `'remove'` | **Yes** | Deletes outlier rows entirely |

> [!IMPORTANT]
> The `'remove'` method is the only handling strategy that changes the number of rows in the DataFrame. All other methods preserve the DataFrame shape.

---

## Automatic Handler Selection

When you use `replacement='auto'`, the `detect_handler()` function selects the best handling strategy based on data characteristics:

```python
from autooutlier.handling import detect_handler

handler = detect_handler(df, "column_name")
print(handler)
# Output: "interpolate", "winsorization", "median", or "mean"
```

### Selection Logic

The automatic handler evaluates the following conditions **in order of priority**:

```
┌─────────────────────────────┐
│  Is the column a datetime   │── Yes ──▶ interpolate
│  (time series)?             │
└──────────┬──────────────────┘
           │ No
┌──────────▼──────────────────┐
│  Is the data continuous     │── Yes ──▶ interpolate
│  (monotonic)?               │
└──────────┬──────────────────┘
           │ No
┌──────────▼──────────────────┐
│  Outlier percentage ≤ 5%?   │── Yes ──▶ winsorization
└──────────┬──────────────────┘
           │ No
┌──────────▼──────────────────┐
│  Is the data skewed?        │── Yes ──▶ median
└──────────┬──────────────────┘
           │ No
┌──────────▼──────────────────┐
│  Is the data symmetric?     │── Yes ──▶ mean
└──────────┬──────────────────┘
           │ No
           ▼
        median (fallback)
```

| Priority | Condition | Handler |
|---|---|---|
| 1 | Time series data | `interpolate` |
| 2 | Continuous/monotonic data | `interpolate` |
| 3 | Outlier percentage ≤ 5% | `winsorization` |
| 4 | Skewed distribution | `median` |
| 5 | Symmetric distribution | `mean` |
| 6 | Fallback | `median` |

---

## Winsorization

### How It Works

Winsorization **caps** extreme values at the IQR fence boundaries instead of replacing them with a single statistic. Values above the upper fence are set to the upper fence value, and values below the lower fence are set to the lower fence value.

- **Upper Fence** = Q3 + 1.5 × IQR
- **Lower Fence** = Q1 − 1.5 × IQR

### Usage

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="winsorization")
```

Or use the function directly:

```python
from autooutlier.handling import winsorization

cleaned_df = winsorization(df.copy(), "salary")
```

### When to Use

- ✅ Preserves data distribution shape
- ✅ Good when outlier percentage is small (≤ 5%)
- ✅ Retains all rows
- ❌ May not be ideal when outliers represent genuine data errors

> [!NOTE]
> Unlike other handling methods, `winsorization()` does **not** require an outlier mask parameter — it calculates the fences internally and caps all values outside them.

### Example

```python
import pandas as pd
from autooutlier.handling import winsorization

df = pd.DataFrame({"values": [1, 2, 3, 4, 5, 6, 7, 100]})
cleaned = winsorization(df.copy(), "values")
print(cleaned["values"].tolist())
# The extreme value 100 is capped to the upper fence
```

---

## Mean Replacement

### How It Works

Outlier values are replaced with the **arithmetic mean** of the column.

### Usage

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="mean")
```

Or use the function directly:

```python
from autooutlier.handling import replace_with_mean

# outlier_mask is a boolean Series from a detection method
cleaned_df = replace_with_mean(df.copy(), "salary", outlier_mask)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Column name to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask indicating outlier positions. |

### When to Use

- ✅ Best for normally distributed (symmetric) data
- ✅ Preserves the overall mean of the dataset
- ❌ Affected by existing outliers (the mean itself may be skewed)
- ❌ Not suitable for skewed distributions

---

## Median Replacement

### How It Works

Outlier values are replaced with the **median** of the column.

### Usage

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="median")
```

Or use the function directly:

```python
from autooutlier.handling import replace_with_median

cleaned_df = replace_with_median(df.copy(), "salary", outlier_mask)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Column name to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask indicating outlier positions. |

### When to Use

- ✅ Robust to extreme values — the median is not pulled by outliers
- ✅ Best default for skewed distributions
- ✅ The most commonly used replacement in data science
- ❌ May slightly underestimate central tendency for symmetric data

> [!TIP]
> Median replacement is the safest general-purpose handling method. When in doubt, use `replacement='median'`.

---

## Mode Replacement

### How It Works

Outlier values are replaced with the **mode** (most frequent value) of the column.

### Usage

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="mode")
```

Or use the function directly:

```python
from autooutlier.handling import replace_with_mode

cleaned_df = replace_with_mode(df.copy(), "salary", outlier_mask)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Column name to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask indicating outlier positions. |

### When to Use

- ✅ Useful for discrete numerical data
- ✅ Good when the most common value is meaningful
- ❌ May not make sense for continuous data with many unique values
- ❌ If no single mode exists, uses the first mode returned by Pandas

---

## Interpolation

### How It Works

Outlier values are first set to `NaN`, then filled using Pandas' `interpolate()` method (linear interpolation by default). This estimates the outlier values based on their neighboring data points.

### Usage

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="interpolate")
```

Or use the function directly:

```python
from autooutlier.handling import interpolate

cleaned_df = interpolate(df.copy(), "salary", outlier_mask)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Column name to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask indicating outlier positions. |

### When to Use

- ✅ Ideal for time series and sequential data
- ✅ Ideal for continuous/monotonic data
- ✅ Preserves trends and patterns
- ❌ Requires data to have a meaningful order
- ❌ May produce unexpected results for randomly ordered data

> [!WARNING]
> Interpolation works best when the data has a natural ordering (e.g., time series). For randomly ordered datasets, consider median or winsorization instead.

---

## Forward Fill

### How It Works

Outlier values are first set to `NaN`, then filled using the **last valid observation** (`ffill()`). If the first row(s) are outliers and have no preceding value, they are filled using backward fill as a fallback.

### Usage

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="ffill")
```

Or use the function directly:

```python
from autooutlier.handling import replace_with_forward_fill

cleaned_df = replace_with_forward_fill(df.copy(), "salary", outlier_mask)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Column name to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask indicating outlier positions. |

### When to Use

- ✅ Useful for ordered or sequential data
- ✅ Propagates the last known good value
- ❌ Can propagate stale values over long stretches of outliers

---

## Backward Fill

### How It Works

Outlier values are first set to `NaN`, then filled using the **next valid observation** (`bfill()`). If the last row(s) are outliers and have no following value, they are filled using forward fill as a fallback.

### Usage

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="bfill")
```

Or use the function directly:

```python
from autooutlier.handling import replace_with_backward_fill

cleaned_df = replace_with_backward_fill(df.copy(), "salary", outlier_mask)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Column name to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask indicating outlier positions. |

### When to Use

- ✅ Useful when the next valid value is more relevant than the previous
- ✅ Good for data with end alignment
- ❌ Can propagate values backward over long stretches of outliers

---

## Custom Value Replacement

### How It Works

Outlier values are replaced with a **user-specified value**.

### Usage

```python
from autooutlier import handle_outliers

# Replace all outliers with 0
cleaned_df, report = handle_outliers(
    df.copy(), "salary",
    replacement="custom",
    value=0
)

# Replace with any specific value
cleaned_df, report = handle_outliers(
    df.copy(), "salary",
    replacement="custom",
    value=45000
)
```

Or use the function directly:

```python
from autooutlier.handling import replace_with_custom_value

cleaned_df = replace_with_custom_value(df.copy(), "salary", outlier_mask, 0)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Column name to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask indicating outlier positions. |
| `value` | numeric | The replacement value. |

> [!IMPORTANT]
> When using `replacement='custom'` via `handle_outliers()`, you **must** provide the `value` parameter. If `value` is `None`, a warning message is printed.

### When to Use

- ✅ Full control over the replacement value
- ✅ Useful when domain knowledge dictates a specific fill value
- ✅ Common use case: replacing outliers with 0, -1, or a sentinel value
- ❌ Requires domain expertise to choose an appropriate value

---

## Remove Outliers

### How It Works

Rows containing outlier values are **completely removed** from the DataFrame.

### Usage

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", replacement="remove")
```

Or use the function directly:

```python
from autooutlier.handling import remove_outliers

cleaned_df = remove_outliers(df.copy(), "salary", outlier_mask)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | The input DataFrame. |
| `column` | `str` | Column name to process. |
| `outliers` | `pd.Series` (bool) | Boolean mask indicating outlier positions. |

> [!CAUTION]
> This is the only handling method that **reduces the number of rows** in the DataFrame. Use with care — removing rows can introduce bias and reduce statistical power, especially if the outlier percentage is significant.

### When to Use

- ✅ Appropriate when outliers are clearly data entry errors
- ✅ Useful when outlier percentage is very small
- ❌ Loses data — reduces dataset size
- ❌ Can introduce selection bias
- ❌ Not recommended for small datasets

---

## Choosing the Right Method

| Scenario | Recommended Method |
|---|---|
| Not sure / want a safe default | `'auto'` (let the package decide) |
| Time series or sequential data | `'interpolate'`, `'ffill'`, or `'bfill'` |
| Small outlier percentage (≤ 5%) | `'winsorization'` |
| Normally distributed data | `'mean'` |
| Skewed data | `'median'` |
| Discrete numerical data | `'mode'` |
| Outliers are clear errors | `'remove'` |
| Domain-specific fill value needed | `'custom'` |

> [!TIP]
> When in doubt, start with `replacement='auto'`. Review the post-cleaning report, and override manually only if the results aren't satisfactory.

---

## Related Pages

- **[Detection Methods](detection_methods.md)** — How outliers are identified.
- **[User Guide](user_guide.md)** — Complete workflow walkthrough.
- **[API Reference](api_reference.md)** — Full function signatures and parameters.
- **[Examples](examples.md)** — Practical end-to-end examples.

---

**Next:** [Visualization →](visualization.md)
