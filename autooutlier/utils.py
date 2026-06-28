# -*- coding: utf-8 -*-
"""Utility functions for outlier detection."""

import pandas as pd


def is_numeric(data,column):
    return pd.api.types.is_numeric_dtype(data[column])

def is_time_series(data,column):
    return pd.api.types.is_datetime64_any_dtype(data[column])

def is_continous(data,column):
    numeric=is_numeric(data,column)
    return ( numeric==True and (data[column].is_monotonic_increasing or data[column].is_monotonic_decreasing))

def outlier_count(outliers):
    return outliers.sum()

def outlier_percentage(outliers):
    return (outliers.sum()/len(outliers))*100
