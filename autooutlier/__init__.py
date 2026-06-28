# -*- coding: utf-8 -*-
"""
autooutlier - Automatic Outlier Detection and Handling for Python
=================================================================

A professional Python package for automatic outlier detection,
handling, and statistical analysis of numerical data.

Usage:
    >>> import autooutlier
    >>> from autooutlier import handle_outliers, detect_outliers
"""

from .handling import handle_outliers
from .summary import before_cleaning_summary
from .detection import detect_outliers
from .detection import detect_outlier_method
from .version import __version__
    
__all__ = [
    "handle_outliers",
    "before_cleaning_summary",
    "detect_outliers",
    "detect_outlier_method",
    "__version__",
]
