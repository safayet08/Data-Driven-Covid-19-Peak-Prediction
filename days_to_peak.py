# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:54:32 2020

@author: Md Safayet Islam Anonno
"""

import pandas as pd
import numpy as np

def split_data(dataset):
    
    # 0 -> USA -> Golden
    #14 -> ind bare
    #15 -> does nothing
    #16 -> ind bare
    
    
    #17 --> BD->bare, IND->kome (hugely) -----> (Always)
    # 19 -> BD kome, ind bare
    
    train_idx = [0,2,3,4,6,7,8,9,10,11,14,15,16,17,18,19]
    test_idx = [20,21,22,23,24,25,26,27,28,29,30,31,32,33]
    csv_idx = [1,5,12,13] #Has to keep at least 1 in the list, (Random, won't matter, will train with everything)

         
    x_train = dataset.iloc[train_idx, :-1]
    x_csv = dataset.iloc[csv_idx, :-1]
    x_test = dataset.iloc[test_idx, :-1]

    last = dataset.shape[1]

    y_train = dataset.iloc[train_idx, last - 1:last]
    y_csv = dataset.iloc[csv_idx, last - 1:last]
    
    return [x_train, x_csv, x_test, y_train, y_csv]


def move_to_df(Type, model, x):
    prediction = model.predict(x)
    name = 'Result(' + Type + ')'
    dataset[name] = np.nan
    pos = list(x.index)
    for i in range(len(pos)):
        dataset[name][pos[i]] = prediction[i]
    return dataset
    
def feature_engineering(dataset):
    #New so doesn't need renaming column
#    dataset['HCI * HCI'] = dataset['HCI'] * dataset['HCI'] 
    
    #New so doesn't need renaming column
    dataset['log(Area * Pop)'] = np.log(dataset['Population(M)'] * dataset['Area(KM^2)'])
    dataset['log(Pop Density ^ 2)'] = np.log(dataset['Pop Density'] * dataset['Pop Density'])
  #  dataset['log(HCI * Pop)'] =  np.log(dataset['Population(M)'] * dataset['HCI'])
    
    
   # dataset['Population(M)'] = np.log(dataset['Population(M)'])
   # dataset = dataset.rename(columns = {"Population(M)": "log(Population)"}) 
    
    dataset['log(Area(KM^2))'] = np.log(dataset['Area(KM^2)']) 
    dataset = dataset.drop(['Area(KM^2)'], axis = 1)
    
    return dataset
    


if __name__ == '__main__':
    
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    dataset = pd.read_excel('train(with days to peaks) + test(without days to peak).xlsx')
    
    dataset = feature_engineering(dataset)
    
    # dataset will be kept intact, we will work on the workset
    workset = dataset
    
    Y = workset['Days to Peak']
    Entry = workset['Entry']
    workset = workset.drop(['Days to Peak', 'Entry', 'First Case'], axis = 1)
    
    from sklearn.preprocessing import MinMaxScaler

    cols = ['Population(M)','Pop Density','HCI','log(Area * Pop)',
            'log(Pop Density ^ 2)','log(Area(KM^2))']
    
  #  workset[cols] = MinMaxScaler().fit_transform(workset[cols])
    
    workset['Days to Peak'] = Y
    
    [x_train, x_csv, x_test, y_train, y_csv] = split_data(workset)
    
    from sklearn.linear_model import LinearRegression
    model = LinearRegression().fit(x_train, y_train)
    
    coef = model.coef_[0]
    
    dataset = move_to_df('CSV', model, x_csv)
    dataset = move_to_df('Train', model, x_train)
    dataset = move_to_df('Test', model, x_test)
    
    dataset['First Case'] = dataset['First Case'].dt.date
    
    prediction_column = 'Days to Peak (Model Result)'
    dataset[prediction_column] = ''
    for i in range(len(dataset)):
        import math
        if math.isnan(dataset['Result(Train)'][i]) == False:
            dataset[prediction_column][i] = dataset['Result(Train)'][i]
        elif math.isnan(dataset['Result(CSV)'][i]) == False:
            dataset[prediction_column][i] = dataset['Result(CSV)'][i]
        elif math.isnan(dataset['Result(Test)'][i]) == False:
            dataset[prediction_column][i] = dataset['Result(Test)'][i]
    
    from datetime import timedelta   
    dataset['Peak Date'] = ''
    for i in range(len(dataset)):
        dataset['Peak Date'][i] = dataset['First Case'][i] + timedelta(days = dataset[prediction_column][i])
    
    workset['Entry'] = dataset['Entry']
    workset['Peak Date'] = dataset['Peak Date']
    workset['Days to Peak (Model Result)'] = dataset['Days to Peak (Model Result)'] 
    
    output_file = 'days_to_peak(prediction).xlsx'
    dataset.to_excel(output_file, index = False)
    
    workset['Acceptable[Threshold = 10 days]'] = ''
    threshold = 10
    acceptable = 0
    unacceptable = 0
    for i in range(len(workset)):
        if math.isnan(workset['Days to Peak'][i]) == False and math.isnan(workset['Days to Peak (Model Result)'][i]) == False:
            if abs(workset['Days to Peak'][i] - workset['Days to Peak (Model Result)'][i]) <= threshold:
                workset['Acceptable[Threshold = 10 days]'][i] = "YES"
                acceptable = acceptable + 1
            else:
                workset['Acceptable[Threshold = 10 days]'][i] = "NO"
                unacceptable = unacceptable + 1
    
    workset['Diff'] = abs(workset['Days to Peak'] - workset['Days to Peak (Model Result)'])
    
  #  workset = workset.set_index('Entry', drop = True)
                
    w_ind = workset['Peak Date'][20]
    w_bd = workset['Peak Date'][21]

    print('Done')
    
    
    