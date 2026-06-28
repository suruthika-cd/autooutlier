# -*- coding: utf-8 -*-
"""
basic_usage.py - Example demonstrating how to use the autooutlier package.

Run this script from the project root:
    python -m examples.basic_usage
Or directly:
    python examples/basic_usage.py
"""

import pandas as pd
from autooutlier import (
    handle_outliers,
    before_cleaning_summary,
    detect_outliers,
    detect_outlier_method,
    __version__,
)

print(f"autooutlier v{__version__}")
print("=" * 60)

# -----------------------------------------------------------
# 1. Create sample data with outliers
# -----------------------------------------------------------
data = {
    "salary": [
        35000, 42000, 38000, 40000, 45000, 250000, 37000,
        41000, 43000, 39000, 44000, 36000, 42000, 38000, 41000,
    ],
    "age": [25, 30, 28, 35, 32, 29, 31, 27, 33, 26, 34, 28, 30, 29, 31],
}
df = pd.DataFrame(data)

print("\n[1] Original Data:")
print(df.to_string(index=False))

# -----------------------------------------------------------
# 2. Detect the suggested outlier method
# -----------------------------------------------------------
method = detect_outlier_method(df, "salary")
print(f"\n[2] Suggested detection method for 'salary': {method}")

# -----------------------------------------------------------
# 3. Detect outliers
# -----------------------------------------------------------
outlier_mask = detect_outliers(df, "salary")
print(f"\n[3] Outliers detected: {outlier_mask.sum()}")
print("Outlier rows:")
print(df[outlier_mask].to_string(index=False))

# -----------------------------------------------------------
# 4. Pre-cleaning summary
# -----------------------------------------------------------
summary = before_cleaning_summary(df, "salary")
print("\n[4] Before Cleaning Summary:")
print(summary.to_string(index=False))

# -----------------------------------------------------------
# 5. Handle outliers (automatic mode)
# -----------------------------------------------------------
cleaned_df, report = handle_outliers(df.copy(), "salary")
print("\n[5] After Cleaning Report:")
print(report.to_string(index=False))

print("\nCleaned Data:")
print(cleaned_df.to_string(index=False))

# -----------------------------------------------------------
# 6. Handle outliers with manual method selection
# -----------------------------------------------------------
cleaned_df2, report2 = handle_outliers(
    df.copy(), "salary", detection_method="z_score", replacement="median"
)
print("\n[6] After Cleaning Report (manual z_score + median):")
print(report2.to_string(index=False))

print("\nDone!")
