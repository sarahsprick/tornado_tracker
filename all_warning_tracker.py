#!/usr/bin/env python
# coding: utf-8

# In[1]:


# install packages

import requests
import pandas as pd
import numpy as np
from pandas import json_normalize
import datetime
import os
import warnings
warnings.filterwarnings("ignore")


# In[2]:


# [SVR] severe thunderstorms seperate due to data quantity

# request api

response = requests.get("https://api.weather.gov/products/types/SVR")
data = response.json()


# In[3]:


# normalize data

norm_data = json_normalize(data)
norm_data = json_normalize(norm_data['@graph']).T.set_axis(['series'], axis=1)#, inplace=False)
norm_data = norm_data['series'].apply(pd.Series)


# In[4]:


# get additional information about event

def get_id_info(id):
    response = requests.get(id)
    norm_data2 = response.json()
    id2 = norm_data2['@id']
    wmoCollectiveId = norm_data2['wmoCollectiveId']
    issuingOffice = norm_data2['issuingOffice']
    issuanceTime = norm_data2['issuanceTime']
    productCode = norm_data2['productCode']
    productName = norm_data2['productName']
    productText = norm_data2['productText']
    event_info = [id2, wmoCollectiveId, issuingOffice, issuanceTime, productCode, productName, productText]
    return event_info


# In[9]:


# append new info to df

newdata = []

for i in range(len(norm_data)):
    try:
        event2 = get_id_info(norm_data['@id'][i])
        newdata.append(event2)
        details = pd.DataFrame(newdata, columns = ['id2', 'wmoCollectiveId', 'issuingOffice', 'issuanceTime', 'productCode', 'productName', 'productText']) 
    except KeyError:
        continue


# In[11]:


# adjust format

def fix(text):
    text['productText'].replace("\n", " ")
    return text

SVR = fix(details)


# In[12]:


# [FFW, FLW, TOR]

url_list = ["https://api.weather.gov/products/types/FFW"     # flash flood
            , "https://api.weather.gov/products/types/FLW"   # flood
            , "https://api.weather.gov/products/types/TOR"]  # tornado

# empty list to store all results
results = []

# request api
for url in url_list:
    response = requests.get(url)
    data = response.json()
    # normalize data
    norm_data = json_normalize(data)
    norm_data = json_normalize(norm_data['@graph']).T.set_axis(['series'], axis=1)#, inplace=False)
    results.append(norm_data)


# In[13]:


df_list = [results[0], results[1], results[2]]
data = pd.concat(df_list)

norm_data = data['series'].apply(pd.Series).reset_index(drop = True)


# In[14]:


# get additional information about event

def get_id_info(id):
    response = requests.get(id)
    norm_data2 = response.json()
    id2 = norm_data2['@id']
    wmoCollectiveId = norm_data2['wmoCollectiveId']
    issuingOffice = norm_data2['issuingOffice']
    issuanceTime = norm_data2['issuanceTime']
    productCode = norm_data2['productCode']
    productName = norm_data2['productName']
    productText = norm_data2['productText']
    event_info = [id2, wmoCollectiveId, issuingOffice, issuanceTime, productCode, productName, productText]
    return event_info


# In[15]:


# append new info to df

newdata = []

for i in range(len(norm_data)):
    event2 = get_id_info(norm_data['@id'][i])
    newdata.append(event2)
    details = pd.DataFrame(newdata, columns = ['id2', 'wmoCollectiveId', 'issuingOffice', 'issuanceTime', 'productCode', 'productName', 'productText'])


# In[16]:


# adjust format

def fix(text):
    text['productText'].replace("\n", " ")
    return text

ALL = fix(details)


# In[ ]:


# combine into single df

df_list = [SVR, ALL]
data = pd.concat(df_list)


# In[17]:


# create unique .csv titled with date

current_date = datetime.datetime.now()
filename = str(current_date.year) + str(current_date.month) + str(current_date.day)
#details.to_csv(str(filename + '.csv'))
os.makedirs('files', exist_ok = True)  
data.to_csv(str('files/' + filename + '.csv'), index = False)

