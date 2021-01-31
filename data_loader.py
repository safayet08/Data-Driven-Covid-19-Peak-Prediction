# -*- coding: utf-8 -*-
"""
Created on Wed May 27 22:19:32 2020

@author: Md Safayet Islam Anonno
"""

import pandas as pd

def extract_countries(sheets):
    sheets.remove('Outline')
    sheets.remove('demo')
    return sheets
    
def load_data(sheet_list, source_file):
    dataset = pd.DataFrame()
    for i in range(0, len(sheet_list)):
        new_data = source_file.parse(sheet_list[i])
        dataset = dataset.append(new_data)
    return dataset


if __name__ == '__main__':
    file_name = 'Peak Prediction _ Phase 2.0.xlsx'
    source_file = pd.ExcelFile(file_name)
    countries = extract_countries(source_file.sheet_names)
    
    dataset = load_data(countries, source_file)
    
    dataset['First Case(DD/MM/YYYY)'] = dataset['First Case(DD/MM/YYYY)'].dt.date
    dataset['Peak Date(DD/MM/YYYY)'] = dataset['Peak Date(DD/MM/YYYY)'].dt.date
    
    irrelevant = ['T - 2 Cases', 'T - 1 Cases', 'T = Peak Day Cases', 'T + 1 Cases', 'T + 2 Cases']
    dataset = dataset.drop(irrelevant, axis = 1)
    
    dataset = dataset.reset_index(drop = True) #Fixing the index after concatanation

    Type = pd.DataFrame(dataset.dtypes)
    
    output_file = 'train + csv data.xlsx'
    dataset.to_excel(output_file, index = False)

    print('Done')