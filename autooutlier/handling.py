# -*- coding: utf-8 -*-
"""Outlier handling and replacement methods."""

import numpy as np
import pandas as pd

from .statistics import mean, median, mode, q1, q3, iqr, skew, skew_measurment
from .utils import is_numeric, is_time_series, is_continous, outlier_count, outlier_percentage
from .detection import (
    Iqr_method,
    z_score_method,
    modified_z_score,
    percentile_method,
    detect_outlier_method,
    detect_outliers,
)


def winsorization(data,column):
    data[column]=data[column].astype(float)
    q1_value=q1(data[column])
    q3_value=q3(data[column])
    IQR=iqr(data[column])
    LowerFence=q1_value-1.5*IQR
    upperFence=q3_value+1.5*IQR
    data.loc[data[column]>upperFence,column]=upperFence
    data.loc[data[column]<LowerFence,column]=LowerFence
    return data

def interpolate(data,column,outliers):
    data.loc[outliers,column]=np.nan
    data[column]=data[column].interpolate()
    return data

def replace_with_median(data,column,outliers):
    data[column]=data[column].astype(float)
    median_value=median(data[column])
    data.loc[outliers,column]=median_value
    return data

def replace_with_mean(data,column,outliers):
     data[column]=data[column].astype(float)
     mean_value=mean(data[column])
     data.loc[outliers,column]=mean_value
     return data

def replace_with_mode(data,column,outliers):
     data[column]=data[column].astype(float)
     mode_value=mode(data[column]).iloc[0]
     data.loc[outliers,column]=mode_value
     return data

def remove_outliers(data,column,outliers):
    data=data[~outliers].copy()
    return data

def replace_with_custom_value(data,column,outliers,value):
    data.loc[outliers,column]=value
    return data

def replace_with_backward_fill(data,column,outliers):
    data.loc[outliers,column]=np.nan
    data[column]=data[column].bfill().ffill()
    return data

def replace_with_forward_fill(data,column,outliers):
    data.loc[outliers,column]=np.nan
    data[column]=data[column].ffill().bfill()
    return data

def is_binary(data, column):
    return data[column].nunique() == 2

def detect_handler(data,column):
     numeric=is_numeric(data,column)
     outliers=detect_outliers(data,column)
     percentage=outlier_percentage(outliers)
     series=is_time_series(data,column)
     continous=is_continous(data,column)
     distribution=skew_measurment(data[column])
     if not numeric :
        return "It is not a numerical Column"
     if series==True:
       handling_method='interpolate'
     elif continous==True:
        handling_method='interpolate'
     elif percentage<=5:
        handling_method='winsorization'
     elif distribution in ['Highly Right Skewed','Highly Left Skewed','Moderately Right Skewed','Moderately Left Skewed']:
        handling_method='median'
     elif distribution in ['Perfectly Symmetric','Approximately Symmetric']:
        handling_method='mean'
     else:
         handling_method='median'
     return handling_method

def handle_outliers(data,column,detection_method='auto',replacement='auto',value=None):
    numeric_check=is_numeric(data,column)
    if numeric_check==False:
        return "It is Not a Numerical Data"
    if is_binary(data, column):
       print( "Binary columns are not suitable for outlier detection")
    if(detection_method=='auto'):
         detection_method=detect_outlier_method(data,column)
         if detection_method == 'z_score':
            outlier = z_score_method(data,column)

         elif detection_method == 'modified_z_score':
          outlier = modified_z_score(data,column)

         elif detection_method == 'Iqr_method':
           outlier = Iqr_method(data,column)

         elif detection_method == 'percentile':
              outlier = percentile_method(data,column)

         else:
             print( "Invalid Detection Method")
    elif detection_method=='Iqr_method':
        outlier= Iqr_method(data,column)
    elif detection_method=='z_score':
        outlier= z_score_method(data,column)
    elif detection_method=='modified_z_score':
         outlier=modified_z_score(data,column)
    elif detection_method=='percentile':
        outlier=percentile_method(data,column)
    else:
       print( "Invalid Detection Method")
    if (replacement=='auto'):
      replacement=detect_handler(data,column)
      if replacement=='interpolate':
        data= interpolate(data,column,outlier)
      elif replacement=='winsorization':
        data= winsorization(data,column)
      elif replacement=='median':
        data= replace_with_median(data,column,outlier)
      elif replacement=='mode':
        data=replace_with_mode(data,column,outlier)
      elif replacement=='mean':
          data= replace_with_mean(data,column,outlier)
    if replacement=='interpolate':
        data= interpolate(data,column,outlier)
    elif replacement=='winsorization':
        data= winsorization(data,column)
    elif replacement=='median':
        data= replace_with_median(data,column,outlier)
    elif replacement=='mode':
        data= replace_with_mode(data,column,outlier)
    elif replacement=='mean':
          data= replace_with_mean(data,column,outlier)
    elif replacement=='custom':
         if value is None:
             print( "Please Provide Custom Value")
         data=replace_with_custom_value(data,column,outlier,value)
    elif replacement=='remove':
        data=remove_outliers(data,column,outlier)
    elif replacement=='bfill':
        data= replace_with_backward_fill(data,column,outlier)
    elif replacement=='ffill':
        data= replace_with_forward_fill(data,column,outlier)
    else:
        print("Invalid Replacement Method")
    outlier = detect_outliers(data, column)
    after_cleaning_report = {
        "Column": [column],
        "Detection Method": [detection_method],
        "Handling Method": [replacement],
        "Outlier Count": [outlier_count(outlier)],
        "Outlier Percentage": [outlier_percentage(outlier)],
        "Skewness": [skew(data[column])],
        "Distribution": [skew_measurment(data[column])]
    }
    return data,pd.DataFrame(after_cleaning_report)
