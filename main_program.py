# -*- coding: utf-8 -*-
"""
Name: main_program.py

Group Members:
Mukunda Aithal    (maithal@andrew.cmu.edu)
Saumya Bansal	   (saumyab@andrew.cmu.edu)
Pranay Muppala   (pmuppala@andrew.cmu.edu)
Yashika Goyal       (ygoyal@andrew.cmu.edu)

Imports jobs2.py, city_info.py files
"""

import os
import pandas as pd
import re
from matplotlib import pyplot as plt
import numpy as np
from urllib.request import urlopen
import city_info
import jobs2

#os.chdir("C:\\Users\\prana\\Documents\\DFP")
#data = pd.read_csv("IBM-Reviews-output.csv" )
#data_numpy = data.to_numpy()
#print(data)
#print(data_numpy)
#table = tabulate(data,headers = 'keys')
#print(table)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#from jobs2 import scrape_jobs_data

data = pd.read_csv("final.csv", encoding = 'utf-8')
jobs_data = pd.read_csv("final_jobs2.csv",encoding = 'utf-8')
jobs_data = jobs_data.drop_duplicates()

jobs_filter = pd.DataFrame()
company_names = data['Company_Name'].unique()
for i in company_names:
    r=re.compile(i.lower())
    temp =jobs_data[jobs_data['company_name'].apply(lambda x: bool(r.match(x.lower())))]    
    jobs_filter =jobs_filter.append(temp,ignore_index=True)
    
### Gets the data about the company and city statistics
def chosen_job(user_choice):
    job_selected = jobs_filter.iloc[int(user_choice),:]
    data_filter = data[data['Company_Name']==job_selected['company_name']].reset_index()
    avg = round(data_filter['OverallRating'].mean(),2)
    review_count = len(data_filter)
    pos_review_count = len(data_filter[data_filter['OverallRating']>=3])
    neg_review_count = len(data_filter[data_filter['OverallRating']<3])
    med = data_filter['OverallRating'].median()
    print('\n-----------------------Company Details------------------------')
    print('Here are some statistics about the company ' +job_selected['company_name'] +'\n')
    print("There are a total of " + str(review_count) + " reviews available \n")
    print("The average rating out of 5 is " + str(avg) + " and the median is " + str(med) +'\n')
    print("The number of positive reviews(>=3) are " + str(pos_review_count) +'\n')
    print("Here are the top 10 recent review summaries")
    #recent_summary = 
    print(data_filter['Summary'].head(10).to_string(header=True))
        
    # Creating dataset 
    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    plt.pie([pos_review_count/review_count, neg_review_count/review_count], labels = ["Positive Reviews","Negative Reviews"],autopct='%.1f%%')
    plt.title("Review Distribution for " + job_selected['company_name'])
    # show plot
    plt.show()
    
    location_reviews = data_filter.loc[:,('AuthorLocation','OverallRating')]
    location_reviews = location_reviews.groupby(['AuthorLocation']).mean()
    location_reviews = location_reviews.reset_index()
    
    top_location_reviews = location_reviews.sort_values(by='OverallRating',ignore_index=True,ascending = False).loc[:12,]
    top_location_reviews.plot(x ='AuthorLocation', y='OverallRating', kind = 'bar')
    
    plt.xlabel('Location')
    plt.ylabel('Overall Rating')
    plt.title(' Company locations with highest average rating')
    plt.show()
    
    low_location_reviews = location_reviews.sort_values(by='OverallRating',ignore_index=True,ascending = True).loc[:12,]
    low_location_reviews.plot(x ='AuthorLocation', y='OverallRating', kind = 'bar')
    
    plt.xlabel('Location')
    plt.ylabel('Overall Rating')
    plt.title('Company locations with lowest average rating')
    plt.show()
    
    inp = input('Do you want to know more about the city in which the job is located?\nEnter yes or no\n')
    if inp=="yes":
        
        #Scrape html from url for climate data and find table html data
        html = urlopen('https://www.infoplease.com/math-science/weather/climate-of-100-selected-us-cities')
        tc_table = city_info.loadHTML(html)
        #Read table html data into a list
        climate_data = city_info.readTable(tc_table)
        #Create labels and create climate DF
        labels = ['City', 'Jan', 'Apr', 'Jul', 'Oct', 
                'Precip_in', 'Precip_days', 'Snowfall_in', '# Yrs Obs']
        clim_df = city_info.climate_df(climate_data, labels)
        #Create population DF from csv file
        pop_df = city_info.population_df()
        #Merge climate and population DFs into one DF
        city_df = city_info.merge_city_pop(clim_df, pop_df)    
        
        ###City Statistics and Plots
        if job_selected['city'] in city_df.index:
            city = city_df.loc[city_df['City_Name'].str.contains(job_selected['city'])]['City_Name'].values[0]    
            city_row = city_df.loc[city_df['City_Name'].str.contains(job_selected['city'])]
            city_info.print_city_stats(city_row)
            charts_inp = input('Would you like to see how your city statistics compares to other cities? Please enter yes or no\n')
            if charts_inp == "yes":
                coldest_df = city_df.loc[((city_df.Jan + city_df.Apr + city_df.Jul + city_df.Oct) / 4).sort_values(ascending = True).index]
                coldest_df = coldest_df.reset_index()
                #print(coldest_df)
                cold_rank = coldest_df.loc[coldest_df['City'] == city].index.values[0]
                print(f'According to our information, {city} has the rank {cold_rank+1} in terms of coldest cities in the US.\n')
                
                city_df[['Precip_in']]= city_df[['Precip_in']].apply(pd.to_numeric)
                precip_df = city_df.loc[city_df.Precip_in.sort_values(ascending = False).index]
                precip_df = precip_df.reset_index()
                precip_rank = precip_df.loc[precip_df['City'] == city].index.values[0]
                print(f'According to our information, {city} has the rank {precip_rank+1} in terms of precipitation in the US.\n')
                
                snowfall_df = city_df.loc[city_df.Snowfall_in.sort_values(ascending = False).index]
                snowfall_df = snowfall_df.reset_index()
                snowfall_rank = snowfall_df.loc[snowfall_df['City'] == city].index.values[0]
                print(f'According to our information, {city} has the rank {snowfall_rank+1} in terms of snowfall in the US.\n')
                
                population_df = city_df.loc[city_df.Population.sort_values(ascending = False).index]
                population_df = population_df.reset_index()
                population_rank = population_df.loc[population_df['City'] == city].index.values[0]
                print(f'According to our information, {city} has the rank {population_rank+1} in terms of population in the US.\n')
                        
                cold_plot = coldest_df.head(10).plot(x = 'City', y = ['Jan', 'Apr', 'Jul', 'Oct'], kind = "bar", title = '10 Coldest Cities Temps (F)')
                cold_plot.set_xlabel('Cities')
                cold_plot.set_ylabel('Avg Temp (F)')
                plt.show()
                
                cold_plot_precip = precip_df.head(10).plot(x = 'City', y = 'Precip_in', kind = "bar", title = '10 Coldest Cities Precipitation (in.)')
                cold_plot_precip.set_xlabel('Cities')
                cold_plot_precip.set_ylabel('Avg Precipitation')
                plt.show()
                
                cold_plot_snow = snowfall_df.head(10).plot(x = 'City', y = 'Snowfall_in', kind = "bar", title = '10 Coldest Cities Snowfall (in.)')
                cold_plot_snow.set_xlabel('Cities')
                cold_plot_snow.set_ylabel('Avg Snowfall (in)')
                plt.show()
                        
                plot_population = population_df.head(10).plot(x = 'City', y = 'Population', kind = "bar", title = '10 Most Populous Cities')
                plot_population.set_xlabel('Cities')
                plot_population.set_ylabel('Population as in 2019')
                plt.show()
                
                city_info.chart_3D(population_df.head(10))
                
            else:
                pass
        else:
            print('This city is currently not included in our database.')
    else:
        pass    
     

###Function to loop through all the jobs based on the jobs available and user input
###Contains a lot of try except and while loops to ensure proper user input
def job_listings():
    user_input = True
    while user_input:    
        print('''Please enter which type of role you are interested in eg.(Developer, Analyst etc)''')    
        answer = input('Your choice: ').strip()
        user_jobs = pd.DataFrame()
        r=re.compile(answer.lower())
        temp =jobs_filter[jobs_filter['job_title'].apply(lambda x: bool(r.search(x.lower())))]    
        user_jobs = user_jobs.append(temp)
        
        if len(user_jobs)>0:
            print("\nThere are " + str(len(user_jobs)) +" listings with " +str(answer)+ " in title\n" )
            if len(user_jobs)>10:
                print("Here are the most recent 10 roles\n")
                user_jobs.columns = ['Company Name','Job Title','City','Location','Salary','Summary']
                print(tabulate(user_jobs.loc[:10,]))
                row_num_bad = True
                while row_num_bad:
                    try:                    
                        user_choice = input('Please enter the row number for the job you are interested in\n')                        
                        chosen_job(user_choice)
                        row_num_bad = False                        
                    except:
                        print("Please enter a number")                    
                job_bad = True
                while job_bad:                    
                    continue_job_search = input('Do you want to look at other jobs?Enter yes or no\n')
                    if continue_job_search not in ("yes", "no"):
                        print('Please enter yes or no\n')
                    elif continue_job_search =="no":                             
                        user_input = False
                        job_bad = False
                    else:
                        break
                                        
            else:
                user_jobs.columns = ['Company Name','Job Title','City','Location','Salary','Summary']
                print(user_jobs)
                row_num_bad = True
                while row_num_bad:
                    try:
                        user_choice = input('Please enter the row number for the job you are interested in\n')
                        chosen_job(user_choice)
                        row_num_bad = False
                    except:
                        print('Please enter a number')
                job_bad = True
                while job_bad:                    
                    continue_job_search = input('Do you want to look at other jobs?Enter yes or no\n')
                    if continue_job_search not in ("yes", "no"):
                        print('Please enter yes or no\n')
                    elif continue_job_search =="no":                             
                        user_input = False
                        job_bad = False
                    else:
                        break
                                            
                    
        else:
            print('Sorry, there are no roles for ' + str(answer)+ "right now")
            job_bad = True
            while job_bad:                    
                inp = input('Do you want to choose another role? If yes, please enter yes or choose no to proceed to check the existing listings\n')
                if inp not in ("yes","no"):
                    print('Please enter yes or no\n')                
                elif inp == "no":            
                    job_bad = False
                    jobs_count = len(jobs_filter)                
                    print("Here are 10 listings")                
                    print(jobs_filter.loc[:9,])
                    more_listings = input('Please choose the job you are interested in or enter "more" to see additional listings\n ')
                    if more_listings != "more": 
                        more_bad= True
                        while more_bad:
                            try:
                                num_input = input("Please finalize the row number\n ")
                                chosen_job(num_input)                
                                more_bad = False                                
                            except:                                
                                pass                        
                        continue_job_search = input('Do you want to look at other jobs? Enter yes or no\n')
                                #check_job_bad()
                        if continue_job_search =="no":                                                                                                
                            user_input = False
                                  
                    elif more_listings == 'more':
                        loop_count = jobs_count -10
                        i=10
                        cancel="no"
                        while loop_count>10:                        
                            j=i+9
                            print(jobs_filter.loc[i:j,])
                            i=j
                            user_choice = input("Please choose a job from these 10 listings or enter 'more' to get additional listings \n")
                            if user_choice != "more": 
                                more_bad= True
                                while more_bad:
                                    try:
                                        num_input = input("Please finalize the row number \n")
                                        chosen_job(num_input)                
                                        more_bad = False                                
                                    except:                                
                                        pass
                                continue_job_search = input('Do you want to look at other jobs? Enter yes or no\n')
                                #check_job_bad()
                                if continue_job_search =="no":                                                                                                
                                    cancel = "yes"
                                    break      
                            loop_count = loop_count -10
                            #print(i)
                            #print(j)
                        if cancel=="yes":
                            user_input = False
                        else:
                            print(jobs_filter.loc[i:,])
                            row_num_bad = True
                            while row_num_bad:
                                try:
                                    user_choice = input("Please choose a job from these final listings\n")
                                    chosen_job(user_choice)
                                    row_num_bad = False
                                except:
                                    print('Please enter a number')                                                        
                            continue_job_search = input('Do you want to look at other jobs? Enter yes or no\n')
                            if continue_job_search =="no":
                                user_input = False
                    else:
                        print('Invalid input')
                elif inp == "yes":
                    break

###Start of the program and getting user input
answer_bad = True
print( '------------------------ Welcome to Jobnest!------------------------------- \n') 
print('We currently have ' +str(len(jobs_filter))+' software jobs available.\n')
while answer_bad:
    print('If you want additional amount of data,please enter "yes" or "no" but be aware that it might take up to 10 minutes to scrape jobs for around 500 listings and increases linearly with listings. The listings will be later filtered for software jobs')
    answer = input('Your choice: \n').strip()
    if answer=="yes":
        answer_bad = False
        num_bad = True
        while num_bad:
            try:
                num_str = input('''Please enter number of listings you want to scrape \n''').strip()
                num =int(num_str)
                num_bad=False
            except:
                print('Please enter a number \n')
        jobs2.scrape_jobs_data(num)
        new_jobs_data = pd.read_csv("final_jobs.csv")
        new_jobs_data = new_jobs_data.drop_duplicates()
            
        for i in company_names:
            r=re.compile(i.lower())
            temp =new_jobs_data[new_jobs_data['company_name'].apply(lambda x: bool(r.match(x.lower())))]    
            jobs_filter =jobs_filter.append(temp,ignore_index=True)
        print('We now have ' + str(len(jobs_filter)) + ' available \n')
        job_listings()
        num_bad = False
    elif answer=="no":
        answer_bad = False
        job_listings()
        num_bad = False
    else:
        print('Your choice is not valid:', answer,'Please enter yes or no \n')
    
                    
                
                