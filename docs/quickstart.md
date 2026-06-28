# Quick Start

Get up and running with `autooutlier` in under 5 minutes. This guide walks you through the most common workflows.

---

## 1. Import the Package

```python
import pandas as pd
from autooutlier import handle_outliers, before_cleaning_summary, detect_outliers
```

---

## 2. Prepare Your Data

`autooutlier` works with **Pandas DataFrames**. Your data must contain at least one numerical column.

```python
df = pd.DataFrame({
    "salary": [
        35000, 42000, 38000, 40000, 45000, 250000, 37000,
        41000, 43000, 39000, 44000, 36000, 42000, 38000, 41000,
    ]
})
```

---

## 3. Get a Pre-Cleaning Summary

Before making any changes, generate a summary report to understand your data:

```python
summary = before_cleaning_summary(df, "salary")
print(summary)
```

Output:

```
  Column Suggested_Detection Method Handling Method  Skewness        Distribution  Outlier Count  Outlier Percentage
  salary            modified_z_score          median  3.872983  Highly Right Skewed              1            6.666667
```

The summary tells you:

- **Which detection method** the package recommends (based on skewness)
- **Which handling method** it will use (based on data characteristics)
- **How many outliers** exist and their percentage

---

## 4. Detect Outliers

To see which rows are outliers without modifying the data:

```python
outlier_mask = detect_outliers(df, "salary")
print(f"Number of outliers: {outlier_mask.sum()}")
print(df[outlier_mask])
```

Output:

```
Number of outliers: 1
   salary
5  250000
```

> [!TIP]
> `detect_outliers()` returns a boolean Series. Use it to filter your DataFrame: `df[outlier_mask]` shows only the outlier rows.

---

## 5. Automatically Handle Outliers

Let `autooutlier` choose the best detection and handling methods for you:

```python
cleaned_df, report = handle_outliers(df.copy(), "salary")
print(report)
print(cleaned_df)
```

> [!IMPORTANT]
> Always pass `df.copy()` if you want to preserve your original DataFrame. `handle_outliers()` may modify the data in place.

The function returns a **tuple** of two items:

1. **`cleaned_df`** — The DataFrame with outliers handled.
2. **`report`** — A summary DataFrame showing what was done.

---

## 6. Use Manual Methods

You can override the automatic selection by specifying detection and/or handling methods:

```python
# Use Z-Score detection with median replacement
cleaned_df, report = handle_outliers(
    df.copy(), "salary",
    detection_method="z_score",
    replacement="median"
)
```

Available detection methods: `'auto'`, `'Iqr_method'`, `'z_score'`, `'modified_z_score'`, `'percentile'`

Available replacement methods: `'auto'`, `'interpolate'`, `'winsorization'`, `'median'`, `'mean'`, `'mode'`, `'custom'`, `'remove'`, `'bfill'`, `'ffill'`

---

## Complete Quick Start Example

Here's a self-contained script you can copy and run:

```python
import pandas as pd
from autooutlier import (
    handle_outliers,
    before_cleaning_summary,
    detect_outliers,
    detect_outlier_method,
)

# Create sample data with an outlier
df = pd.DataFrame({
    "salary": [35000, 42000, 38000, 40000, 45000, 250000, 37000,
               41000, 43000, 39000, 44000, 36000, 42000, 38000, 41000]
})

# Step 1: Check which detection method is recommended
method = detect_outlier_method(df, "salary")
print(f"Recommended detection method: {method}")

# Step 2: Get a pre-cleaning summary
summary = before_cleaning_summary(df, "salary")
print("\nBefore Cleaning Summary:")
print(summary.to_string(index=False))

# Step 3: Detect outliers
outlier_mask = detect_outliers(df, "salary")
print(f"\nOutliers found: {outlier_mask.sum()}")
print("Outlier rows:")
print(df[outlier_mask].to_string(index=False))

# Step 4: Handle outliers automatically
cleaned_df, report = handle_outliers(df.copy(), "salary")
print("\nAfter Cleaning Report:")
print(report.to_string(index=False))

print("\nCleaned Data:")
print(cleaned_df.to_string(index=False))
```

---

## What's Next?

- **[User Guide](user_guide.md)** — Comprehensive walkthrough of all features.
- **[Detection Methods](detection_methods.md)** — Deep dive into how each detection algorithm works.
- **[Handling Methods](handling_methods.md)** — Understand every replacement strategy.
- **[Examples](examples.md)** — More practical, real-world usage scenarios.

---

**Next:** [User Guide →](user_guide.md)
