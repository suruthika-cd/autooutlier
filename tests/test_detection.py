# -*- coding: utf-8 -*-
"""Tests for autooutlier.detection module."""

import numpy as np
import pandas as pd
import pytest

from autooutlier.detection import (
    Iqr_method,
    z_score_method,
    modified_z_score,
    percentile_method,
    detect_outlier_method,
    detect_outliers,
)


@pytest.fixture
def sample_df():
    """Create a sample DataFrame with an obvious outlier."""
    data = [10, 12, 14, 11, 13, 100, 15, 12, 14, 11]
    return pd.DataFrame({"values": data})


@pytest.fixture
def normal_df():
    """Create a roughly symmetric DataFrame."""
    np.random.seed(42)
    data = np.random.normal(loc=50, scale=5, size=100).tolist()
    return pd.DataFrame({"values": data})


class TestIqrMethod:
    def test_returns_boolean_series(self, sample_df):
        result = Iqr_method(sample_df, "values")
        assert result.dtype == bool

    def test_detects_obvious_outlier(self, sample_df):
        result = Iqr_method(sample_df, "values")
        assert result.sum() >= 1  # At least the 100 should be flagged


class TestZScoreMethod:
    def test_returns_boolean_series(self, sample_df):
        result = z_score_method(sample_df, "values")
        assert result.dtype == bool

    def test_handles_zero_std(self):
        df = pd.DataFrame({"values": [5, 5, 5, 5, 5]})
        result = z_score_method(df, "values")
        assert result.sum() == 0


class TestModifiedZScore:
    def test_returns_boolean_series(self, sample_df):
        result = modified_z_score(sample_df, "values")
        assert result.dtype == bool

    def test_handles_zero_mad(self):
        df = pd.DataFrame({"values": [5, 5, 5, 5, 5]})
        result = modified_z_score(df, "values")
        assert result.sum() == 0


class TestPercentileMethod:
    def test_returns_boolean_series(self, sample_df):
        result = percentile_method(sample_df, "values")
        assert result.dtype == bool


class TestDetectOutlierMethod:
    def test_returns_string(self, sample_df):
        result = detect_outlier_method(sample_df, "values")
        assert isinstance(result, str)

    def test_non_numeric_column(self):
        df = pd.DataFrame({"names": ["Alice", "Bob", "Charlie"]})
        result = detect_outlier_method(df, "names")
        assert result == "It is not a numerical Column"

    def test_symmetric_data_returns_z_score(self, normal_df):
        result = detect_outlier_method(normal_df, "values")
        assert result == "z_score"


class TestDetectOutliers:
    def test_returns_boolean_series(self, sample_df):
        result = detect_outliers(sample_df, "values")
        assert result.dtype == bool

    def test_detects_outlier(self, sample_df):
        result = detect_outliers(sample_df, "values")
        assert result.sum() >= 1
