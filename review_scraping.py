# -*- coding: utf-8 -*-
"""
Name: review_scraping.py

Group Members:
Mukunda Aithal    (maithal@andrew.cmu.edu)
Saumya Bansal	   (saumyab@andrew.cmu.edu)
Pranay Muppala   (pmuppala@andrew.cmu.edu)
Yashika Goyal       (ygoyal@andrew.cmu.edu)

Not imported in main_program.py, manually run and stored due to complications mentioned in ReadMe
"""

import os
import time

import numpy as np
import pandas as pd
import math
import re

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

#Creating Lists to store objects
Summary=[]
Date_n_JobTitle=[]
Date=[]
JobTitle=[]
AuthorLocation=[]
OverallRating=[]
Pros=[]
Cons=[]  

##Get the data from the page
def review_scraper(url):
  
    req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})  
    soup = BeautifulSoup(urlopen(req), "html.parser") 

    for x in soup.find_all('h2', {'class':'mb-xxsm mt-0 css-93svrw el6ke055'}):
        Summary.append(x.text)

    for x in soup.find_all('span', {'class':'authorJobTitle middle common__EiReviewDetailsStyle__newGrey'}): 
        Date_n_JobTitle.append(x.text)

  
    for x in Date_n_JobTitle:
        Date.append(x.split(' -')[0])
  
    for x in Date_n_JobTitle:    
        JobTitle.append(x.split(' -')[1].split(" in")[0].strip())
  
    for x in soup.find_all('span', {'class':'authorLocation'}):
        AuthorLocation.append(x.text)

    for x in soup.find_all('span', {'class':'ratingNumber mr-xsm'}):
        OverallRating.append(float(x.text))
  
    for x in soup.find_all('span', {'data-test':'pros'}):
        Pros.append(x.text)

    for x in soup.find_all('span', {'data-test':'cons'}):
        Cons.append(x.text)

    Reviews = pd.DataFrame(list(zip(Summary, Date, JobTitle, AuthorLocation, OverallRating, Pros, Cons)), 
                    columns = ['Summary', 'Date', 'JobTitle', 'AuthorLocation', 'OverallRating', 'Pros', 'Cons'])
  
    return Reviews

##change url to the company you review
input_url = "https://www.glassdoor.com/Reviews/Varsity-Tutors-Reviews-E431872.htm"

##Sorting it and having the review List
url_mod = input_url.split(".htm")[0]+"_P"+str(1) + ".htm?filter.iso3Language=eng&sort.sortType=RD&sort.ascending=false"

#scraping the first page content to get max pages and review counts
req = Request(url_mod,headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urlopen(req), "html.parser") 
countReviews = soup.find('div', {'data-test':'pagination-footer-text'}).text
countReviews = float(countReviews.split(' Reviews')[0].split('of ')[1].replace(',',''))

countPages = math.ceil(countReviews/10)

if countPages > 50:
    maxPage = 51
else:    
    maxPage = countPages + 1

#scraping multiple pages of company glassdoor review
output = pd.DataFrame()
for x in range(1,maxPage):
  url = input_url.split(".htm")[0]+"_P"+str(x) + ".htm?filter.iso3Language=eng&sort.sortType=RD&sort.ascending=false"
  output = output.append(review_scraper(url), ignore_index=True)

#display the output
display(output)
output['Company_Name'] = input_url.split("Reviews/")[1].split('-Reviews')[0]
output.to_csv(re.split("E\d",input_url.split("Reviews/")[1])[0]+'output.csv', index=False)


#List of input URL's
input_url =[]
input_url.append("https://www.glassdoor.com/Reviews/Bowman-Williams-Reviews-E1081064.htm")
input_url.append("https://www.glassdoor.com/Reviews/Deloitte-Reviews-E2763.htm"          )
input_url.append("https://www.glassdoor.com/Reviews/J-P-Morgan-Reviews-E145.htm"         )
input_url.append("https://www.glassdoor.com/Reviews/Northrop-Grumman-Reviews-E488.htm"   )
input_url.append("https://www.glassdoor.com/Reviews/Insight-Global-Reviews-E152783.htm"  )
input_url.append("https://www.glassdoor.com/Reviews/Apple-Reviews-E1138.htm"             )
input_url.append("https://www.glassdoor.com/Reviews/TuSimple-Reviews-E1147857.htm"       )
input_url.append("https://www.glassdoor.com/Reviews/Brooksource-Reviews-E227518.htm"     )
input_url.append("https://www.glassdoor.com/Reviews/Esri-Reviews-E4043.htm"              )
input_url.append("https://www.glassdoor.com/Reviews/C3-AI-Reviews-E312703.htm"           )
input_url.append("https://www.glassdoor.com/Reviews/Indeed-Reviews-E100561.htm"          )
input_url.append("https://www.glassdoor.com/Reviews/Comcentric-Reviews-E719287.htm"      )
#input_url.append("https://www.glassdoor.com/Reviews/CI-Reviews-E241911.htm"              )
input_url.append("https://www.glassdoor.com/Reviews/Varsity-Tutors-Reviews-E431872.htm"  )
input_url.append("https://www.glassdoor.com/Reviews/TikTok-Reviews-E2230881.htm"         )

outputList = []

for input_url in input_url:
    outputList.append(re.split("E\d",input_url.split("Reviews/")[1])[0]+'output.csv')
    
data=pd.DataFrame()

###Concatenate all the outputs
for i in outputList:
    data = data.append(pd.read_csv(i),ignore_index=True)
data.to_csv('final.csv',index=False)
















