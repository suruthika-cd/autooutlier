# Changelog

All notable changes to `autooutlier` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2024-01-01

### Added

- **Initial release** of `autooutlier`.

#### Statistics Module (`autooutlier.statistics`)

- `mean(data)` — Compute arithmetic mean.
- `median(data)` — Compute median.
- `mode(data)` — Compute mode.
- `std(data)` — Compute standard deviation.
- `var(data)` — Compute variance.
- `data_range(data)` — Compute range (max − min).
- `q1(data)` — Compute first quartile (25th percentile).
- `q3(data)` — Compute third quartile (75th percentile).
- `iqr(data)` — Compute interquartile range.
- `skew(data)` — Compute skewness (unbiased, via SciPy).
- `skew_measurment(data)` — Classify distribution by skewness.
- `is_normal(data)` — Check if data is approximately normal.
- `kurtosis(data)` — Compute excess kurtosis.
- `kurtosis_measurement(data)` — Classify tail weight.

#### Detection Module (`autooutlier.detection`)

- `Iqr_method(data, column)` — IQR-based outlier detection.
- `z_score_method(data, column)` — Z-Score outlier detection.
- `modified_z_score(data, column)` — Modified Z-Score (MAD-based) outlier detection.
- `percentile_method(data, column)` — Percentile-based outlier detection.
- `detect_outlier_method(data, column)` — Automatic detection method selection based on skewness.
- `detect_outliers(data, column)` — Automatic outlier detection.

#### Handling Module (`autooutlier.handling`)

- `winsorization(data, column)` — Cap values at IQR fences.
- `interpolate(data, column, outliers)` — Linear interpolation replacement.
- `replace_with_mean(data, column, outliers)` — Mean replacement.
- `replace_with_median(data, column, outliers)` — Median replacement.
- `replace_with_mode(data, column, outliers)` — Mode replacement.
- `replace_with_custom_value(data, column, outliers, value)` — Custom value replacement.
- `replace_with_forward_fill(data, column, outliers)` — Forward fill replacement.
- `replace_with_backward_fill(data, column, outliers)` — Backward fill replacement.
- `remove_outliers(data, column, outliers)` — Remove outlier rows.
- `detect_handler(data, column)` — Automatic handling method selection.
- `handle_outliers(data, column, ...)` — Full detection + handling pipeline.

#### Summary Module (`autooutlier.summary`)

- `before_cleaning_summary(data, column)` — Pre-cleaning diagnostic report.

#### Visualization Module (`autooutlier.visualization`)

- `box_plot(data)` — Box plot visualization using Seaborn.

#### Utility Module (`autooutlier.utils`)

- `is_numeric(data, column)` — Check if column is numeric.
- `is_time_series(data, column)` — Check if column is datetime.
- `is_continous(data, column)` — Check if column is monotonic.
- `outlier_count(outliers)` — Count outliers from boolean mask.
- `outlier_percentage(outliers)` — Calculate outlier percentage.

#### Infrastructure

- Automatic detection method selection based on data distribution skewness.
- Automatic handling method selection based on data characteristics (time series, continuity, outlier percentage, distribution).
- Professional package structure with `pyproject.toml`.
- Test suite (`tests/`).
- Usage examples (`examples/`).
- MIT License.

---

## Versioning

This project uses **Semantic Versioning** (`MAJOR.MINOR.PATCH`):

- **MAJOR** — Incompatible API changes.
- **MINOR** — New features, backward-compatible.
- **PATCH** — Bug fixes, backward-compatible.

---

## Links

- **Repository**: [https://github.com/suruthika-cd/autooutlier](https://github.com/suruthika-cd/autooutlier)
- **PyPI**: [https://pypi.org/project/autooutlier/](https://pypi.org/project/autooutlier/)
- **Issues**: [https://github.com/suruthika-cd/autooutlier/issues](https://github.com/suruthika-cd/autooutlier/issues)
