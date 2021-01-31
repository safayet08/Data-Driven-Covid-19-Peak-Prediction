# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:51:08 2020

@author: Md Safayet Islam Anonno
"""

import numpy as np
import matplotlib.pyplot as plt

def polynomial_fitting(dataset, time, peak_stacked, time_peak, peak_data,
                       peak_flag = False, cumulative_flag = False):
    from scipy.optimize import curve_fit
    idx = 0
    
    for idx in range(len(dataset)):
        xData = time[idx]   #Load time data
        yData = peak_stacked[idx] #Load case data
    
        x, y = xData, yData
          
        def test(x, a, b, c): 
            return a *(x**2) + b*x + c
          
        param= curve_fit(test, x, y)[0]
    
       # print('Fitted parameters:', param)
        
        x_domain = np.linspace(time[idx][0], time_peak[idx])
        modelPredictions = test(x_domain, *param) 
        
        plt.ioff() # Turn interactive plotting off]
        fig = plt.figure()
        
        plt.title(dataset['Entry'][idx])
        plt.plot(xData, yData, 'o', color ='red', label ="data points") 
        plt.plot(x_domain, modelPredictions, color = 'Green', label = 'Polynomial model Degree 2')
        plt.plot(x_domain[-1], modelPredictions[-1], 'o', color ='blue', label = "Model Peak")
        plt.plot(time_peak[idx], peak_data[idx], 'x', color = 'black', label = 'Actual Peak')
        plt.legend(loc = 'best')
        plt.grid()
        
        if peak_flag == True:
            location = 'Result for Poly Reg Order 2/Peak Cases/'
        elif cumulative_flag == True:
            location = 'Result for Poly Reg Order 2/Cumulative Cases/'
        
        plt.savefig(location + dataset['Entry'][idx] + '.png')
        plt.close(fig)