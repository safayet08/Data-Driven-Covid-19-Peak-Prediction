# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:06:50 2020

@author: Md Safayet Islam Anonno
"""

import pandas as pd

def generate_irrelevant_ordinal(base):
    order = ['1st ', '2nd ', '3rd ', '4th ']
    irrelevant = []
    for i in range(len(order)):
        irrelevant.append(order[i] + base)
    return irrelevant

def generate_irrelevant_numeric(base):
    irrelevant = []
    for i in range(1, 10):
        irrelevant.append(base + str(i))
    return irrelevant

def load_data(sheet_list, source_file):
    dataset = pd.DataFrame()
    for i in range(0, len(sheet_list)):
        new_data = source_file.parse(sheet_list[i])
        dataset = dataset.append(new_data)
    return dataset

if __name__ == '__main__':
    test_csv_file = pd.ExcelFile('train + csv data.xlsx')
    train_file = pd.ExcelFile('Test Set.xlsx')
    
    test_csv_data = load_data(test_csv_file.sheet_names, test_csv_file)
    train_data = load_data(train_file.sheet_names, train_file)
    
    test_csv_data = test_csv_data.rename(columns = {'First Case(DD/MM/YYYY)' : 'First Case'}) 
    
    required = ['Entry','Population(M)','Area(KM^2)','Pop Density','HCI', 'Days to Peak', 'First Case']
    
    combined = test_csv_data.loc[:, required]
    combined = combined.append( train_data.loc[:, required] )
    
    combined = combined.reset_index(drop = True) #Fixing the index after concatanation
    
    output_file = 'train(with days to peaks) + test(without days to peak).xlsx'
    combined.to_excel(output_file, index = False)

    print('Done')