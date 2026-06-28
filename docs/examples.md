# Examples

Practical, end-to-end usage examples for `autooutlier`. Each example is self-contained and can be copied and run directly.

---

## Table of Contents

- [Example 1: Basic Outlier Detection and Handling](#example-1-basic-outlier-detection-and-handling)
- [Example 2: Exploring Statistical Summary](#example-2-exploring-statistical-summary)
- [Example 3: Comparing Detection Methods](#example-3-comparing-detection-methods)
- [Example 4: Comparing Handling Methods](#example-4-comparing-handling-methods)
- [Example 5: Cleaning Multiple Columns](#example-5-cleaning-multiple-columns)
- [Example 6: Custom Value Replacement](#example-6-custom-value-replacement)
- [Example 7: Working with Skewed Data](#example-7-working-with-skewed-data)
- [Example 8: Before and After Comparison](#example-8-before-and-after-comparison)
- [Example 9: Using Individual Statistical Functions](#example-9-using-individual-statistical-functions)
- [Example 10: Complete Data Cleaning Pipeline](#example-10-complete-data-cleaning-pipeline)

---

## Example 1: Basic Outlier Detection and Handling

The simplest way to use `autooutlier` — let it automatically detect and handle outliers.

```python
import pandas as pd
from autooutlier import handle_outliers, detect_outliers

# Create sample data with obvious outliers
df = pd.DataFrame({
    "salary": [35000, 42000, 38000, 40000, 45000, 250000, 37000,
               41000, 43000, 39000, 44000, 36000, 42000, 38000, 41000]
})

# Step 1: Detect outliers
outlier_mask = detect_outliers(df, "salary")
print(f"Outliers found: {outlier_mask.sum()}")
print("Outlier rows:")
print(df[outlier_mask])
print()

# Step 2: Handle outliers automatically
cleaned_df, report = handle_outliers(df.copy(), "salary")
print("Cleaning report:")
print(report.to_string(index=False))
print()
print("Cleaned data:")
print(cleaned_df.to_string(index=False))
```

---

## Example 2: Exploring Statistical Summary

Use `before_cleaning_summary()` to get a diagnostic report before making any changes.

```python
import pandas as pd
from autooutlier import before_cleaning_summary

# Sample dataset
df = pd.DataFrame({
    "temperature": [22.1, 23.5, 21.8, 24.0, 22.5, 55.0, 23.0, 22.8, 21.5, 23.2],
    "pressure":    [1013, 1015, 1010, 1012, 1014, 1013, 1100, 1011, 1013, 1012],
})

# Generate summary for each column
for col in ["temperature", "pressure"]:
    summary = before_cleaning_summary(df, col)
    print(f"\n--- Summary for '{col}' ---")
    print(summary.to_string(index=False))
```

Expected output includes:

- The suggested detection method
- The suggested handling method
- Skewness and distribution classification
- Outlier count and percentage

---

## Example 3: Comparing Detection Methods

Apply all four detection methods to the same data and compare results.

```python
import pandas as pd
from autooutlier.detection import (
    Iqr_method, z_score_method, modified_z_score, percentile_method
)

df = pd.DataFrame({
    "values": [10, 12, 11, 13, 14, 12, 10, 11, 100, 13, 12, 11, 14, 10, 12]
})

methods = {
    "IQR": Iqr_method,
    "Z-Score": z_score_method,
    "Modified Z-Score": modified_z_score,
    "Percentile": percentile_method,
}

print("Detection Method Comparison")
print("=" * 45)
for name, method in methods.items():
    outliers = method(df, "values")
    print(f"{name:20s} → {outliers.sum()} outliers detected")
    if outliers.sum() > 0:
        print(f"{'':20s}   Outlier values: {df.loc[outliers, 'values'].tolist()}")
```

---

## Example 4: Comparing Handling Methods

Apply different handling methods and compare the results.

```python
import pandas as pd
from autooutlier import handle_outliers

df = pd.DataFrame({
    "price": [100, 120, 110, 115, 105, 900, 108, 112, 118, 103]
})

methods = ["median", "mean", "winsorization", "interpolate", "remove"]

print("Handling Method Comparison")
print("=" * 60)
for method in methods:
    cleaned_df, report = handle_outliers(df.copy(), "price", replacement=method)
    remaining = report["Outlier Count"].values[0]
    print(f"\n--- {method} ---")
    print(f"  Remaining outliers: {remaining}")
    print(f"  Cleaned values: {cleaned_df['price'].tolist()}")
    print(f"  New mean: {cleaned_df['price'].mean():.2f}")
```

---

## Example 5: Cleaning Multiple Columns

Process all numeric columns in a DataFrame.

```python
import pandas as pd
from autooutlier import handle_outliers, before_cleaning_summary
from autooutlier.utils import is_numeric

df = pd.DataFrame({
    "salary":      [35000, 42000, 250000, 40000, 38000, 41000, 39000, 43000],
    "age":         [25, 30, 28, 95, 32, 29, 31, 27],
    "experience":  [2, 5, 3, 4, 6, 3, 4, 5],
    "department":  ["HR", "IT", "HR", "IT", "HR", "IT", "HR", "IT"],
})

# Process only numeric columns
numeric_cols = [col for col in df.columns if is_numeric(df, col)]

print("Pre-Cleaning Analysis")
print("=" * 70)
for col in numeric_cols:
    summary = before_cleaning_summary(df, col)
    print(f"\n{col}:")
    print(summary.to_string(index=False))

# Clean all numeric columns
print("\n\nCleaning Process")
print("=" * 70)
cleaned_df = df.copy()
for col in numeric_cols:
    cleaned_df, report = handle_outliers(cleaned_df, col)
    outlier_count = report["Outlier Count"].values[0]
    method = report["Handling Method"].values[0]
    print(f"{col}: handled with '{method}' — {outlier_count} outliers remaining")

print("\nCleaned DataFrame:")
print(cleaned_df.to_string(index=False))
```

---

## Example 6: Custom Value Replacement

Replace outliers with a domain-specific value.

```python
import pandas as pd
from autooutlier import handle_outliers

# Sensor data where negative values are physically impossible
df = pd.DataFrame({
    "sensor_reading": [50, 52, 48, 51, -100, 53, 49, 50, 47, 300]
})

# Replace outliers with the sensor's known baseline value of 50
cleaned_df, report = handle_outliers(
    df.copy(), "sensor_reading",
    detection_method="Iqr_method",
    replacement="custom",
    value=50
)

print("Original data:")
print(df["sensor_reading"].tolist())
print("\nCleaned data:")
print(cleaned_df["sensor_reading"].tolist())
print("\nReport:")
print(report.to_string(index=False))
```

---

## Example 7: Working with Skewed Data

Demonstrate how `autooutlier` handles skewed distributions.

```python
import numpy as np
import pandas as pd
from autooutlier import detect_outlier_method, before_cleaning_summary, handle_outliers
from autooutlier.statistics import skew, skew_measurment

# Generate right-skewed data (e.g., income distribution)
np.random.seed(42)
incomes = np.concatenate([
    np.random.normal(50000, 10000, 90),   # Normal incomes
    np.random.normal(200000, 30000, 10),   # High incomes
])
df = pd.DataFrame({"income": incomes})

# Check distribution
print(f"Skewness: {skew(df['income']):.4f}")
print(f"Distribution: {skew_measurment(df['income'])}")
print(f"Suggested method: {detect_outlier_method(df, 'income')}")
print()

# Get summary
summary = before_cleaning_summary(df, "income")
print("Before cleaning:")
print(summary.to_string(index=False))
print()

# Clean
cleaned_df, report = handle_outliers(df.copy(), "income")
print("After cleaning:")
print(report.to_string(index=False))
print()

print(f"Original mean: ${df['income'].mean():,.2f}")
print(f"Cleaned mean:  ${cleaned_df['income'].mean():,.2f}")
```

---

## Example 8: Before and After Comparison

Compare key statistics before and after cleaning.

```python
import pandas as pd
from autooutlier import handle_outliers, before_cleaning_summary
from autooutlier.statistics import mean, median, std, skew

df = pd.DataFrame({
    "scores": [72, 85, 90, 78, 65, 88, 500, 82, 91, 76, 84, 70, 79, 87, 83]
})

# Before cleaning stats
print("BEFORE CLEANING")
print(f"  Mean:     {mean(df['scores']):.2f}")
print(f"  Median:   {median(df['scores']):.2f}")
print(f"  Std Dev:  {std(df['scores']):.2f}")
print(f"  Skewness: {skew(df['scores']):.4f}")

# Summary report
summary = before_cleaning_summary(df, "scores")
print(f"\n  Summary report:")
print(summary.to_string(index=False))

# Clean
cleaned_df, report = handle_outliers(df.copy(), "scores")

# After cleaning stats
print(f"\nAFTER CLEANING")
print(f"  Mean:     {mean(cleaned_df['scores']):.2f}")
print(f"  Median:   {median(cleaned_df['scores']):.2f}")
print(f"  Std Dev:  {std(cleaned_df['scores']):.2f}")
print(f"  Skewness: {skew(cleaned_df['scores']):.4f}")
print(f"\n  Cleaning report:")
print(report.to_string(index=False))
```

---

## Example 9: Using Individual Statistical Functions

Access the underlying statistical utility functions.

```python
import pandas as pd
from autooutlier.statistics import (
    mean, median, mode, std, var, data_range,
    q1, q3, iqr, skew, skew_measurment,
    is_normal, kurtosis, kurtosis_measurement
)

data = pd.Series([10, 12, 14, 11, 13, 15, 12, 14, 11, 13])

print("Statistical Analysis")
print("=" * 40)
print(f"Mean:              {mean(data):.2f}")
print(f"Median:            {median(data):.2f}")
print(f"Mode:              {mode(data).tolist()}")
print(f"Std Deviation:     {std(data):.2f}")
print(f"Variance:          {var(data):.2f}")
print(f"Range:             {data_range(data):.2f}")
print(f"Q1 (25th pctl):    {q1(data):.2f}")
print(f"Q3 (75th pctl):    {q3(data):.2f}")
print(f"IQR:               {iqr(data):.2f}")
print(f"Skewness:          {skew(data):.4f}")
print(f"Distribution:      {skew_measurment(data)}")
print(f"Is Normal:         {is_normal(data)}")
print(f"Kurtosis:          {kurtosis(data):.4f}")
print(f"Kurtosis Type:     {kurtosis_measurement(data)}")
```

---

## Example 10: Complete Data Cleaning Pipeline

A full end-to-end workflow for cleaning a dataset.

```python
import pandas as pd
from autooutlier import (
    handle_outliers,
    before_cleaning_summary,
    detect_outliers,
    detect_outlier_method,
)
from autooutlier.visualization import box_plot
from autooutlier.utils import is_numeric

# ── Step 1: Load Data ──────────────────────────────────────
df = pd.DataFrame({
    "salary":     [35000, 42000, 38000, 40000, 45000, 250000, 37000,
                   41000, 43000, 39000, 44000, 36000, 42000, 38000, 41000],
    "age":        [25, 30, 28, 35, 32, 29, 31, 27, 33, 26, 34, 28, 30, 29, 31],
    "bonus":      [2000, 2500, 2200, 2300, 50000, 2100, 2400, 2300, 2600, 2000,
                   2500, 2100, 2200, 2400, 2300],
})

print("=" * 60)
print("STEP 1: Original Data")
print("=" * 60)
print(df.to_string(index=False))
print(f"\nShape: {df.shape}")

# ── Step 2: Pre-Cleaning Analysis ──────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Pre-Cleaning Analysis")
print("=" * 60)

numeric_cols = [col for col in df.columns if is_numeric(df, col)]

for col in numeric_cols:
    print(f"\n--- {col} ---")
    method = detect_outlier_method(df, col)
    print(f"  Detection method: {method}")

    outliers = detect_outliers(df, col)
    print(f"  Outliers found: {outliers.sum()}")

    if outliers.sum() > 0:
        print(f"  Outlier values: {df.loc[outliers, col].tolist()}")

    summary = before_cleaning_summary(df, col)
    print(summary.to_string(index=False))

# ── Step 3: Visualize (optional) ───────────────────────────
# Uncomment the following lines to display box plots:
# for col in numeric_cols:
#     print(f"\nBox plot for {col}:")
#     box_plot(df[col])

# ── Step 4: Clean Data ─────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: Cleaning")
print("=" * 60)

cleaned_df = df.copy()
reports = []

for col in numeric_cols:
    cleaned_df, report = handle_outliers(cleaned_df, col)
    reports.append(report)
    outlier_count = report["Outlier Count"].values[0]
    detection = report["Detection Method"].values[0]
    handling = report["Handling Method"].values[0]
    print(f"  {col}: {detection} + {handling} → {outlier_count} remaining outliers")

# ── Step 5: Results ────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: Cleaned Data")
print("=" * 60)
print(cleaned_df.to_string(index=False))
print(f"\nShape: {cleaned_df.shape}")

# ── Step 6: All Reports ────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: All Cleaning Reports")
print("=" * 60)
all_reports = pd.concat(reports, ignore_index=True)
print(all_reports.to_string(index=False))
```

---

## Related Pages

- **[Quick Start](quickstart.md)** — The fastest way to get started.
- **[User Guide](user_guide.md)** — Comprehensive feature walkthrough.
- **[API Reference](api_reference.md)** — Complete function reference.
- **[Detection Methods](detection_methods.md)** — How each detection algorithm works.
- **[Handling Methods](handling_methods.md)** — How each handling strategy works.

---

**Next:** [FAQ →](faq.md)
