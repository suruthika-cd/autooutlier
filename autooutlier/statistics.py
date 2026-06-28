# -*- coding: utf-8 -*-
"""Statistical functions for outlier detection."""

import numpy as np
from scipy.stats import skew as scipy_skew


def mean(data):
    return data.mean()

def median(data):
    return data.median()

def mode(data):
    return data.mode()

def std(data):
    return data.std()

def var(data):
    return data.var()

def data_range(data):
    return data.max()-data.min()

def q1(data):
    a= np.percentile(data,25)
    return a

def q3(data):
     b= np.percentile(data,75)
     return b

def iqr(data):
     return q3(data)-q1(data)

def skew(data):
    return scipy_skew(data,bias=False)

def skew_measurment(data):
    s=skew(data)
    if s==0:
        return "Perfectly Symmetric"
    if  s >= -0.5and s <= 0.5:
        return "Approximately Symmetric"
    if s >= 0.5 and s<= 1:
        return "Moderately Right Skewed"
    if s>1:
        return "Highly Right Skewed"
    if s<-1:
        return "Highly Left Skewed"
    if s>=-1 and s<=-0.5:
        return "Moderately Left Skewed"

def is_normal(data):
    s=skew(data)
    if (abs(s)<0.5):
        return True
    return False

def kurtosis(data):
    return data.kurt()

def kurtosis_measurement(data):
    k=kurtosis(data)
    if k==0:
        return "Normal Distribution"
    if k>0:
        return "Heavier Tail"
    if k<0:
        return "Lighter Tail"
