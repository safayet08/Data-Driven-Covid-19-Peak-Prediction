# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:34:47 2020

@author: Md Safayet Islam Anonno
"""

import pandas as pd
    
def load_data(sheet_list, source_file):
    dataset = pd.DataFrame()
    for i in range(0, len(sheet_list)):
        new_data = source_file.parse(sheet_list[i])
        dataset = dataset.append(new_data)
    return dataset


if __name__ == '__main__':
    file_name = 'Test Set.xlsx'
    source_file = pd.ExcelFile(file_name)
    countries = source_file.sheet_names
    
    test_data = load_data(countries, source_file)
    
    test_data['First Case'] = test_data['First Case'].dt.date
    test_data = test_data.reset_index(drop = True) #Fixing the index after concatanation

    output_file = 'loaded test data.xlsx'
    test_data.to_excel(output_file, index = False)

    print('Done')