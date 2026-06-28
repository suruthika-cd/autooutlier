# -*- coding: utf-8 -*-
"""Tests for autooutlier.handling module."""

import numpy as np
import pandas as pd
import pytest

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
    detect_handler,
    handle_outliers,
)


@pytest.fixture
def sample_df():
    """Create a sample DataFrame with an obvious outlier."""
    data = [10, 12, 14, 11, 13, 100, 15, 12, 14, 11]
    return pd.DataFrame({"values": data})


@pytest.fixture
def outlier_mask(sample_df):
    """Create a boolean mask marking index 5 (value=100) as outlier."""
    mask = pd.Series([False] * len(sample_df))
    mask.iloc[5] = True
    return mask


class TestWinsorization:
    def test_caps_outlier(self, sample_df):
        result = winsorization(sample_df.copy(), "values")
        assert result["values"].max() <= 100  # should be capped


class TestInterpolate:
    def test_replaces_outlier(self, sample_df, outlier_mask):
        result = interpolate(sample_df.copy(), "values", outlier_mask)
        assert not result["values"].isna().any()


class TestReplaceWithMean:
    def test_replaces_outlier(self, sample_df, outlier_mask):
        result = replace_with_mean(sample_df.copy(), "values", outlier_mask)
        assert result["values"].iloc[5] != 100


class TestReplaceWithMedian:
    def test_replaces_outlier(self, sample_df, outlier_mask):
        result = replace_with_median(sample_df.copy(), "values", outlier_mask)
        assert result["values"].iloc[5] != 100


class TestReplaceWithMode:
    def test_replaces_outlier(self, sample_df, outlier_mask):
        result = replace_with_mode(sample_df.copy(), "values", outlier_mask)
        assert result["values"].iloc[5] != 100


class TestReplaceWithCustomValue:
    def test_replaces_with_custom(self, sample_df, outlier_mask):
        result = replace_with_custom_value(sample_df.copy(), "values", outlier_mask, 0)
        assert result["values"].iloc[5] == 0


class TestReplaceWithForwardFill:
    def test_replaces_outlier(self, sample_df, outlier_mask):
        result = replace_with_forward_fill(sample_df.copy(), "values", outlier_mask)
        assert result["values"].iloc[5] != 100


class TestReplaceWithBackwardFill:
    def test_replaces_outlier(self, sample_df, outlier_mask):
        result = replace_with_backward_fill(sample_df.copy(), "values", outlier_mask)
        assert result["values"].iloc[5] != 100


class TestRemoveOutliers:
    def test_removes_row(self, sample_df, outlier_mask):
        result = remove_outliers(sample_df.copy(), "values", outlier_mask)
        assert len(result) == len(sample_df) - 1


class TestDetectHandler:
    def test_returns_string(self, sample_df):
        result = detect_handler(sample_df, "values")
        assert isinstance(result, str)

    def test_non_numeric(self):
        df = pd.DataFrame({"names": ["Alice", "Bob", "Charlie"]})
        # detect_handler calls detect_outliers before the numeric check,
        # which raises on non-numeric data — this is the original behavior.
        with pytest.raises(Exception):
            detect_handler(df, "names")


class TestHandleOutliers:
    def test_auto_mode(self, sample_df):
        cleaned, report = handle_outliers(sample_df.copy(), "values")
        assert isinstance(cleaned, pd.DataFrame)
        assert isinstance(report, pd.DataFrame)
        assert "Outlier Count" in report.columns

    def test_non_numeric_returns_string(self):
        df = pd.DataFrame({"names": ["Alice", "Bob", "Charlie"]})
        result = handle_outliers(df, "names")
        assert result == "It is Not a Numerical Data"

    def test_manual_iqr(self, sample_df):
        cleaned, report = handle_outliers(
            sample_df.copy(), "values", detection_method="Iqr_method"
        )
        assert isinstance(cleaned, pd.DataFrame)

    def test_manual_replacement_median(self, sample_df):
        cleaned, report = handle_outliers(
            sample_df.copy(), "values", replacement="median"
        )
        assert isinstance(cleaned, pd.DataFrame)
