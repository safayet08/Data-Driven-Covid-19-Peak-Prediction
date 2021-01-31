# -*- coding: utf-8 -*-
"""
Created on Wed May 27 22:45:34 2020

@author: Md Safayet Islam Anonno
"""
import pandas as pd
import numpy as np


def interval_stack(dataset, info):
    ordering = ['1st ', '2nd ', '3rd ', '4th ']
    pile = [np.empty(0) for i in range(4)]
    for i in range(4):
        pile[i] = dataset[ordering[i] + info].to_numpy() 

    return np.stack((pile[0], pile[1], pile[2], pile[3])).T

def drop_irrelevant_col(df, irrelevant):
    return df.drop(irrelevant, axis = 1)


if __name__ == '__main__':
    dataset = pd.read_excel('train + csv data.xlsx')
    dataset = dataset.drop(['First Case(DD/MM/YYYY)', 'Peak Date(DD/MM/YYYY)'], axis = 1)
    
    time = dataset['Days to Peak'].to_numpy()
    peak_case = dataset['Peak Case'].to_numpy()
    peak_cumulative = dataset['Peak Cumulative'].to_numpy()
    
    time_peak = time
    time = np.stack((time * 35/100, time * 55/100, time * 70/100 , time * 80/100)).T  #Time percentage
    
    peak_stacked = interval_stack(dataset, info = 'Interval Case/day')
    c_peak_stacked = interval_stack(dataset, info = 'Interval Cum Case/day')
   
    
    ## This function is inside fitting.py
  #  polynomial_fitting(dataset, time, c_peak_stacked, time_peak, peak_cumulative, cumulative_flag = True)
  #  polynomial_fitting(dataset, time, peak_stacked, time_peak, peak_case, peak_flag = True)
    
    print('Done')
    
  #  [X_train, Y_train_PeakCases,Y_train_CumulativePeakCases, Y_train_days2peak] = assemble_XY(train_set)
  #  [X_csv, Y_csv_PeakCases,Y_csv_CumulativePeakCases,Y_csv_days2peak] = assemble_XY(csv_set)
  #  [X_test, Y_test_PeakCases,Y_test_CumulativePeakCases, Y_test_days2peak] = assemble_XY(test_set)
    
  #  from sklearn.linear_model import LinearRegression as LR
  #  weights = [float(x) for x in range(X_train.shape[0])]
  #  model = LR().fit(X_train, Y_train_CumulativePeakCases, sample_weight = weights)
  #  prediction = model.predict(X_csv)
    
  #  print(prediction)
    
    

    
    
    

