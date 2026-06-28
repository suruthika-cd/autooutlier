# -*- coding: utf-8 -*-
"""Tests for autooutlier.summary module."""

import pandas as pd
import pytest

from autooutlier.summary import before_cleaning_summary


@pytest.fixture
def sample_df():
    """Create a sample DataFrame with an obvious outlier."""
    data = [10, 12, 14, 11, 13, 100, 15, 12, 14, 11]
    return pd.DataFrame({"values": data})


class TestBeforeCleaningSummary:
    def test_returns_dataframe(self, sample_df):
        result = before_cleaning_summary(sample_df, "values")
        assert isinstance(result, pd.DataFrame)

    def test_has_expected_columns(self, sample_df):
        result = before_cleaning_summary(sample_df, "values")
        expected_cols = [
            "Column",
            "Suggested_Detection Method",
            "Handling Method",
            "Skewness",
            "Distribution",
            "Outlier Count",
            "Outlier Percentage",
        ]
        for col in expected_cols:
            assert col in result.columns

    def test_column_value(self, sample_df):
        result = before_cleaning_summary(sample_df, "values")
        assert result["Column"].iloc[0] == "values"

    def test_outlier_count_positive(self, sample_df):
        result = before_cleaning_summary(sample_df, "values")
        assert result["Outlier Count"].iloc[0] >= 0
