#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: city_info.py

Group Members:
Mukunda Aithal    (maithal@andrew.cmu.edu)
Saumya Bansal	   (saumyab@andrew.cmu.edu)
Pranay Muppala   (pmuppala@andrew.cmu.edu)
Yashika Goyal       (ygoyal@andrew.cmu.edu)

Imported in main_program.py


"""
from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


#Load the html data
def loadHTML(html):
    bsyc = BeautifulSoup(html.read(), 'html.parser')
    tc_table_list = bsyc.findAll('table', { "class" : "sgmltable" })
    tc_table = tc_table_list[0]
    return tc_table

#Read the table contents
def readTable(tc_table):
    climate_data = []
    for c in tc_table.children:
        temp = []
        for r in c.children:
            r = str(r)
            if "</td>" in r:
                val = r.split('>')
                val = val[1]
                val = val.split('<')
                val = val[0]
                if len(val) <= 5 and val != 'trace':
                    val = float(val)
                elif val == 'trace':
                    val = float(0)
                else:
                    val = str(val)
                temp.append(val)
        climate_data.append(temp)
    climate_data = climate_data[3:]
    return climate_data

#store climate data in dataframe
def climate_df(climate_data, labels):
    climate_df = pd.DataFrame(climate_data, columns = labels)
    climate_df = climate_df.drop(columns = ['# Yrs Obs'])
    climate_df[['City', 'State']] = climate_df['City'].str.split(',', 1, expand=True)
    climate_df = climate_df.drop(columns = ['State'])
    climate_df.loc[59, 'City'] = 'Minneapolis'
    climate_df.loc[87, 'City'] = 'Seattle'
    climate_df.loc[28, 'City'] = 'Dallas'
    return climate_df

#store population data in dataframe
def population_df():
    pop_df = pd.read_csv(r"Population_UnitedStates-Citywise_2019.csv")
    pop_df = pop_df.sort_values(by = ['Geographic Area'])
    pop_df['Population'] = pop_df['Population'].str.replace(',','')
    pop_df['Population'] = pd.to_numeric(pop_df['Population'], downcast="float")
    pop_df = pop_df.drop([0])
    pop_df[['City', 'State']] = pop_df['Geographic Area'].str.split(',', 1, expand=True)
    pop_df['City'] = pop_df['City'].str.replace(r' city| town| municipality', '')
    pop_df = pop_df.drop(columns = ['Geographic Area', 'State'])
    pop_df = pop_df.sort_values(by = ['City'])
    pop_df.loc[4722, 'City'] = 'Indianapolis'
    pop_df.loc[2996, 'City'] = 'Honolulu'
    pop_df.loc[3013, 'City'] = 'Boise'
    return pop_df

#merging the data
def merge_city_pop(clim_df, pop_df):
    merged_left = pd.merge(left=clim_df, right=pop_df, how='left', left_on='City', right_on='City')
    merged_left = merged_left.sort_values(by = ['City','Population'], ascending = True)
    merged_left = merged_left.drop_duplicates(subset = 'City', keep = "last")
    merged_left['City_Name'] = merged_left['City']
    city_df = merged_left.set_index('City', verify_integrity = True)
    city_df.drop(['Mt. Washington'])
    return city_df

#Printing the city stats
def print_city_stats(city_row):
    print('\n*********** City Statistics ***********')
    print(city_row['City_Name'].values[0],'Average Winter Temperature (F): ',city_row['Jan'].values[0])
    print('Average Spring Temperature (F):', city_row['Apr'].values[0])
    print('Average Summer Temperature (F):', city_row['Jul'].values[0])
    print('Average Fall Temperature (F):', city_row['Oct'].values[0])
    print('Average Annual Rain (in.):', city_row['Precip_in'].values[0])
    print('Average Annual Rainy Days:', city_row['Precip_days'].values[0])
    print('Average Annual Snowfall (in.):', city_row['Snowfall_in'].values[0])
    print('Population (2019):', city_row['Population'].values[0])

#Generating a 3D surface chart
def chart_3D(population_df):
    import numpy as np    
    import matplotlib.pyplot as plt
    from matplotlib import cm
    
    #fig = plt.figure()
    fig = plt.figure(figsize =(10,10))
    city_names = population_df['City_Name'].values
    temp1 = population_df['Jan'].values
    temp2 = population_df['Apr'].values
    temp3 = population_df['Jul'].values
    temp4 = population_df['Oct'].values
    
    X = np.arange(0,len(population_df['City_Name'].values))
    #print(X)
    X = np.array([X])
    Y = np.array([[1, 2 , 3, 4]]).reshape(4,1)
    Z = np.array([temp1, temp2, temp3, temp4])
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    
    ax.set_xlim([0, 9])
    ax.set_ylim([0, 3])
    
    ax.set_xticks(range(len(X.T)))
    ax.set_yticks([1, 2, 3, 4])
    ax.set_xticklabels(city_names)
    ax.set_yticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    
    ax.tick_params(axis='x', which='major', labelrotation=-1000)
    
    surf = ax.plot_surface(X, Y, Z, cmap = cm.coolwarm)
    fig.colorbar(surf, ax=ax, shrink=0.4, aspect=5)
    ax.set_title('Temperatures of 10 Most Populous Cities')
    ax.set_xlabel('Cities')
    ax.xaxis.labelpad = 40
    
    ax.set_ylabel('Quarter')
    ax.set_zlabel('Temperature (F)')        
    
    plt.show()
    