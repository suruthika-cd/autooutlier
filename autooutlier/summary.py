# -*- coding: utf-8 -*-
"""Summary report generation for outlier analysis."""

import pandas as pd

from .statistics import skew, skew_measurment
from .utils import outlier_count, outlier_percentage
from .detection import detect_outliers, detect_outlier_method
from .handling import detect_handler


def before_cleaning_summary(data, column):
    outliers = detect_outliers(data, column)

    report = {
        "Column": [column],
        "Suggested_Detection Method": [detect_outlier_method(data,column)],
        "Handling Method": [detect_handler(data,column)],
        "Skewness": [skew(data[column])],
        "Distribution": [skew_measurment(data[column])],
        "Outlier Count": [outlier_count(outliers)],
        "Outlier Percentage": [outlier_percentage(outliers)]
    }

    return pd.DataFrame(report)
