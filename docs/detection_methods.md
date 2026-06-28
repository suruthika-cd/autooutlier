# Detection Methods

`autooutlier` provides four outlier detection methods. This page explains the theory behind each algorithm, when it is selected automatically, and how to use it manually.

---

## Table of Contents

- [Overview](#overview)
- [Automatic Method Selection](#automatic-method-selection)
- [IQR Method](#iqr-method)
- [Z-Score Method](#z-score-method)
- [Modified Z-Score Method](#modified-z-score-method)
- [Percentile Method](#percentile-method)
- [Choosing the Right Method](#choosing-the-right-method)

---

## Overview

All detection methods accept a DataFrame and column name, and return a **boolean Series** (mask) where `True` indicates an outlier.

| Method | Function | Best For | Threshold |
|---|---|---|---|
| IQR | `Iqr_method(data, column)` | General-purpose, robust | 1.5 × IQR beyond Q1/Q3 |
| Z-Score | `z_score_method(data, column)` | Normally distributed data | \|z\| > 3 |
| Modified Z-Score | `modified_z_score(data, column)` | Skewed data | \|modified z\| > 3.5 |
| Percentile | `percentile_method(data, column)` | Fixed-boundary detection | Outside 5th–95th percentile |

```python
from autooutlier.detection import Iqr_method, z_score_method, modified_z_score, percentile_method

# All return a boolean Series
outlier_mask = Iqr_method(df, "column_name")
```

---

## Automatic Method Selection

The `detect_outlier_method()` function selects the most appropriate detection method based on the **skewness** of the data:

```python
from autooutlier import detect_outlier_method

method = detect_outlier_method(df, "salary")
print(method)  # e.g., "z_score", "modified_z_score", or "Iqr_method"
```

### Selection Logic

```
                    ┌──────────────────┐
                    │  Calculate Skew  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Is numeric?     │──── No ──▶ "Not a numerical Column"
                    └────────┬─────────┘
                             │ Yes
                    ┌────────▼─────────┐
              ┌─────│  Skewness value  │─────┐
              │     └──────────────────┘     │
              │                              │
     Symmetric (|s| ≤ 0.5)          Skewed (|s| > 0.5)
              │                              │
              ▼                              ▼
         Z-Score                    Modified Z-Score
```

| Distribution Classification | Skewness Range | Selected Method |
|---|---|---|
| Perfectly Symmetric | `s == 0` | `z_score` |
| Approximately Symmetric | `-0.5 ≤ s ≤ 0.5` | `z_score` |
| Moderately Right Skewed | `0.5 ≤ s ≤ 1` | `modified_z_score` |
| Moderately Left Skewed | `-1 ≤ s ≤ -0.5` | `modified_z_score` |
| Highly Right Skewed | `s > 1` | `modified_z_score` |
| Highly Left Skewed | `s < -1` | `modified_z_score` |

> [!NOTE]
> The IQR method serves as a fallback and is used when the distribution classification doesn't match any of the above categories. In the current implementation, the primary automatic choices are between Z-Score and Modified Z-Score.

---

## IQR Method

### Theory

The **Interquartile Range (IQR)** method identifies outliers as values that fall beyond the "fences" defined by the first and third quartiles:

- **Q1** = 25th percentile
- **Q3** = 75th percentile
- **IQR** = Q3 − Q1
- **Lower Fence** = Q1 − 1.5 × IQR
- **Upper Fence** = Q3 + 1.5 × IQR

Any value below the lower fence or above the upper fence is flagged as an outlier.

### Usage

```python
from autooutlier.detection import Iqr_method

outlier_mask = Iqr_method(df, "salary")
print(f"Outliers: {outlier_mask.sum()}")
print(df[outlier_mask])
```

Or via `handle_outliers()`:

```python
from autooutlier import handle_outliers

cleaned_df, report = handle_outliers(df.copy(), "salary", detection_method="Iqr_method")
```

### When to Use

- ✅ Works well for most data distributions
- ✅ Robust to extreme values (not influenced by outliers themselves)
- ✅ No assumption of normality required
- ❌ May flag too many values in heavily skewed distributions

### Example

```python
import pandas as pd
from autooutlier.detection import Iqr_method

df = pd.DataFrame({"values": [2, 4, 5, 6, 7, 8, 9, 50]})

outliers = Iqr_method(df, "values")
print(df[outliers])
# Output: 50 is flagged as an outlier
```

---

## Z-Score Method

### Theory

The **Z-Score** method measures how many standard deviations a value is from the mean:

```
z = (x − μ) / σ
```

Where:
- `x` = individual data point
- `μ` = mean of the data
- `σ` = standard deviation of the data

A data point is classified as an outlier if **|z| > 3** (i.e., more than 3 standard deviations from the mean).

### Edge Case Handling

If the standard deviation is 0 (all values are identical), the function returns a boolean array of all `False` (no outliers).

### Usage

```python
from autooutlier.detection import z_score_method

outlier_mask = z_score_method(df, "salary")
```

Or via `handle_outliers()`:

```python
cleaned_df, report = handle_outliers(df.copy(), "salary", detection_method="z_score")
```

### When to Use

- ✅ Ideal for normally (Gaussian) distributed data
- ✅ Statistically grounded threshold (3σ rule)
- ❌ Sensitive to extreme outliers (they inflate the mean and std)
- ❌ Not appropriate for skewed distributions

> [!WARNING]
> The Z-Score method assumes approximately normal distribution. For skewed data, use the Modified Z-Score or IQR method instead.

### Example

```python
import pandas as pd
from autooutlier.detection import z_score_method

df = pd.DataFrame({
    "temperature": [20, 21, 19, 22, 20, 21, 18, 100, 20, 19]
})

outliers = z_score_method(df, "temperature")
print(df[outliers])
# Output: 100 is flagged as an outlier
```

---

## Modified Z-Score Method

### Theory

The **Modified Z-Score** uses the median and **Median Absolute Deviation (MAD)** instead of the mean and standard deviation, making it more robust to skewed data:

```
Modified Z = 0.6745 × (x − median) / MAD
```

Where:
- `MAD` = median(|x − median|)
- `0.6745` is a consistency constant that makes MAD comparable to standard deviation for normal distributions

A data point is classified as an outlier if **|Modified Z| > 3.5**.

### Edge Case Handling

If MAD is 0 (more than half the values are identical), the function returns a boolean array of all `False` (no outliers).

### Usage

```python
from autooutlier.detection import modified_z_score

outlier_mask = modified_z_score(df, "salary")
```

Or via `handle_outliers()`:

```python
cleaned_df, report = handle_outliers(df.copy(), "salary", detection_method="modified_z_score")
```

### When to Use

- ✅ Excellent for skewed distributions
- ✅ Robust to extreme outliers (median-based, not affected by extreme values)
- ✅ Works well when data is not normally distributed
- ❌ May be overly conservative for truly normal data

### Example

```python
import pandas as pd
from autooutlier.detection import modified_z_score

df = pd.DataFrame({
    "income": [30000, 32000, 31000, 35000, 33000, 500000, 29000, 34000]
})

outliers = modified_z_score(df, "income")
print(df[outliers])
# Output: 500000 is flagged as an outlier
```

---

## Percentile Method

### Theory

The **Percentile method** flags any value that falls outside the **5th to 95th percentile** range:

- **Lower limit** = 5th percentile
- **Upper limit** = 95th percentile

Any value below the lower limit or above the upper limit is classified as an outlier.

### Usage

```python
from autooutlier.detection import percentile_method

outlier_mask = percentile_method(df, "salary")
```

Or via `handle_outliers()`:

```python
cleaned_df, report = handle_outliers(df.copy(), "salary", detection_method="percentile")
```

### When to Use

- ✅ Simple and intuitive
- ✅ Always flags approximately 10% of the data
- ✅ No distribution assumptions
- ❌ Arbitrary boundary (always flags roughly the top/bottom 5%)
- ❌ Not adaptive to data shape

> [!NOTE]
> The percentile method uses fixed boundaries (5th and 95th percentile). This means it will always flag approximately 10% of data as outliers, regardless of whether true outliers exist. This makes it useful for trimming extreme tails but less precise for true outlier identification.

### Example

```python
import pandas as pd
from autooutlier.detection import percentile_method

df = pd.DataFrame({
    "scores": list(range(1, 101))  # 1 to 100
})

outliers = percentile_method(df, "scores")
print(f"Outliers flagged: {outliers.sum()}")
print(df[outliers])
# Output: Values 1-5 and 96-100 are flagged
```

---

## Choosing the Right Method

Use this decision guide to select the appropriate detection method:

```
Is your data normally distributed?
├── Yes ──▶ Use Z-Score ('z_score')
└── No
    ├── Is it skewed? ──▶ Use Modified Z-Score ('modified_z_score')
    ├── Not sure? ──▶ Use IQR ('Iqr_method') — safe default
    └── Want fixed boundaries? ──▶ Use Percentile ('percentile')
```

### Summary Comparison

| Criteria | IQR | Z-Score | Modified Z-Score | Percentile |
|---|---|---|---|---|
| Handles normal data | ✅ | ✅ | ✅ | ✅ |
| Handles skewed data | ⚠️ | ❌ | ✅ | ✅ |
| Robust to extremes | ✅ | ❌ | ✅ | ✅ |
| Adapts to data shape | ✅ | ✅ | ✅ | ❌ |
| No assumptions needed | ✅ | ❌ | ⚠️ | ✅ |

> [!TIP]
> When in doubt, use `detection_method='auto'` and let `autooutlier` choose for you. The automatic selection is based on tested statistical heuristics.

---

## Related Pages

- **[Handling Methods](handling_methods.md)** — What to do with detected outliers.
- **[User Guide](user_guide.md)** — Complete workflow walkthrough.
- **[API Reference](api_reference.md)** — Full function signatures and parameters.

---

**Next:** [Handling Methods →](handling_methods.md)
