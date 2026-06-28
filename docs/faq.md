# Frequently Asked Questions

Common questions about `autooutlier` and outlier analysis.

---

## General

### What is `autooutlier`?

`autooutlier` is a Python package that automatically detects and handles outliers in numerical data. It analyzes your data distribution and selects the best detection and handling methods — requiring zero configuration.

### What Python versions are supported?

Python **3.8 and later** are supported (3.8, 3.9, 3.10, 3.11, 3.12).

### What data formats does it work with?

`autooutlier` works with **Pandas DataFrames**. Your data must be in a DataFrame with named columns. Individual detection/handling functions work with `pd.Series` or array-like data.

### Is it free to use?

Yes. `autooutlier` is open-source software released under the **MIT License**. You can use it in personal, academic, and commercial projects.

---

## Usage

### Do I need to configure anything?

No. The default behavior (`detection_method='auto'` and `replacement='auto'`) intelligently selects methods based on your data distribution. Just call:

```python
cleaned_df, report = handle_outliers(df.copy(), "column_name")
```

### Can I override the automatic selections?

Yes. You can specify both the detection method and handling method manually:

```python
cleaned_df, report = handle_outliers(
    df.copy(), "column_name",
    detection_method="z_score",
    replacement="median"
)
```

See the [User Guide](user_guide.md) for all available options.

### Does `handle_outliers()` modify my original DataFrame?

Yes, most handling methods **modify the DataFrame in place**. Always pass `df.copy()` if you need to preserve the original:

```python
# ✅ Safe — original df is preserved
cleaned_df, report = handle_outliers(df.copy(), "column_name")

# ❌ Risky — original df may be modified
cleaned_df, report = handle_outliers(df, "column_name")
```

### How do I clean multiple columns?

Loop through your columns:

```python
cleaned_df = df.copy()
for col in ["salary", "age", "score"]:
    cleaned_df, report = handle_outliers(cleaned_df, col)
```

See [Example 5](examples.md#example-5-cleaning-multiple-columns) for a complete example.

### What happens if I pass a non-numeric column?

The function returns the string `"It is Not a Numerical Data"` without modifying the DataFrame:

```python
result = handle_outliers(df, "name_column")
print(result)  # "It is Not a Numerical Data"
```

### What happens with binary columns?

If a column has exactly 2 unique values (e.g., 0 and 1), `handle_outliers()` prints a warning: `"Binary columns are not suitable for outlier detection"`. The function still proceeds with the operation.

---

## Detection Methods

### How does automatic detection work?

The package calculates the **skewness** of your data and selects the method accordingly:

| Distribution | Method |
|---|---|
| Approximately symmetric (`|skew| ≤ 0.5`) | Z-Score |
| Skewed (`|skew| > 0.5`) | Modified Z-Score |
| Fallback | IQR Method |

See [Detection Methods](detection_methods.md) for full details.

### Which detection method should I use?

- **Z-Score** — Best for normally distributed data
- **Modified Z-Score** — Best for skewed data
- **IQR** — Good general-purpose method
- **Percentile** — When you want fixed 5th/95th boundaries

When in doubt, use `'auto'` and let the package decide.

### What thresholds are used?

| Method | Threshold |
|---|---|
| Z-Score | `|z| > 3` |
| Modified Z-Score | `|modified_z| > 3.5` |
| IQR | Beyond Q1 − 1.5×IQR or Q3 + 1.5×IQR |
| Percentile | Outside 5th–95th percentile |

### Can I change the thresholds?

The current version uses fixed thresholds. If you need custom thresholds, you can implement custom detection using the statistical functions:

```python
from autooutlier.statistics import mean, std

# Custom Z-Score with threshold = 2
z_scores = (df["col"] - mean(df["col"])) / std(df["col"])
custom_outliers = abs(z_scores) > 2  # Your custom threshold
```

### What if all values in a column are the same?

If the standard deviation or MAD is 0, the Z-Score and Modified Z-Score methods return **no outliers** (all `False`). This is the correct behavior — identical values have no outliers.

---

## Handling Methods

### How does automatic handling work?

The package evaluates your data characteristics in this priority order:

1. **Time series data** → Interpolation
2. **Continuous/monotonic data** → Interpolation
3. **Low outlier percentage (≤ 5%)** → Winsorization
4. **Skewed distribution** → Median replacement
5. **Symmetric distribution** → Mean replacement
6. **Fallback** → Median replacement

See [Handling Methods](handling_methods.md) for full details.

### Which handling method preserves the most data?

All methods except `'remove'` preserve the DataFrame shape (number of rows). The best-preserving methods are:

- **Winsorization** — Caps values at boundaries (most conservative)
- **Interpolation** — Estimates from neighbors (best for ordered data)
- **Median/Mean** — Simple statistical replacement

### When should I remove outliers instead of replacing them?

Only remove outliers when:

- You're confident they are data entry errors
- The outlier percentage is very small
- Your dataset is large enough that losing rows won't affect analysis

> [!WARNING]
> Removing outliers reduces your dataset size and can introduce selection bias. Prefer replacement methods for most use cases.

### What's the difference between forward fill and backward fill?

- **Forward fill (`ffill`)** — Fills outliers with the last valid (non-outlier) value before them.
- **Backward fill (`bfill`)** — Fills outliers with the next valid value after them.

Both include a fallback to the opposite direction if the outlier is at the beginning or end of the data.

---

## Statistical Functions

### Can I use the statistical functions independently?

Yes. All functions in the `statistics` module work on Pandas Series:

```python
from autooutlier.statistics import mean, median, std, skew

series = df["column_name"]
print(f"Mean: {mean(series)}")
print(f"Skewness: {skew(series)}")
```

### How is skewness calculated?

Skewness is calculated using **SciPy's `skew()` function** with `bias=False` (unbiased estimator). This uses the Fisher-Pearson standardized moment coefficient with the N-1 correction.

### How is kurtosis calculated?

Kurtosis is calculated using **Pandas' `.kurt()` method**, which returns the **excess kurtosis** (Fisher's definition, where normal distribution = 0).

---

## Visualization

### What visualization does the package provide?

The package includes a `box_plot()` function that creates Seaborn box plots:

```python
from autooutlier.visualization import box_plot

box_plot(df["salary"])
```

See [Visualization](visualization.md) for more examples including custom plots.

### Can I customize the box plot?

The built-in `box_plot()` function uses default Seaborn styling. For custom visualizations, use Matplotlib and Seaborn directly with the outlier masks from `detect_outliers()`. See the [Visualization](visualization.md) page for custom visualization recipes.

---

## Troubleshooting

### I get `ModuleNotFoundError: No module named 'autooutlier'`

Make sure:

1. The package is installed: `pip install autooutlier`
2. You're in the correct Python environment: `python -c "import sys; print(sys.executable)"`
3. Try reinstalling: `pip install --force-reinstall autooutlier`

### The package detects no outliers when I expect some

- Try a different detection method: `detection_method="Iqr_method"` or `detection_method="percentile"`
- Check your data skewness — highly skewed data may cause the Modified Z-Score MAD to be 0
- Use `before_cleaning_summary()` to inspect the data characteristics

### The cleaned data still has outliers

This can happen because:

1. The handling method you chose may not eliminate all outliers (e.g., winsorization caps values but re-detection may still flag borderline points)
2. Handling one outlier may reveal a previously masked outlier

You can run `handle_outliers()` iteratively, but usually one pass is sufficient.

### Performance is slow on large datasets

`autooutlier` uses NumPy and Pandas operations which are vectorized and fast. For very large datasets (millions of rows):

- Process one column at a time
- Avoid the `'remove'` method (creates a copy)
- Consider sampling your data for initial exploration

---

## Related Pages

- **[Installation](installation.md)** — Setup and dependency issues.
- **[User Guide](user_guide.md)** — Comprehensive usage guide.
- **[API Reference](api_reference.md)** — Complete function reference.
- **[Examples](examples.md)** — Practical code examples.

---

**Next:** [Changelog →](changelog.md)
