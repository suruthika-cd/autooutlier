# -*- coding: utf-8 -*-
"""Tests for autooutlier.statistics module."""

import numpy as np
import pandas as pd
import pytest

from autooutlier.statistics import (
    mean,
    median,
    mode,
    std,
    var,
    data_range,
    q1,
    q3,
    iqr,
    skew,
    skew_measurment,
    is_normal,
    kurtosis,
    kurtosis_measurement,
)


@pytest.fixture
def sample_series():
    """Create a simple numeric Series."""
    return pd.Series([10, 12, 14, 11, 13, 15, 12, 14, 11, 13])


class TestMean:
    def test_correct_value(self, sample_series):
        result = mean(sample_series)
        assert result == pytest.approx(sample_series.mean())


class TestMedian:
    def test_correct_value(self, sample_series):
        result = median(sample_series)
        assert result == pytest.approx(sample_series.median())


class TestMode:
    def test_returns_series(self, sample_series):
        result = mode(sample_series)
        assert isinstance(result, pd.Series)


class TestStd:
    def test_correct_value(self, sample_series):
        result = std(sample_series)
        assert result == pytest.approx(sample_series.std())


class TestVar:
    def test_correct_value(self, sample_series):
        result = var(sample_series)
        assert result == pytest.approx(sample_series.var())


class TestDataRange:
    def test_correct_value(self, sample_series):
        result = data_range(sample_series)
        assert result == 5  # 15 - 10


class TestQ1:
    def test_correct_value(self, sample_series):
        result = q1(sample_series)
        assert result == pytest.approx(np.percentile(sample_series, 25))


class TestQ3:
    def test_correct_value(self, sample_series):
        result = q3(sample_series)
        assert result == pytest.approx(np.percentile(sample_series, 75))


class TestIqr:
    def test_correct_value(self, sample_series):
        result = iqr(sample_series)
        expected = np.percentile(sample_series, 75) - np.percentile(sample_series, 25)
        assert result == pytest.approx(expected)


class TestSkew:
    def test_returns_float(self, sample_series):
        result = skew(sample_series)
        assert isinstance(result, (float, np.floating))


class TestSkewMeasurement:
    def test_returns_string(self, sample_series):
        result = skew_measurment(sample_series)
        assert isinstance(result, str)

    def test_symmetric_data(self):
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result = skew_measurment(data)
        assert result == "Perfectly Symmetric"


class TestIsNormal:
    def test_returns_bool(self, sample_series):
        result = is_normal(sample_series)
        assert isinstance(result, bool)

    def test_symmetric_is_normal(self):
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert is_normal(data) is True


class TestKurtosis:
    def test_returns_float(self, sample_series):
        result = kurtosis(sample_series)
        assert isinstance(result, (float, np.floating))


class TestKurtosisMeasurement:
    def test_returns_string(self, sample_series):
        result = kurtosis_measurement(sample_series)
        assert isinstance(result, str)
        assert result in ["Normal Distribution", "Heavier Tail", "Lighter Tail"]
