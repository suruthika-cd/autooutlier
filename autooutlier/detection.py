# -*- coding: utf-8 -*-
"""Outlier detection methods."""

import numpy as np

from .statistics import mean, std, q1, q3, iqr, skew_measurment
from .utils import is_numeric


def Iqr_method(data,column):
    q1_value=q1(data[column])
    q3_value=q3(data[column])
    IQR=iqr(data[column])
    LowerFence=q1_value-1.5*IQR
    upperFence=q3_value+1.5*IQR
    outliers=(data[column]>upperFence) | (data[column]<LowerFence)
    return outliers

def z_score_method(data,column):
    mean_value=mean(data[column])
    std_value=std(data[column])
    if std_value==0:
        return np.zeros(len(data),dtype=bool)
    z_score=(data[column]-mean_value)/std_value
    outliers=abs(z_score)>3
    return outliers

def modified_z_score(data,column):
    median_value=data[column].median()
    absolute_value=abs(data[column]-median_value)
    MAD=absolute_value.median()
    if MAD==0:
        return np.zeros(len(data),dtype=bool)
    modified_z_score=0.6745*(data[column]-median_value)/MAD
    outliers=abs(modified_z_score)>3.5
    return outliers

def percentile_method(data,column):
    lower_limit=np.percentile(data[column],5)
    upper_limit=np.percentile(data[column],95)
    outliers=(data[column]>upper_limit) | (data[column]<lower_limit)
    return outliers

def detect_outlier_method(data,column):
    numeric=is_numeric(data,column)
    if not numeric :
        return "It is not a numerical Column"
    distribution=skew_measurment(data[column])
    if distribution in ['Perfectly Symmetric','Approximately Symmetric']:
        detection_method='z_score'
    elif distribution in ['Highly Right Skewed','Highly Left Skewed','Moderately Right Skewed','Moderately Left Skewed']:
        detection_method='modified_z_score'
    else:
        detection_method='Iqr_method'
    return detection_method

def detect_outliers(data,column):
    method=detect_outlier_method(data,column)

    if method == 'z_score':
       return z_score_method(data,column)

    elif method == 'modified_z_score':
      return modified_z_score(data,column)

    else:
       return Iqr_method(data,column)
