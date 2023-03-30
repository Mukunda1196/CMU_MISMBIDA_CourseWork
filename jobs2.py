# -*- coding: utf-8 -*-
"""
Name: jobs2.py

Group Members:
Mukunda Aithal    (maithal@andrew.cmu.edu)
Saumya Bansal       (saumyab@andrew.cmu.edu)
Pranay Muppala   (pmuppala@andrew.cmu.edu)
Yashika Goyal       (ygoyal@andrew.cmu.edu)

Imported in main_program.py
"""

import requests
from bs4 import BeautifulSoup  
import pandas as pd
import csv
  

# Raw HTML data regarding Job Search in United States has been scraped from 'https://www.indeed.com/' containing below information:
# Job Role
# Company Name
# Job Location
# Job Requirements
# Estimated Salary

def scrape_jobs_data(num):

    result = []
    i = 0
    while i < num: 
        # API is called in order to scrape HTML data for all the jobs
        URL = "https://www.indeed.com/jobs?q=software&l=United+States&start=" + str(i) + "&sort=date"
        r = requests.get(URL)
          
        soup = BeautifulSoup(r.content, 'html5lib')
        
        quotes=[]
        job_titles = []
        company_name = []
        search = ''
        allSliderItems = []
           
        table = soup.find('table', attrs = {'id':'resultsBody'})
        #   Find all the tables containing data for each job opening
        for row in table.findAll('div', attrs={'class': 'slider_item'}):
            obj = {}
            allSliderItems.append(row)
            topTable = row.find('table', attrs={'class': 'jobCard_mainContent'})
            h2 = topTable.find('h2', attrs={'class': 'jobTitle'})
            span = h2.findAll('span')
            # print(span[len(span)-1])
            JOBTITLE = span[len(span) - 1].text
            # print(JOBTITLE)
        
            companyLocationDiv = topTable.find('div', attrs={'class': 'company_location'})
            companyName = companyLocationDiv.find('span', attrs={'class': 'companyName'})
            
            COMPANYNAME = ''
            
            try:
                if len(companyName.findAll('a')) == 0:
                    COMPANYNAME = companyName.text
                else:
                    COMPANYNAME = companyName.find('a').text
            except Exception as e:
                COMPANYNAME=''
            
            companyLocation = companyLocationDiv.find('div', attrs={'class': 'companyLocation'})
            COMPANYLOCATION = companyLocation.text
            location1 = []
            location2 = []
            location3 = []
            CITY = ''
            if (COMPANYLOCATION.find("+")) != -1:
                location1 = COMPANYLOCATION.split("+")
                if (location1[0] == ""):
                    COMPANYLOCATION = "Remote"
                else:
                    COMPANYLOCATION = location1[0]
            
            if (COMPANYLOCATION.find("•")) != -1:
                location2 = COMPANYLOCATION.split("•")
                COMPANYLOCATION = location2[0]
                
            if (COMPANYLOCATION.find(",")) != -1:
                location3 = COMPANYLOCATION.split(",")
                CITY = location3[0]
                COMPANYLOCATION = location3[1]
                
            if(CITY == ""):
                CITY = 'Remote'
        
            try:
                
                salaryData = topTable.find('div', attrs={'class': 'metadata salary-snippet-container'})
                salaryAttribute = salaryData.find('div', attrs={'class': 'attribute_snippet'})
                SALARY = salaryAttribute.text
            except:
                #print("Salary not present for " + COMPANYNAME + ", " + JOBTITLE)
                #print("\n")
                SALARY = ""
            
            bottomTable = row.find('table', attrs={'class': 'jobCardShelfContainer'})
            tableRow = bottomTable.find('tr', attrs={'class': 'underShelfFooter'})
            jobSnippet = tableRow.find('div', attrs={'class': 'job-snippet'})
            allSnippets = jobSnippet.findAll('li')
            ALLJOBSNIPPETS = ''
            for snippet in allSnippets:
                ALLJOBSNIPPETS = ALLJOBSNIPPETS + snippet.text
        # Store all the fetched data as a dictionary object for each job opening
            obj['company_name'] = COMPANYNAME
            obj['job_title'] = JOBTITLE
            obj['city'] = CITY
            obj['company_location'] = COMPANYLOCATION
            obj['salary'] = SALARY
            obj['snippet'] = ALLJOBSNIPPETS
        
            result.append(obj)
        i = i + 20
        
            
    res = pd.DataFrame(result)
    res.to_csv('final_jobs.csv',index=False)
        
        

